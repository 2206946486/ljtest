# -*- coding: UTF-8 -*-
"""
@author: lj
@date: 2019/3/5
"""
import os
import pymysql
from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from app.config import load_config


pymysql.install_as_MySQLdb()
os.environ.setdefault('MODE','LOCAL')

config = load_config()
db = SQLAlchemy()
celery = Celery(__name__, broker=config.CELERY_BROKER_URL)
celery.autodiscover_tasks(["app.tasks"])


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)
    celery.config_from_object(config)

    from app.apis.html import html
    app.register_blueprint(html)

    from app.apis.partner import partners
    app.register_blueprint(partners, url_prefix="/partners")

    return app