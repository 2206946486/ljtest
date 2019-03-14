# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/24 
"""
from app import db
from app.tools.dbs import JsonSerializer


class AuthorityGroupRelation(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __json_hidden__ = []

    __tablename__ = 'iot_authority_group_relation'

    __table_args__ = (
        db.UniqueConstraint("group_id", "authority_id", name="uiq_group_auth"),
    )

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.SmallInteger, db.ForeignKey("iot_authority_group.id"), nullable=False, default=0)
    group = db.relationship("AuthorityGroup", backref=db.backref("relation_group", lazy="dynamic"))

    authority_id = db.Column(db.SmallInteger, db.ForeignKey("iot_authority.id"), nullable=False, default=0)
    authority = db.relationship("Authority", backref=db.backref("relation_auth", lazy="dynamic"))

    def __init__(self, group_id, authority_id, *args, **kwargs):
        self.group_id = group_id
        self.authority_id = authority_id

    def __str__(self):
        return "AuthorityGroupRelation<{0}, {1}>".format(self.partner_id, self.amount)

    __repr__ = __str__
