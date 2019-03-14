# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/12/17 
"""
from app.configs.default import Config


class DockerConfig(Config):
    ADDR = "http://localhost:8100"

    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "123456"
    MYSQL_DB = "iot1205"
    SQLALCHEMY_DATABASE_URI = "mysql://{user}:{pwd}@{host}:{port}/{db}".format(user=MYSQL_USER, pwd=MYSQL_PWD,
                                                                               host=MYSQL_HOST,
                                                                               port=MYSQL_PORT, db=MYSQL_DB)

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 3
    REDIS_URL = "redis://{host}:{port}/{db}".format(host=REDIS_HOST,
                                                    port=REDIS_PORT,
                                                    db=REDIS_DB)


    CELERY_BROKER_URL = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)
    CELERY_RESULT_BACKEND = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)