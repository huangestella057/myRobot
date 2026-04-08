import streamlit as st


def render_robot_info():
    st.markdown("<h1 style='text-align: center; color:#1E3A8A;'>伊娃 (EVA) 机器人硬件规格说明</h1>",
                unsafe_allow_html=True)
    st.markdown("---")

    # 第一部分：核心控制中枢与系统架构
    col1, col2 = st.columns([1, 1.5])
    with col1:
        # 建议替换为PDF中的“机器人内部图”或“整体结构图”
        st.image("https://img.icons8.com/illustrations/400/000000/artificial-intelligence.png",
                 caption="控制中枢架构图")

    with col2:
        st.subheader("🧠 控制中枢 (Control Hub)")
        st.info("**算力核心：** 采用 X86 架构计算机，搭载 NVIDIA RTX 3090 显卡，运行 Ubuntu 20.04 系统。")
        st.write("- **底层控制：** 集成 STM32 单片机，负责面部舵机的实时指令分发。")
        st.write("- **感知层：** 搭载双模蓝牙、Wi-Fi 及 IMU 六轴姿态传感器。")

    st.markdown("---")

    # 第二部分：机械结构与表情系统
    st.subheader("⚙️ 机械结构与动力学")
    m_col1, m_col2, m_col3 = st.columns(3)

    with m_col1:
        st.metric(label="面部自由度 (DoF)", value="13", help="由13个高精度伺服舵机单元组成")
        st.write("**驱动方案：** 采用多圈绝对值编码器伺服舵机。")

    with m_col2:
        st.metric(label="感知精度", value="12 bit", help="磁位置传感器精度")
        st.write("**反馈控制：** 360°磁位置传感器提供高精度位置反馈。")

    with m_col3:
        st.metric(label="制造工艺", value="3D 打印", help="骨架实现方式")
        st.write("**外观材质：** 定制特殊仿真触感皮肤，模仿人脸肌肉。")

    # 第三部分：传感器矩阵与关键技术
    with st.expander("🔍 详细技术参数清单", expanded=False):
        tab1, tab2 = st.tabs(["传感器矩阵", "机械创新点"])
        with tab1:
            st.write("- **视觉：** 非特定人脸识别系统，识别准确率 > 90%。")
            st.write("- **听觉：** ASR 语音识别 + 语义理解交互。")
            st.write("- **姿态：** 仿生头颈三轴旋转机构，支持点头、摇头。")
        with tab2:
            st.write("- **骨架结构：** 通过 SolidWorks (CAD) 优化设计。")
            st.write("- **处理方式：** 串行+并行处理，实现语音与表情低延时同步。")
            st.write("- **未来扩展：** 计划新增 6 个微型舵机，将自由度提升至 19 个。")

    st.success("💡 硬件亮点：突破技术难关，在头盖骨大小区域内布置 13 个多圈绝对值编码器，实现微表情级控制。")