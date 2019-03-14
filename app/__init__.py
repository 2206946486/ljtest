# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18
"""

import os
import pymysql
from flask import Flask
from celery import Celery
from app.configs import load_config
from flask_sqlalchemy import SQLAlchemy


pymysql.install_as_MySQLdb()
os.environ.setdefault("MODE", "LOCAL")

config = load_config()
db = SQLAlchemy()
celery = Celery(__name__, broker=config.CELERY_BROKER_URL)
celery.autodiscover_tasks(["app.tasks"])


def create_app():

    app = Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)
    celery.config_from_object(config)

    print("当前环境变量为: {env}".format(env=os.environ.get("MODE")))

    from app.apis.html import html
    app.register_blueprint(html)

    from app.apis.partners import partners
    app.register_blueprint(partners, url_prefix="/partners")

    from app.apis.authorities import authorities
    app.register_blueprint(authorities, url_prefix="/authorities")

    from app.apis.cards import cards
    app.register_blueprint(cards, url_prefix="/cards")

    from app.apis.plans import plans
    app.register_blueprint(plans, url_prefix="/plans")

    return app
