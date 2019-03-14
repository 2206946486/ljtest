# -*- coding: utf-8 -*-
"""
@author: cc
@date: 2018/10/23
"""
from .card import CardAuthLossRate
from sqlalchemy import func
from app import db

class CardAuthLossRateService():
    __model__ = CardAuthLossRate

    def find_loss_data(self,partner_id,start_at,end_at):
        # model = self.__model__
        # sql = db.session.query(
        #     func.sum(model.card_query).label("card_query"),
        #     func.sum(model.card_charge).label("card_charge"),
        #     func.sum(model.card_auth).label("card_auth"),
        #     func.sum(model.card_taobao).label("card_taobao"),
        #     func.sum(model.card_complete).label("card_complete")
        # )
        # if partner_id:
        #     sql = sql.filter(model.partner_id==partner_id)
        # else:
        #     sql = sql.filter(db.or_(
        #         model.partner_id == 1,
        #         model.partner_id == 214,
        #         model.partner_id == 620
        #     ))
        # if start_at:
        #     sql = sql.filter(model.created_at>start_at)
        # if end_at:
        #     sql = sql.filter(model.created_at<end_at)
        # # print(sql)
        # return sql.first()
        if partner_id:
            where = "="+str(partner_id)
        else:
            where = "in (1,214,479,620)"
        sql = "select DATE_FORMAT(created_at,'%Y-%m-%d') time ,sum(card_query) card_query,sum(card_charge) card_charge," \
              "sum(card_auth) card_auth,sum(card_taobao) card_taobao,sum(card_complete) card_complete from iot_card_auth_loss_rate" \
              " where created_at>\'"+str(start_at)+"\' and created_at<\'"+str(end_at)+"\'and partner_id "+where+" group by time order by time desc"
        print(sql)
        res = db.session.execute(sql)
        res = res.fetchall()
        return res


    def find_loss_data_detail(self,partner_id,start_at,end_at,limit,offset):
        model = self.__model__
        sql = db.session.query(
            func.sum(model.card_query).label("card_query"),
            func.sum(model.card_charge).label("card_charge"),
            func.sum(model.card_auth).label("card_auth"),
            func.sum(model.card_taobao).label("card_taobao"),
            func.sum(model.card_complete).label("card_complete"),
            model.partner_id, model.partner_name, model.partner_card_auth
        )
        if partner_id:
            sql = sql.filter(model.partner_id==partner_id)
        if start_at:
            sql = sql.filter(model.created_at > start_at)
        if end_at:
            sql = sql.filter(model.created_at < end_at)
        sql = sql.group_by(model.partner_id)
        count = sql.count()
        # print(sql)
        return count,sql.limit(limit).offset(offset).all()