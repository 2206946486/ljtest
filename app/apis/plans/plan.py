# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/11/26 
"""
import logging
from app import db
from schema import Use
from schema import And
from schema import Schema
from schema import Optional
from flask import request
from app.apis.plans import plans
from app.tools.errors import res, State
from app.models.partners.partner import Partner
from app.models.plans.plan import RatePlan
from app.tools.decorators import requires_logged_in


@plans.route("/create", methods=["POST"])
@requires_logged_in()
def create():
    """
    套餐创建
    :return:
    """
    user_id = request.partner.user_id

    req = request.get_json(force=True)
    form = Schema({
        # 来源，多来源逗号隔开
        "source_2": Use(str),
        # 资费类型：0累计套餐，1月套餐，2加油吧，3加速包
        "plan_type": And(Use(int), lambda x: x in [0, 1, 2, 3]),
        # 套餐名称
        "name": And(Use(str), lambda x: x >= 2),
        # 流量
        "ndata": And(Use(float), lambda x: x >= 0),
        # 流量系数
        "dmp": And(Use(int), lambda x: len(x) > 0),
        # 通话时间
        "call_time": And(Use(int), lambda x: x >= 0),
        # 短信
        "meal_message": And(Use(int), lambda x: x >= 0),
        # 有效期
        "day": And(Use(int), lambda x: x >= 0),
        # 市场价格
        "market_price": And(Use(float), lambda x: x > 0),
        # 是否推荐: 0不推荐，1推荐
        "is_recommend": And(Use(int), lambda x: x in [0, 1]),
        # 第三方ID
        "third_id": And(Use(int), lambda x: x >= 0),
        # 套餐单价
        "price": And(Use(float), lambda x: x > 0),
        # 充值次数，-1代表无数次
        "cz_count": And(Use(int), lambda x: x >= -1),
        # 套餐描述
        "describe": And(Use(str)),
        # 下级代理商价格
        "cost_price": And(Use(float), lambda x: x > 0),
        # 套餐组
        "plan_ids": And(Use(str), lambda x: len(x) > 1),
        # 是否指定返利，1是，0否
        "is_back": And(Use(int), lambda x: x in [0, 1]),
        # 返利比例
        Optional("back_persents"): And(Use(int), lambda x: 0 <= x < 100),
        # 父级套餐ID
        Optional("mother_id"): And(Use(int), lambda x: x > 0)
    }).validate(req)

    back_persents = form.get("back_persents", None)
    mother_id = form.get("mother_id", None)

    if form["is_back"] == 1 and back_persents is None:
        return res(state=State.PLAN_BACK_PERSENTS_ERROR)

    if form["cost_price"] < form["price"]:
        return res(state=State.PLAN_COST_PRICE_ERROR)

    partner = Partner.query.filter_by(id=user_id).first()
    if partner.role != 0 and not mother_id:
        logging.error("参数不全: {}".format(req))
        return res(state=State.PARAMS_ERROR)

    if mother_id:
        rp = RatePlan.query.filter_by(id=mother_id).with_entities(RatePlan.id, RatePlan.root_id).first()
        if not rp:
            logging.info("参数错误: {}".format(mother_id))
            return res(state=State.PARAMS_ERROR)
        if rp[1] == 0:
            root_id = rp[0]
        else:
            root_id = rp[1]

        mother_id = mother_id
    else:
        root_id = 0
        mother_id = 0

    if form["type"] == 1:   # 月套餐
        month_data = form["ndata"] * 30 / form["day"]
    else:
        month_data = 0

    rp = RatePlan(name=form["name"], data=form["ndata"], day=form["day"],
                  price=form["price"], partner_id=user_id, month_data=month_data,
                  type=form["type"], market_price=form["market_price"],
                  recommend=form["is_recommend"], third_id=form["third_id"],
                  call_time=form["call_time"], meal_message=form["meal_message"],
                  describe=form["describe"], cost_price=form["cost_price"],
                  mother_id=mother_id, root_id=root_id, dmp=form["dmp"],
                  is_back=form["is_back"], back_persents=back_persents,
                  source_2=form["source_2"], cz_count=form["cz_count"])
    db.session.add(rp)

    # todo 尚未完

    return res()