# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""
from app import celery


@celery.task
def task_1():
    pass