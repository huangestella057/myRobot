# 使用官方 Python 镜像
FROM python:3.9-slim

# 安装系统级依赖 (OpenCV, PyAudio, 语音库等需要)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    portaudio19-dev \
    python3-all-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有代码到容器
COPY . .

# 暴露 Hugging Face 指定的端口
EXPOSE 7860

# 启动 Streamlit
# 注意：必须指定 server.port 为 7860，server.address 为 0.0.0.0
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
