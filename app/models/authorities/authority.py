# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/23 
"""

from app import db
from app.tools.dbs import JsonSerializer


class Authority(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __json_hidden__ = ["relation_auth"]
    __tablename__ = 'iot_authority'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.SmallInteger, nullable=False, default=0)
    name = db.Column(db.String(255), nullable=False)
    describe = db.Column(db.String(255))
    url = db.Column(db.String(255))
    type = db.Column(db.SmallInteger)
    order = db.Column(db.SmallInteger)
    partner_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    icon = db.Column(db.String(255))

    def __init__(self, name, describe, icon, parent_id, partner_id, url=None, type=0, order=0, status=0, *args,
                 **kwargs):
        self.name = name
        self.describe = describe
        self.status = status
        self.url = url
        self.order = order
        self.type = type
        self.partner_id = partner_id
        self.group_id = parent_id
        self.icon = icon

    def __str__(self):
        return "Authority<{0}, {1}>".format(self.id, self.url)

    __repr__ = __str__
