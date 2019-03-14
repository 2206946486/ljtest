# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/19 
"""
from app import db
from datetime import datetime
from app.tools.dbs import JsonSerializer


class Register(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __json_hidden__ = ["partner_cards", "orders", "card_plans", 'auth']

    __tablename__ = "iot_register"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True, default='')
    password = db.Column(db.String(100), nullable=False, default='')
    telphone = db.Column(db.String(11), nullable=False, default='')
    status = db.Column(db.SmallInteger, nullable=False, default=0)
    user_remark = db.Column(db.String(200), nullable=False, default='')
    remark = db.Column(db.String(200), nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, password, telphone, status,user_remark,remark,
                 created_at=datetime.now(), updated_at=datetime.now()):
        self.username = username
        self.password = password
        self.telphone = telphone
        self.status = status
        self.user_remark = user_remark
        self.remark = remark
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return "Register<{0}, {1}>".format(self.id, self.username)

    __repr__ = __str__
