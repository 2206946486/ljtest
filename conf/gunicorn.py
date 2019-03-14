# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""

bind = "{}:{}".format("127.0.0.1", 8100)
backlog = 1024

workers = 2
worker_class = "egg:meinheld#gunicorn_worker"
worker_connections = 1000
max_requests = 10000
timeout = 20

daemon = False
pidfile = "./pidfile"
