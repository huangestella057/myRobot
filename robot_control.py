import streamlit as st
from control_tabs.voice_tab import render_voice_tab
from control_tabs.servo_tab import render_servo_tab
from control_tabs.vision_tab import render_vision_tab

def render_robot_control():
    st.markdown("<h2 style='color:#1A3A3A;'>🎮 机器人实时控制面板</h2>", unsafe_allow_html=True)

    # 初始化语音状态（供 voice_tab 使用）
    if "voice_stage" not in st.session_state:
        st.session_state.voice_stage = "idle"

    tab1, tab2, tab3 = st.tabs(["🎙️ 语音系统教学", "🦾 舵机控制", "👁️ 机器视觉"])

    with tab1:
        render_voice_tab()
    with tab2:
        render_servo_tab()
    with tab3:
        render_vision_tab()