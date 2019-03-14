# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18
@description: 线上环境配置
"""

from app.configs.default import Config


class OnlineConfig(Config):
    ADDR = "https://iot.china-m2m.com"

    # mysql
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "111"
    MYSQL_DB = "iot"
    SQLALCHEMY_DATABASE_URI = "mysql://{user}:{pwd}@{host}:{port}/{db}".format(user=MYSQL_USER, pwd=MYSQL_PWD,
                                                                               host=MYSQL_HOST,
                                                                               port=MYSQL_PORT, db=MYSQL_DB)

    # redis
    REDIS_HOST = "r-wz91122e8d2dd9b4.redis.rds.aliyuncs.com"
    REDIS_PORT = 6379
    REDIS_PWD = "ZpNg2rqb"
    REDIS_DB = 3
    REDIS_URL = "redis://:{pwd}@{host}:{port}/{db}".format(pwd=REDIS_PWD,
                                                           host=REDIS_HOST,
                                                           port=REDIS_PORT,
                                                           db=REDIS_DB)

    CELERY_BROKER_URL = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)
    CELERY_RESULT_BACKEND = 'redis://{}:{}/1'.format(REDIS_HOST, REDIS_PORT)
