# 使用 Python 3.12 的 Alpine Linux 版本作为基础镜像
# Alpine 是一个很小的 Linux 系统，可以让镜像体积更小
FROM python:3.12-alpine

# 设置容器内部的工作目录为 /app
# 后面的 COPY、RUN、CMD 默认都会在 /app 目录下执行
WORKDIR /app

# 把本地项目中的 requirements.txt 复制到容器的 /app 目录
# requirements.txt 里面通常写着项目需要安装的 Python 依赖
COPY requirements.txt .

# 根据 requirements.txt 安装 Python 依赖
# --no-cache-dir 表示不保留 pip 缓存，减少镜像体积
RUN pip install --no-cache-dir -r requirements.txt

# 把本地项目中的 app.py 复制到容器的 /app 目录
# app.py 是这个 Python 项目的主程序
COPY app.py .

# 声明容器内部程序会使用 5000 端口
# 注意：EXPOSE 只是声明端口，不会自动把端口映射到宿主机
EXPOSE 5000

# 容器启动时默认执行的命令
# 等价于在容器里运行：python app.py
CMD ["python", "app.py"]
