
## IOT_Server项目结构说明
IOT_Server基本结构如下：
```
|IOT_Server
|--app/
|----apis/
|----configs/
|----models/
|----tasks/
|----tools/
|--conf/
|--docker/
|--docs/
|--scripts/
```
各级文件夹使用介绍：

- app: 代码核心
    - app/apis: 所有视图文件代码
    - app/configs: 配置文件代码
    - app/models: 所有模型文件代码
    - app/tasks: 所有异步任务代码
    - app/tools: 所有工具模块代码
- conf: 启动配置
- docker: Docker相关文件
- docs: 文档
- scripts: 脚本文件

## 依赖

- 安装
```
pip3 install -r conf/requirements.txt
```
- 写入配置
```
pip3 freeze > conf/requirements.txt
```

## app启动方式
```
gunicorn -c conf/gunicorn.py wsgi:app
```

## 脚本命令使用方式
```
python3 manage.py xxx
```

## celery启动方式
```
celery worker -B -A celery_tasks.celery_server -l info
```
