# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/11/27 
"""
from app import db
from datetime import datetime
from app.tools.dbs import JsonSerializer


class RatePlan(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __json_hidden__ = ['card_plans', 'partner_plans', 'card_orders', 'plan_count']

    __tablename__ = "iot_rate_plan"

    id = db.Column(db.Integer, primary_key=True)
    third_id = db.Column(db.Integer, nullable=False)
    source = db.Column(db.Integer)
    partner_id = db.Column(db.Integer, nullable=False, default=0)
    type = db.Column(db.SmallInteger, nullable=False, default=0)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)
    month_data = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    is_recommend = db.Column(db.Boolean(), nullable=False, default=0)
    price = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)
    market_price = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False, default=0)
    into_price = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False, default=0)
    activity_price = db.Column(db.Numeric(10, 3, asdecimal=False),
                               nullable=False, default=0)
    activity_start_at = db.Column(db.DateTime)
    activity_end_at = db.Column(db.DateTime)
    call_time = db.Column(db.Integer, nullable=False, default=0)
    meal_message = db.Column(db.Integer, nullable=False, default=0)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # iot_v1.5新增字段
    describe = db.Column(db.String(255), nullable=True)
    cost_price = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)
    mother_id = db.Column(db.Integer, nullable=False)
    root_id = db.Column(db.Integer, nullable=False)

    # iot_v151新增字段 status=0 在用 ， status>0 移除
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    dmp = db.Column(db.String(5), nullable=False,default=1)#流量系数

    # 是否指定返利
    is_back = db.Column(db.Integer, default=0)
    # 返利比例
    back_persents = db.Column(db.SmallInteger, nullable=True)

    # 来源：替换原来的source，多个源用逗号隔开
    source_2 = db.Column(db.String(20))

    # 可充值次数, -1为无限次
    cz_count = db.Column(db.SmallInteger, nullable=False, default=-1)

    def __init__(self, name, data, day, price, partner_id=0,
                 month_data=0, type=0, market_price=0, is_recommend=False,
                 activity_price=0, activity_start_at=None, third_id=0,
                 activity_end_at=None, is_deleted=False, into_price=0, call_time=0, meal_message=0,
                 created_at=datetime.now(), updated_at=datetime.now(), describe='', cost_price=0,
                 mother_id=0, root_id=0, status=0,dmp=1, is_back=False, back_persents=None, source_2='',
                 cz_count=-1, *args, **kwargs):
        self.third_id = third_id
        self.partner_id = partner_id
        self.type = type
        self.name = name
        self.data = data
        self.month_data = month_data
        self.day = day
        self.is_recommend = is_recommend
        self.price = price
        self.describe = describe
        self.cost_price = cost_price
        self.market_price = market_price
        self.into_price = into_price
        self.activity_price = activity_price
        self.activity_start_at = activity_start_at
        self.activity_end_at = activity_end_at
        self.call_time = call_time
        self.meal_message = meal_message
        self.is_deleted = is_deleted
        self.created_at = created_at
        self.updated_at = updated_at
        self.mother_id = mother_id
        self.root_id = root_id
        self.status = status
        self.dmp = dmp
        self.is_back = is_back
        self.back_persents = back_persents
        self.source_2 = source_2
        self.cz_count = cz_count