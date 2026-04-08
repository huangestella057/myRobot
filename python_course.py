import streamlit as st


def render_python_course():
    st.markdown("<h2 style='color:#1A3A3A;'>🐍 Python 编程基础</h2>", unsafe_allow_html=True)
    st.write("在这里学习机器人编程的灵魂语言。")

    # 知识点 1：变量
    with st.container():
        st.markdown("""
        <div class="card">
            <h3>1. 变量与数据类型</h3>
            <p>变量就像机器人的<strong>寄存器</strong>，用来存储传感器数据或控制参数。</p>
            <pre style="background:#f4f4f4; padding:10px; border-radius:10px;">
angle = 90          # 整数 (int)
robot_name = "Alpha" # 字符串 (str)
is_active = True     # 布尔值 (bool)
            </pre>
        </div>
        """, unsafe_allow_html=True)

        # 练习题 1
        st.markdown("#### ✍️ 练习：定义一个表示距离的变量 `distance` 并赋值为 100")
        col1, col2 = st.columns([3, 1])
        with col1:
            user_input_1 = st.text_input("在下方输入代码：", key="ex1")
        with col2:
            st.write("")  # 占位
            st.write("")
            if st.button("检查答案", key="btn1"):
                if user_input_1.strip().replace(" ", "") == "distance=100":
                    st.success("回答正确！🎉")
                else:
                    st.error("再试一次吧，注意变量名和赋值。")

    st.markdown("---")

    # 知识点 2：函数
    with st.container():
        st.markdown("""
        <div class="card">
            <h3>2. 函数定义</h3>
            <p>函数允许我们将一套动作（如“向前走”）封装起来，重复调用。</p>
            <pre style="background:#f4f4f4; padding:10px; border-radius:10px;">
def move_forward():
    print("机器人正在向前移动...")
            </pre>
        </div>
        """, unsafe_allow_html=True)

        # 练习题 2
        st.markdown("#### ✍️ 练习：补全函数调用代码，使程序打印输出")
        st.code("def say_hello():\n    print('Hello Robot')\n\n# 在下方调用该函数")
        col3, col4 = st.columns([3, 1])
        with col3:
            user_input_2 = st.text_input("输入调用指令：", key="ex2")
        with col4:
            st.write("")
            st.write("")
            if st.button("检查答案", key="btn2"):
                if user_input_2.strip() == "say_hello()":
                    st.success("完美！你掌握了函数调用。")
                else:
                    st.warning("提示：直接写出函数名加括号即可。")