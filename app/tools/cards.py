# -*- coding: UTF-8 -*-
"""
@author: cc
@date: 2018/10/23
"""

def get_card_loss_rate(res_now,res_yester):
    # 今天流失率统计
    now_card_query_rate = 0
    now_card_charge_rate = (res_now.card_query - res_now.card_charge) / res_now.card_query
    now_card_auth_rate = (res_now.card_charge - res_now.card_auth) / res_now.card_charge
    now_card_taobao_rate = (res_now.card_auth - res_now.card_taobao) / res_now.card_auth
    now_card_complete_rate = (res_now.card_taobao - res_now.card_complete) / res_now.card_taobao
    # 昨天流失率统计
    yes_card_query_rate = 0
    yes_card_charge_rate = (res_yester.card_query - res_yester.card_charge) / res_yester.card_query
    yes_card_auth_rate = (res_yester.card_charge - res_yester.card_auth) / res_yester.card_charge
    yes_card_taobao_rate = (res_yester.card_auth - res_yester.card_taobao) / res_yester.card_auth
    yes_card_complete_rate = (res_yester.card_taobao - res_yester.card_complete) / res_yester.card_taobao

    card_query = dict(amount=str(res_now.card_query), loss_amount=0, card_loss_rate=0, rate_contrast=0)
    card_charge = dict(amount=str(res_now.card_charge), loss_amount=str(res_now.card_query - res_now.card_charge),card_loss_rate=str(now_card_charge_rate), rate_contrast=str(now_card_charge_rate - yes_card_charge_rate))
    card_auth = dict(amount=str(res_now.card_auth), loss_amount=str(res_now.card_charge - res_now.card_auth),card_loss_rate=str(now_card_auth_rate), rate_contrast=str(now_card_auth_rate - yes_card_auth_rate))
    card_taobao = dict(amount=str(res_now.card_taobao), loss_amount=str(res_now.card_auth - res_now.card_taobao),card_loss_rate=str(now_card_taobao_rate), rate_contrast=str(now_card_taobao_rate - yes_card_taobao_rate))
    card_complete = dict(amount=str(res_now.card_complete), loss_amount=str(res_now.card_taobao - res_now.card_complete),card_loss_rate=str(now_card_complete_rate),rate_contrast=str(now_card_complete_rate - yes_card_complete_rate))
    return dict(card_query=card_query, card_charge=card_charge, card_auth=card_auth, card_taobao=card_taobao,card_complete=card_complete)
