import streamlit as st


def render_settings():
    st.markdown("<h2 style='color:#012a4a;'>⚙️ 实验室设置</h2>", unsafe_allow_html=True)

    st.subheader("个人学习目标")
    st.slider("每日目标时长 (Hours)", 1.0, 8.0, 4.0)

    st.subheader("通知偏好")
    st.checkbox("开启学习提醒", value=True)
    st.checkbox("新课程发布通知", value=True)

    if st.button("保存更改"):
        st.toast("设置已更新！", icon="✅")