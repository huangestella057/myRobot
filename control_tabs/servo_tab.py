import streamlit as st
import serial
import pandas as pd

MINT_GREEN = "#00BFA5"

# 舵机配置信息表 (根据上传图片整理)
SERVO_DATA = [
    {"类别": "头上下", "ID": 1, "最小值": 1348, "最大值": 2748, "描述": "1348(下) - 2748(上)"},
    {"类别": "头左右", "ID": 2, "最小值": 1448, "最大值": 2648, "描述": "1448(左) - 2648(右)"},
    {"类别": "摆头", "ID": 3, "最小值": 1348, "最大值": 2748, "描述": "1348(右) - 2748(左)"},
    {"类别": "微笑左", "ID": 6, "最小值": 2048, "最大值": 2548, "描述": "2048(正常) - 2548"},
    {"类别": "微笑右", "ID": 7, "最小值": 1548, "最大值": 2048, "描述": "1548 - 2048(正常)"},
    {"类别": "眼球", "ID": 8, "最小值": 1800, "最大值": 2300, "描述": "1800(右最大) - 2300(左最大)"},
    {"类别": "皱眉左", "ID": 9, "最小值": 1800, "最大值": 2248, "描述": "1800(上) - 2248(下)"},
    {"类别": "皱眉右", "ID": 10, "最小值": 1800, "最大值": 2248, "描述": "1800(下) - 2248(上)"},
    {"类别": "下巴", "ID": 11, "最小值": 2048, "最大值": 2348, "描述": "2048(闭嘴) - 2348(张嘴)"},
    {"类别": "上嘴唇左", "ID": 12, "最小值": 1848, "最大值": 2048, "描述": "1848(上翘) - 2048(正常)"},
    {"类别": "上嘴唇右", "ID": 13, "最小值": 2048, "最大值": 2248, "描述": "2048(正常) - 2248(上翘)"},
    {"类别": "眨眼左", "ID": 14, "最小值": 2048, "最大值": 2500, "描述": "2048(正常) - 2500(闭眼)"},
    {"类别": "眨眼右", "ID": 15, "最小值": 1600, "最大值": 2048, "描述": "1600(闭眼) - 2048(正常)"},
]

# 初始化串口
if 'ser' not in st.session_state:
    try:
        # 请根据实际情况修改端口号，如 'COM3' 或 '/dev/ttyUSB0'
        st.session_state.ser = serial.Serial('COM3', 115200, timeout=0.1)
    except:
        st.session_state.ser = None


def send_servo_command(servo_id, position, speed=1000):
    """根据《通讯协议手册》1.3.3节构建指令包并发送"""
    if st.session_state.ser and st.session_state.ser.is_open:
        instruction = 0x03  # WRITE DATA
        address = 0x2A  # 目标位置寄存器首地址

        # 参数：地址(1B), 位置(2B), 时间(2B), 速度(2B)
        # 字节序：低位在前，高位在后
        params = [
            address,
            position & 0xFF, (position >> 8) & 0xFF,
            0x00, 0x00,
            speed & 0xFF, (speed >> 8) & 0xFF
        ]

        length = len(params) + 2  # N+2
        checksum = ~(servo_id + length + instruction + sum(params)) & 0xFF  #

        packet = bytearray([0xFF, 0xFF, servo_id, length, instruction] + params + [checksum])
        st.session_state.ser.write(packet)


def render_servo_tab():
    st.markdown(
        f"<div style='border-left: 5px solid {MINT_GREEN}; padding:10px;'><h4>🤖 机器人表情与头部动作控制</h4></div>",
        unsafe_allow_html=True)

    # 1. 显示参数参考表，方便用户查看
    with st.expander("查看舵机参数手册 (ID、范围及指令说明)", expanded=False):
        df = pd.DataFrame(SERVO_DATA)
        st.table(df[["类别", "ID", "最小值", "最大值", "描述"]])
        st.info("提示：所有舵机的默认初始位（缺省值）均为 2048。")

    # 2. 控制界面
    col1, col2 = st.columns(2)

    # 将舵机分为两组显示
    half = len(SERVO_DATA) // 2 + 1

    for i, servo in enumerate(SERVO_DATA):
        target_col = col1 if i < half else col2
        with target_col:
            # 根据手册范围动态生成滑块
            val = st.slider(
                f"{servo['类别']} (ID: {servo['ID']})",
                min_value=int(servo['最小值']),
                max_value=int(servo['最大值']),
                value=2048,
                help=servo['描述'],
                key=f"servo_{servo['ID']}"
            )

            # 当数值改变或点击按钮时发送串口指令
            if st.button(f"执行 {servo['类别']}", key=f"btn_{servo['ID']}"):
                send_servo_command(servo['ID'], val)
                st.toast(f"已发送 ID:{servo['ID']} 位置:{val}")

    # 3. 全局重置
    st.divider()
    if st.button("全部恢复初始位 (2048)"):
        for servo in SERVO_DATA:
            send_servo_command(servo['ID'], 2048)
        st.success("所有舵机已归位")