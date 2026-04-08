from vosk import Model, KaldiRecognizer
import pyaudio
import json
import struct
from ollama import chat
import re
import asyncio
import edge_tts
import pygame
import os
import csv
import threading
import time
import queue


class IntelligentAgent():
    def __init__(self):
        # 初始化Vosk语音识别模型（中文）
        self.model = Model('zh')

        # 初始化音频资源
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4000
        )

        # 初始化识别器
        self.recognizer = KaldiRecognizer(self.model, 16000)

        # 状态变量
        self.last_recognized_text = ""
        self.is_listening = False
        self.running = True
        self.audio_playing = False  # 标志位，表示是否正在播放音频

        # 新增：音频队列和播放线程
        self.audio_queue = queue.Queue()
        self.playback_thread = threading.Thread(target=self.audio_playback_worker, daemon=True)
        self.playback_thread.start()

        # 新增：当前处理中的响应
        self.current_response = ""
        self.response_lock = threading.Lock()

    def is_speech(self, data, threshold=500):
        """判断音频数据是否包含语音活动"""
        audio_data = struct.unpack(f'{len(data) // 2}h', data)
        amplitude = sum(abs(x) for x in audio_data) / len(audio_data)
        return amplitude > threshold

    def start_chat(self, user_message):
        """调用大模型进行对话，流式处理响应"""
        stream = chat(
            model='deepseek-r1:8b',
            messages=[{'role': 'user', 'content': user_message}],
            stream=True,
        )

        # 停止语音识别
        self.stop_speech_recognition()

        # 处理流式响应
        full_response = ""
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content

                # 处理并播放当前片段
                self.process_response_chunk(content)

        print()  # 换行

        # 处理完整的响应（用于CSV写入等）
        with self.response_lock:
            self.current_response = full_response
            self.process_full_response()

        return full_response

    def process_response_chunk(self, chunk):
        """处理并播放单个响应片段"""
        # 简单分割逻辑（可根据需要改进）
        if any(punc in chunk for punc in "。？！"):
            with self.response_lock:
                # 将新内容添加到当前响应
                self.current_response += chunk

                # 分割句子
                sentences = re.split(r'([。？！])', self.current_response)
                sentences = [s + p for s, p in zip(sentences[::2], sentences[1::2])]

                # 如果有完整句子
                if len(sentences) > 1:
                    # 播放所有完整句子（除了最后一个）
                    for sentence in sentences[:-1]:
                        self.queue_audio(sentence)

                    # 保留未完成的句子
                    self.current_response = sentences[-1] if sentences[-1] else ""

    def process_full_response(self):
        """处理完整的响应"""
        # 检查是否存在<think>和</think>中间的内容
        think_content = re.findall(r'<think>.*?</think>', self.current_response, flags=re.DOTALL)

        # 如果存在<think>和</think>中间的内容，将其删除
        if think_content:
            cleaned_response = re.sub(r'<think>.*?</think>', '', self.current_response, flags=re.DOTALL)
            # 写入CSV文件
            self.write_to_csv(cleaned_response)
        else:
            # 写入CSV文件
            self.write_to_csv(self.current_response)

        # 处理未完成的句子
        if self.current_response:
            self.queue_audio(self.current_response)
            self.current_response = ""

    def write_to_csv(self, response):
        """将处理后的回答写入CSV文件，每次覆盖原文件"""
        # 删除原文件（如果存在）
        if os.path.exists('response.csv'):
            os.remove('response.csv')

        # 通过标点符号分割
        sentences = re.split(r'([。？！])', response)

        # 过滤空字符串并组合句子
        sentences = [s + p for s, p in zip(sentences[::2], sentences[1::2])]

        # 写入新文件
        with open('response.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Sentence'])
            for idx, sentence in enumerate(sentences):
                writer.writerow([sentence])

    def queue_audio(self, sentence):
        """将句子加入音频队列"""
        if sentence.strip():  # 忽略空句子
            # 生成唯一文件名
            timestamp = int(time.time() * 1000)
            audio_file = f"response_{timestamp}.mp3"

            # 异步生成音频
            threading.Thread(target=self.generate_audio_async, args=(sentence, audio_file), daemon=True).start()

            # 将音频文件加入播放队列
            self.audio_queue.put(audio_file)

    def generate_audio_async(self, sentence, audio_file):
        """异步生成音频文件"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.generate_audio(sentence, audio_file))
        loop.close()

    async def generate_audio(self, sentence, audio_file):
        """生成语音文件"""
        communicate = edge_tts.Communicate(sentence, 'zh-CN-XiaoyiNeural')
        await communicate.save(audio_file)

    def audio_playback_worker(self):
        """音频播放工作线程"""
        pygame.mixer.init()

        while self.running:
            try:
                audio_file = self.audio_queue.get(timeout=1)

                if os.path.exists(audio_file):
                    # 播放音频
                    self.audio_playing = True
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.play()

                    # 等待播放完成
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)

                    # 删除文件
                    try:
                        os.remove(audio_file)
                    except Exception as e:
                        print(f"删除音频文件失败: {e}")

                    self.audio_playing = False
                else:
                    print(f"音频文件不存在: {audio_file}")

                self.audio_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"音频播放错误: {e}")

        pygame.mixer.quit()

    def stop_speech_recognition(self):
        """停止语音识别"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def resume_speech_recognition(self):
        """恢复语音识别"""
        if not self.stream:
            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4000
            )

    def speech_recognition_loop(self):
        """语音识别主循环"""
        try:
            buffer = bytearray()  # 用于缓存音频数据
            speech_detected = False  # 语音活动状态
            silence_counter = 0  # 记录连续静默的帧数

            while self.running:
                # 检查是否正在播放音频
                if self.audio_playing:
                    time.sleep(0.1)
                    continue

                # 检查音频流是否可用
                if not self.stream:
                    time.sleep(0.1)
                    continue

                # 读取音频数据
                try:
                    data = self.stream.read(4000, exception_on_overflow=False)
                except Exception as e:
                    print(f"读取音频流错误: {e}")
                    time.sleep(0.1)
                    continue

                buffer.extend(data)

                # 检测是否包含语音活动
                current_speech = self.is_speech(data)

                if current_speech:
                    # 如果当前帧包含语音活动
                    if not speech_detected:
                        speech_detected = True
                    silence_counter = 0  # 重置静默计数器
                else:
                    # 如果当前帧不包含语音活动
                    if speech_detected:
                        silence_counter += 1

                        if silence_counter >= 3:  # 连续静默帧数3，认为语音活动结束
                            self.last_recognized_text = ""
                            if self.recognizer.AcceptWaveform(bytes(buffer)):
                                result = self.recognizer.Result()
                                text = json.loads(result)['text'].replace(' ', ' ')
                                if text:
                                    self.last_recognized_text = text
                            else:
                                # 如果识别未完成，获取最终结果
                                final_result = self.recognizer.FinalResult()
                                text = json.loads(final_result)['text'].replace(' ', ' ')
                                if text:
                                    self.last_recognized_text = text

                            # 检查是否是激活/结束命令
                            if self.last_recognized_text:
                                print("\n识别结果：", self.last_recognized_text)

                                # 激活对话
                                if "你好" in self.last_recognized_text and not self.is_listening:
                                    self.is_listening = True
                                    print("\nAI：", end='', flush=True)
                                    self.start_chat("你是一个友善开朗乐于助人的AI助手" + self.last_recognized_text)

                                # 结束对话
                                elif "再见" in self.last_recognized_text and self.is_listening:
                                    self.is_listening = False
                                    print("\nAI：再见！期待下次和你聊天。")
                                    self.running = False
                                    break

                                # 正常对话
                                elif self.is_listening:
                                    print("\nAI：", end='', flush=True)
                                    self.start_chat("你是一个友善开朗乐于助人的AI助手" + self.last_recognized_text)

                            # 清空缓存和重置状态
                            buffer.clear()
                            speech_detected = False
                            silence_counter = 0
        except KeyboardInterrupt:
            print("\n识别已停止")
        finally:
            # 在退出时获取最终结果
            if buffer:
                if self.recognizer.AcceptWaveform(bytes(buffer)):
                    result = self.recognizer.Result()
                    text = json.loads(result)['text'].replace(' ', ' ')
                    if text:
                        self.last_recognized_text = text
                else:
                    final_result = self.recognizer.FinalResult()
                    text = json.loads(final_result)['text'].replace(' ', ' ')
                    if text:
                        self.last_recognized_text = text

            # 检查是否是激活/结束命令
            if self.last_recognized_text:
                print("\n识别结果：", self.last_recognized_text)

                # 激活对话
                if "你好" in self.last_recognized_text and not self.is_listening:
                    self.is_listening = True
                    print("\nAI：", end='', flush=True)
                    self.start_chat("你是一个友善开朗乐于助人的AI助手" + self.last_recognized_text)

                # 结束对话
                elif "再见" in self.last_recognized_text and self.is_listening:
                    self.is_listening = False
                    print("\nAI：再见！期待下次和你聊天。")
                    self.running = False

            # 关闭音频流
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.p:
                self.p.terminate()
            print("\n音频流已关闭")

    def run(self):
        """启动智能助手"""
        print("智能助手已启动，等待您的呼唤...")
        while self.running:
            self.speech_recognition_loop()
            if not self.running:
                break
        print("智能助手已停止")


# 使用示例
if __name__ == "__main__":
    agent = IntelligentAgent()
    agent.run()