# -*- coding: UTF-8 -*-
"""
@author: lj
@date: 2019/3/5
"""
from app.config.defualt import Config


class OnlineConfig(Config):
    ADDR = "http://www.lzzhq.cn/"

    # mysql
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "admin123"
    MYSQL_DB = "iot"
    SQLALCHEMY_DATABASE_URI = "mysql://{user}:{pwd}@{host}:{port}/{db}".format(user=MYSQL_USER, pwd=MYSQL_PWD,
                                                                               host=MYSQL_HOST,
                                                                               port=MYSQL_PORT, db=MYSQL_DB)

    # redis
    REDIS_HOST = "r-wz91122e8d2dd9b4.redis.rds.aliyuncs.com"
    REDIS_PORT = 6379
    REDIS_PWD = "admin123"
    REDIS_DB = 3
    REDIS_URL = "redis://:{pwd}@{host}:{port}/{db}".format(pwd=REDIS_PWD,
                                                           host=REDIS_HOST,
                                                           port=REDIS_PORT,
                                                           db=REDIS_DB)

    CELERY_BROKER_URL = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)
    CELERY_RESULT_BACKEND = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)