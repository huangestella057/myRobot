FROM python:3.9-slim

# --- 关键修改：安装 OpenCV 和系统所需的库 ---
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    portaudio19-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
# ---------------------------------------

WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 启动命令
EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
