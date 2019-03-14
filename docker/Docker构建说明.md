## Docker构建
- 安装Docker，文档说明：https://blog.csdn.net/y472360651/article/details/81289061
- 安装Docker-Compose，文档说明：https://blog.csdn.net/y472360651/article/details/81836272
- 进入项目所在目录
- 进入项目之后，进入`docker`文件：
```
root@ubuntu:~/IOT_Server# cd docker
```
- 执行以下命令：
```
root@ubuntu:~/IOT_Server/docker# docker-compose up
Building iot_server
Step 1/6 : FROM python:3.6
 ---> 3e4c2972dc8d
Step 2/6 : COPY ./ /IOT_server
 ---> 680afb8cb338
Step 3/6 : WORKDIR /IOT_server
 ---> Running in 1b8ff98bb765
Removing intermediate container 1b8ff98bb765
 ---> c854b8504fbe
Step 4/6 : RUN pip install -r ./conf/requirements.txt
 ---> Running in 4dc369b5536c
 ...
```
- over