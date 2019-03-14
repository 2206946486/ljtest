# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""

from app import db
from datetime import datetime
from app.tools.dbs import JsonSerializer


class Partner(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __json_hidden__ = ['partner_cards', 'partner_plans', 'partner_amounts', 'addresses', 'partner_invoices',
                       'card_orders']

    __tablename__ = 'iot_partner'

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=False, default=0)
    app_id = db.Column(db.String(20))
    app_key = db.Column(db.String(32))
    openid = db.Column(db.String(64))
    mobile = db.Column(db.String(20), nullable=False, unique=True)
    nickname = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    avatar = db.Column(db.String(100))
    realname = db.Column(db.String(50))
    id_no = db.Column(db.String(30))
    name = db.Column(db.String(20))
    copyright = db.Column(db.String(100))
    total_amount = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)
    amount = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)
    role = db.Column(db.SmallInteger, nullable=False, default=0)
    draw_type = db.Column(db.SmallInteger, nullable=False, default=0)
    draw_value = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    # 移动端购卡需求
    is_must_plan = db.Column(db.SmallInteger, nullable=False, default=0)  # 购卡时是否必须带套餐，1为必须，0为非必须
    card_price = db.Column(db.SmallInteger, nullable=False, default=5)  # 卡价格

    # 创建账户（权限需求，区分账户和代理商）
    type = db.Column(db.SmallInteger, default=0)

    roles = db.Column(db.String(255))

    # 代理商实名方式
    need_auth = db.Column(db.SmallInteger, nullable=False, default=1)  # 实名方式

    partner_fare = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False, default=0)  # 费率

    # 折扣(0-100)
    discount = db.Column(db.SmallInteger, nullable=True)
    # 最大欠款(最大100000)
    max_debt = db.Column(db.Integer, nullable=True)
    notice = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, mobile, nickname, password, type, roles=None, app_id=None,
                 app_key=None, role=0, realname=None, total_amount=0, amount=0,
                 draw_type=0, draw_value=0, name=None, copyright=None,
                 id_no=None, pid=0, openid=None, avatar=None, status=0,
                 card_price=5, is_must_plan=0, need_auth=1, partner_fare=0,
                 discount=None, max_debt=None, notice=0,
                 created_at=datetime.now(), updated_at=datetime.now(),
                 *args, **kwargs):
        self.pid = pid
        self.app_id = app_id
        self.app_key = app_key
        self.openid = openid
        self.mobile = mobile
        self.nickname = nickname
        self.password = password
        self.avatar = avatar
        self.realname = realname
        self.total_amount = total_amount
        self.amount = amount
        self.id_no = id_no
        self.name = name
        self.copyright = copyright
        self.role = role
        self.status = status
        self.draw_type = draw_type
        self.draw_value = draw_value
        self.is_must_plan = is_must_plan
        self.card_price = card_price
        self.created_at = created_at
        self.updated_at = updated_at
        self.type = type
        self.roles = roles
        self.need_auth = need_auth
        self.partner_fare = partner_fare

        self.discount = discount
        self.max_debt = max_debt
        self.notice = notice

    def __str__(self):
        return "Partner<{0}, {1}>".format(self.id, self.mobile)

    __repr__ = __str__
