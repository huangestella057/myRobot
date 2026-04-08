import streamlit as st
import os
import pandas as pd

MAIN_BLUE = "#2AA9C9"

def render_voice_tab():
    st.markdown(f"""
        <div style="border-left: 5px solid {MAIN_BLUE}; padding: 10px; background: #f9f9f9; border-radius: 5px; margin-bottom: 20px;">
            <h4 style="margin:0;">语音交互流水线：从 ASR 到 DeepSeek 再到 TTS</h4>
            <p style="color:gray; font-size:14px; margin:5px 0 0 0;">本面板通过实际工具链演示 AI 语音助手的底层逻辑。</p>
        </div>
    """, unsafe_allow_html=True)

    # 状态指示灯
    s_cols = st.columns(4)
    stages = {
        "idle": ["⚪ 等待唤醒", "gray"],
        "listening": ["🟢 Vosk 识别中", "#00BFA5"],
        "thinking": ["🔵 DeepSeek 推理", "#2AA9C9"],
        "speaking": ["🔊 edge-tts 播报", "#FFB300"]
    }
    for i, (key, val) in enumerate(stages.items()):
        is_active = st.session_state.voice_stage == key
        b_color = val[1] if is_active else "#EEEEEE"
        t_color = "white" if is_active else "gray"
        s_cols[i].markdown(f"""
            <div style="background:{b_color}; color:{t_color}; padding:8px; border-radius:8px; text-align:center; font-size:12px; font-weight:bold;">
                {val[0]}
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    v_col, c_col = st.columns([1.2, 1])

    with v_col:
        st.subheader("🛠️ 核心组件技术手册")
        with st.expander("1. 语音识别 (Vosk)", expanded=True):
            st.markdown("""
            **工具：Vosk ASR**
            - **如何下载**：`pip install vosk`，并从官网下载中文模型文件夹 `zh`。
            - **性能表现**：
                - **全本地运行**：无需联网，保护隐私且延迟极低。
                - **跨平台**：支持嵌入式设备（如树莓派），内存占用极小。
                - **精度**：在安静环境下针对中文语音有很高的识别准确率。
            """)
        with st.expander("2. 逻辑推理 (DeepSeek / Ollama)", expanded=False):
            st.markdown("""
            **工具：Ollama + DeepSeek R1**
            - **如何部署**：
                1. 安装 [Ollama](https://ollama.com/)。
                2. 运行命令 `ollama run deepseek-r1:8b`。
            - **为什么选择 DeepSeek**：
                - **思维链 (CoT)**：具备强大的推理能力，能处理复杂逻辑。
                - **本地化成本低**：8B 版本在主流显卡上即可流畅运行。
                - **开源生态**：目前最强的开源模型之一，适配性极佳。
            """)
        with st.expander("3. 语音合成 (edge-tts)", expanded=False):
            st.markdown("""
            **工具：edge-tts (Microsoft Edge 接口)**
            - **如何下载**：`pip install edge-tts`。
            - **性能表现**：
                - **高拟真度**：使用的是微软神经网络语音，听起来非常接近真人。
                - **无需 API Key**：直接通过 Python 脚本调用，方便快捷。
                - **多语种支持**：支持超过 100 种语言和多种音色。
            """)

    with c_col:
        st.subheader("💬 对话记录 (实时读取 robotspeak.py)")
        if os.path.exists('response.csv'):
            try:
                df = pd.read_csv('response.csv')
                for _, row in df.iterrows():
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(row['Sentence'])
            except Exception:
                st.warning("等待数据写入中...")
        else:
            st.info("尚未检测到运行记录。请确保后台 `robotspeak.py` 正在运行。")

        if st.button("🔄 刷新对话状态"):
            st.rerun()