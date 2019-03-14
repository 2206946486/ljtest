# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/22 
"""

from app import db
from app.tools.dbs import JsonSerializer


class AuthorityRole(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __json_hidden__ = ["relation_group"]

    __tablename__ = 'iot_authority_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    describe = db.Column(db.String(255))
    type = db.Column(db.SmallInteger)
    partner_id = db.Column(db.SmallInteger)
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    def __init__(self, name, describe, partner_id, type=0, status=0, *args, **kwargs):
        self.name = name
        self.describe = describe
        self.status = status
        self.type = type
        self.partner_id = partner_id
