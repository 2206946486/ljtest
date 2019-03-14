# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18
@description: 全局配置
"""

from celery.schedules import crontab


class Config(object):

    # mysql
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 200
    SQLALCHEMY_POOL_TIMEOUT = 7200
    CELERY_TIMEZONE = "Asia/Shanghai"
    CELERYBEAT_SCHEDULE = {
        "check_plan": {
            "task": "iot.tasks.check_plan",
            "schedule": crontab(minute=10, hour=0, day_of_month=27),
            "args": (0,),
        },
        "check_order": {
            "task": "iot.tasks.check_order",
            "schedule": crontab(minute="*/3"),
        },
        "check_card": {
            "task": "iot.tasks.check_card",
            "schedule": crontab(minute=25, hour="*/6"),
        },
    }

    # celery
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 24 * 60 * 60
    CELERY_ACCEPT_CONTENT = ['json']


    # excel存放路径
    PATH = "/var/tmp/www/html/export2/iot"
    # excel下载路径
    DOWNLOAD_PATH = "/export2/iot"

    # session-secret
    SECRET_KEY = "qhyl&12$*-aa22f0b3d3bb494-"
