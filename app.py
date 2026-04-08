import streamlit as st
from home import render_home
from robot_info import render_robot_info
from settings import render_settings
from python_course import render_python_course
from robot_control import render_robot_control

# 全局配置
st.set_page_config(
    page_title="Be.Robot Lab",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 全局样式注入
st.markdown("""
    <style>
    .stApp { background-color: #F8FDFF; }
    [data-testid="stSidebar"] { background-color: #012a4a; }
    [data-testid="stSidebar"] * { color: white !important; }
    .card {
        background: white;
        padding: 24px;
        border-radius: 28px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.03);
        margin-bottom: 20px;
        border: 1px solid #E0F7FA;
    }
    .stButton>button {
        background-color: #2AA9C9;
        color: white;
        border-radius: 12px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 侧边栏导航
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>Be.Robot</h2>", unsafe_allow_html=True)
    st.markdown("---")
    # 更新导航菜单，加入新功能
    page = st.radio("导航菜单", ["首页", "Python 基础课", "机器人控制", "机器人介绍", "设置"], label_visibility="collapsed")

# 路由分发
if page == "首页":
    render_home()
elif page == "Python 基础课":
    render_python_course()
elif page == "机器人控制":
    render_robot_control()
elif page == "机器人介绍":
    render_robot_info()
elif page == "设置":
    render_settings()