FROM python:3.6
# 作者
LABEL author=ycx
# 将上下文所在位置下的所有，拷贝至镜像/IOT_Server
COPY ./ /IOT_Server
# 切换工作目录
WORKDIR /IOT_Server
# 安装依赖
RUN pip install -r ./conf/requirements.txt
# 设置环境变量
ENV MODE=DOCKER
# 启动项目
CMD ["gunicorn", "-c", "conf/gunicorn.py", "wsgi:app"]