import streamlit as st
import datetime
import calendar


def render_home():
    # 配色常量
    MAIN_BLUE = "#2AA9C9"
    MINT_GREEN = "#00BFA5"
    LIGHT_BLUE = "#B2EBF2"

    st.markdown(f"<h2 style='color:#1A3A3A;'>嗨，开发者！</h2><p style='color:gray;'>这是你今天的实验室概览</p>",
                unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # 1. 左上卡片：机器人能力进度 (圆形球体设计)
        st.markdown(f"""
            <div class="card">
                <h4 style='margin-top:0; color:#1A3A3A;'>机器人能力进阶</h4>
                <div style="display: flex; justify-content: space-around; align-items: center; padding: 20px 0;">
                    <!-- 动作控制球 -->
                    <div style="text-align: center;">
                        <div style="width: 100px; height: 100px; background: {MAIN_BLUE}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; box-shadow: 0 10px 20px rgba(42,169,201,0.3); font-size: 20px;">65%</div>
                        <p style="margin-top:10px; font-size:14px;">动作控制</p>
                    </div>
                    <!-- 视觉追踪球 (进度稍小，尺寸也稍小) -->
                    <div style="text-align: center;">
                        <div style="width: 80px; height: 80px; background: {MINT_GREEN}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; box-shadow: 0 8px 15px rgba(0,191,165,0.3); font-size: 16px;">30%</div>
                        <p style="margin-top:10px; font-size:14px;">视觉追踪</p>
                    </div>
                    <!-- 语音交互球 (更小) -->
                    <div style="text-align: center;">
                        <div style="width: 60px; height: 60px; background: {LIGHT_BLUE}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #012a4a; font-weight: bold; border: 1px solid {MAIN_BLUE}; font-size: 14px;">15%</div>
                        <p style="margin-top:10px; font-size:14px;">语音交互</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 2. 左下卡片：今日学习时长
        st.markdown(f"""
            <div class="card">
                <h4 style='margin-top:0; color:#1A3A3A;'>今日学习时长</h4>
                <div style="display: flex; align-items: baseline;">
                    <span style="font-size: 48px; font-weight: bold; color: {MAIN_BLUE};">2.5</span>
                    <span style="margin-left: 10px; color: gray;">Hours</span>
                </div>
                <div style="background: #F0F0F0; height: 12px; border-radius: 6px; margin-top: 15px;">
                    <div style="background: linear-gradient(90deg, {MAIN_BLUE}, {MINT_GREEN}); width: 62.5%; height: 12px; border-radius: 6px;"></div>
                </div>
                <p style="font-size: 12px; color: gray; margin-top: 10px;">目标完成度: 62.5% (距目标还剩 1.5h)</p>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        # 3. 右上卡片：美化日历设计
        today = datetime.date.today()
        cal = calendar.monthcalendar(today.year, today.month)
        month_name = today.strftime("%B %Y")

        # 模拟已打卡的日期
        checked_days = [1, 2, 4, 8, 15, today.day]

        cal_html = f"""
        <div class="card" style="background: #012a4a; color: white; min-height: 380px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <span style="font-size: 18px; font-weight: bold;">{month_name}</span>
                <span style="background: {MINT_GREEN}; padding: 4px 12px; border-radius: 20px; font-size: 12px;">今日已学</span>
            </div>
            <table style="width: 100%; text-align: center; border-collapse: collapse;">
                <tr style="opacity: 0.6; font-size: 12px;">
                    <th>MO</th><th>TU</th><th>WE</th><th>TH</th><th>FR</th><th>SA</th><th>SU</th>
                </tr>
        """
        for week in cal:
            cal_html += "<tr>"
            for day in week:
                if day == 0:
                    cal_html += "<td></td>"
                else:
                    style = ""
                    if day in checked_days:
                        style = f"background: {MINT_GREEN}; border-radius: 50%; width: 30px; height: 30px; display: inline-flex; align-items: center; justify-content: center; color: white; font-weight: bold;"
                    else:
                        style = "width: 30px; height: 30px; display: inline-flex; align-items: center; justify-content: center;"
                    cal_html += f"<td><div style='margin: 5px 0; {style}'>{day}</div></td>"
            cal_html += "</tr>"

        cal_html += "</table></div>"
        st.markdown(cal_html, unsafe_allow_html=True)

        # 4. 右下：快速跳转按钮
        st.markdown(f"""
            <div class="card">
                <h4 style='margin-top:0;'>快速进入</h4>
                <div style="display:grid; gap:10px;">
                    <button style="width:100%; padding:12px; border-radius:12px; border:1px solid {LIGHT_BLUE}; background:white; color:{MAIN_BLUE}; text-align:left; cursor:pointer;">🐍 Python 基础课程</button>
                    <button style="width:100%; padding:12px; border-radius:12px; border:none; background:{MAIN_BLUE}; color:white; text-align:left; cursor:pointer;">🎮 模拟机器人控制</button>
                </div>
            </div>
        """, unsafe_allow_html=True)