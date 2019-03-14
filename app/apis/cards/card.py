# -*- coding: UTF-8 -*-
"""
@author: cc
@date: 2018/10/23
"""

from flask import request
from app.apis.cards import cards
from app.tools.decorators import requires_logged_in
from app.models.cards import CardAuthLossRateService
from app.tools.cards import get_card_loss_rate
from app.tools.errors import res, State
import datetime

@cards.route("/cards_auth_loss", methods=["POST"])
@requires_logged_in()
def cards_auth_loss():
    """
    实名流失率访问量统计
    :param partner_id: 代理商id，不选默认为0查所有
    :return:
    """
    user = request.partner.partner
    data = request.get_json()
    # data = request.form.to_dict()
    partner_id = data.get('partner_id',0)
    calrs = CardAuthLossRateService()

    # if not int(partner_id):
    #     user_id = user.correctid if user.role else 0
    # else:
    #     user_id = partner_id
    #
    # if int(user_id) in [1,214,620]:
    #     user_id = 0
    # 当前时间
    now = datetime.datetime.now()
    # 获取今天零点
    now_start_at = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                        microseconds=now.microsecond)
    # 获取23:59:59
    now_end_at = now_start_at + datetime.timedelta(hours=23, minutes=59, seconds=59)
    # 今天实名流失率查询
    # res_now = calrs.find_loss_data(int(partner_id), now_start_at, now_end_at)

    #昨天实名流失率查询
    yester_start_at = now_start_at - datetime.timedelta(days=1)
    yester_end_at = now_end_at - datetime.timedelta(days=1)
    res_data = calrs.find_loss_data(int(partner_id), yester_start_at, now_end_at)
    # print now, yester_start_at, yester_end_at

    if not res_data:
        return res(data=dict())
    loss_rate = get_card_loss_rate(res_data[0],res_data[1])
    # print(loss_rate)
    return res(data=loss_rate)

@cards.route("/cards_auth_loss_trend", methods=["GET"])
@requires_logged_in()
def cards_auth_loss_trend():
    """
    实名流失率访问量趋势图
    :param start_at: 开始时间
    :param end_at: 结束时间
    :param partner_id: 代理商id，不选默认为0查所有
    :return:
    """
    user = request.partner.partner
    data = request.get_json()
    start_at = data.get('start_at', None)
    end_at = data.get('end_at', None)
    partner_id = data.get('partner_id', 0)
    calrs = CardAuthLossRateService()

    # 将时间进行处理
    if not start_at and end_at:
        start_at = '2000-01-01 00:00:00'
        end_at = '2099-01-01 00:00:00'
    elif not start_at:
        start_at = '2000-01-01 00:00:00'
    elif not end_at:
        start_at = '2018-01-01 00:00:00'

    rows = calrs.find_loss_data(int(partner_id), start_at, end_at)
    return res(data={"rows": rows})

@cards.route("/cards_auth_loss_deail", methods=["POST"])
@requires_logged_in()
def cards_auth_loss_deail():
    """
    实名流失率访问量详情
    :param start_at: 开始时间
    :param end_at: 结束时间
    :param offset: 页码
    :param limit: 数量
    :param partner_id: 代理商id，不选默认为0查所有
    :return:
    """
    user = request.partner.partner
    data = request.get_json()
    # data = request.form.to_dict()
    start_at = data.get('start_at', None)
    end_at = data.get('end_at', None)
    partner_id = data.get('partner_id', 0)
    limit = data.get('limit', 25)
    offset = data.get('offset', 0)
    calrs = CardAuthLossRateService()

    count, resps = calrs.find_loss_data_detail(int(partner_id), start_at, end_at, limit, offset)
    rows = []
    for r in resps:
        rep = dict()
        rep['card_query'] = str(r.card_query)
        rep['card_charge'] = str(r.card_charge)
        rep['card_charge_loss'] = str(r.card_query-r.card_charge)
        rep['card_charge_loss_rate'] = str((r.card_query-r.card_charge)/r.card_query)

        rep['card_auth'] = str(r.card_auth)
        rep['card_auth_loss'] = str(r.card_charge - r.card_auth)
        rep['card_auth_loss_rate'] = str((r.card_charge - r.card_auth) / r.card_charge)

        rep['card_taobao'] = str(r.card_taobao)
        rep['card_taobao_loss'] = str(r.card_auth - r.card_taobao)
        rep['card_taobao_loss_rate'] = str((r.card_auth - r.card_taobao) / r.card_auth)

        rep['card_complete'] = str(r.card_complete)
        rep['card_complete_loss'] = str(r.card_taobao - r.card_complete)
        rep['card_complete_loss_rate'] = str((r.card_taobao - r.card_complete) / r.card_taobao)
        rep['partner_name'] = r.partner_name
        rows.append(rep)

    return res(data={"rows": rows, "total": count})