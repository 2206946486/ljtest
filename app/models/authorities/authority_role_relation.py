# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/23 
"""

from app import db
from app.tools.dbs import JsonSerializer


class AuthorityRoleRelation(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __json_hidden__ = ["relation_group"]

    __tablename__ = 'iot_authority_role_relation'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    authority_id = db.Column(db.Integer)
    parent_auth_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    def __str__(self):
        return "AuthorityRoleRelation<{0}, {1}>".format(self.role_id, self.authority_id)

    def __init__(self, role_id, authority_id=None, parent_auth_id=None, status=0, *args, **kwargs):
        self.status = status
        self.role_id = role_id
        self.authority_id = authority_id
        self.status = status
        self.parent_auth_id = parent_auth_id