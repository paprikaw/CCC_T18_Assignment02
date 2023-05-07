# 使用官方 Python 镜像作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 将 requirement.txt 文件复制到工作目录
COPY requirements.txt .

# 安装依赖项
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 将构建产物复制到 Flask 静态文件夹
COPY backend /app/backend
COPY frontend  /app/frontend
COPY data /app/data

# 进入后端工作目录
WORKDIR /app/backend

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露端口
EXPOSE 5000

# 启动 Flask 应用
CMD ["flask", "run"]
