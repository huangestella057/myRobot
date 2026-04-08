import streamlit as st
import cv2
import os
import pandas as pd
import numpy as np
from PIL import Image

# 尝试导入 DeepFace
try:
    from deepface import DeepFace

    HAS_DEEPFACE = True
except ImportError:
    HAS_DEEPFACE = False


def render_vision_tab():
    st.markdown("""
        <div style="border-left: 5px solid #FF4B4B; padding: 10px; background: #f9f9f9; border-radius: 5px; margin-bottom: 20px;">
            <h4 style="margin:0;">机器视觉：人脸识别与表情分析系统</h4>
            <p style="color:gray; font-size:14px; margin:5px 0 0 0;">通过深度学习模型实时捕捉人类情感，实现人机共情交互。</p>
        </div>
    """, unsafe_allow_html=True)

    if not HAS_DEEPFACE:
        st.error("检测到环境缺少 DeepFace 库。请在终端运行: `pip install deepface` 并重启应用。")

    v_col1, v_col2 = st.columns([1.5, 1])

    with v_col2:
        st.subheader("🛠️ 技术原理与工具说明")

        with st.expander("1. 使用工具：DeepFace", expanded=True):
            st.markdown("""
            **DeepFace** 是一个用于 Python 的轻量级人脸识别和面部属性分析框架。它集成了多种最先进的模型（如 VGG-Face、Google FaceNet、OpenFace 等）。
            - **功能**：识别年龄、性别、种族和**情绪**。
            - **优势**：高度封装，只需几行代码即可完成复杂的深度学习推理。
            """)

        with st.expander("2. 工作流程解析", expanded=False):
            st.markdown("""
            表情识别主要分为三个核心步骤：
            1. **人脸检测 (Detection)**：在复杂的背景中定位人脸矩形区域。
            2. **特征提取 (Feature Extraction)**：通过卷积神经网络 (CNN) 提取面部肌肉微小的变化特征。
            3. **分类决策 (Classification)**：将特征向量输入 Softmax 层，输出各情绪的百分比（如：Happy: 95%, Sad: 2%）。
            """)

        st.divider()
        run_vision = st.toggle("🚀 开启实时表情分析", help="开启后将调用本地摄像头进行实时识别")

    with v_col1:
        st.subheader("👁️ 实时视觉反馈")

        if run_vision:
            # 建立视频捕获窗口
            FRAME_WINDOW = st.image([])
            camera = cv2.VideoCapture(0)  # 0 代表默认摄像头

            # 用于显示检测到的表情
            status_placeholder = st.empty()

            while run_vision:
                ret, frame = camera.read()
                if not ret:
                    st.error("无法获取摄像头画面。")
                    break

                # 转换为 RGB 格式供 Streamlit 显示
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 每隔一定帧数处理一次，防止网页卡顿
                try:
                    # 使用 DeepFace 分析情绪
                    # enforce_detection=False 防止因人脸太小或遮挡导致报错
                    objs = DeepFace.analyze(frame_rgb, actions=['emotion'], enforce_detection=False)

                    # 获取主导情绪
                    dominant_emotion = objs[0]['dominant_emotion']

                    # 在画面上绘制结果
                    # 注意：DeepFace 分析的是 RGB，绘制文字建议在原始 frame 上或 RGB 上
                    cv2.putText(frame_rgb, f"Emotion: {dominant_emotion}", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    status_placeholder.markdown(f"**当前检测到表情：** `{dominant_emotion}`")
                except Exception as e:
                    pass

                FRAME_WINDOW.image(frame_rgb)

            camera.release()
        else:
            st.markdown("""
                <div style="background:#000; height:350px; border-radius:15px; display:flex; align-items:center; justify-content:center; color:white; border: 2px dashed #444;">
                    <div style="text-align:center;">
                        <p style="font-size:40px;">📷</p>
                        <p style="color:#888;">摄像头未开启，请点击右侧开关</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)