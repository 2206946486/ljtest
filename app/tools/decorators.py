# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""
import os
from flask import request
from flask import session
from functools import wraps
from app.tools.errors import res, State
from app.models.partners.partner import Partner


class PartnerInfo(object):
    partner_id = 0
    partner_ip = ""
    user_id = 0
    partner = {}


def requires_logged_in(is_top_partner=False):
    """
    登录判断装饰器
    :param is_top_partner: 是否需要顶级代理商权限
    :return:
    """
    def wrapper(func):

        @wraps(func)
        def sub_wrapper(*args, **kwargs):
            if not hasattr(request, "partner"):
                partner_data = PartnerInfo()
                setattr(request, "partner", partner_data)

            partner_data = getattr(request, "partner")
            partner_id = session.get("partner_id")

            env = os.environ.get("MODE", "")
            partner_id = 1 if env == "LOCAL" else partner_id

            if partner_id:
                partner_data.partner_id = partner_id
                partner_data.partner_ip = session.get("partner_ip")
                partner_data.partner = Partner.query.filter_by(id=partner_id).first()
                partner_data.user_id = partner_data.partner.pid if partner_data.partner.type == 1 else partner_id
                if partner_data.partner.role != 0 and is_top_partner:
                    return res(state=State.PARTNER_AUTHORITY_ERROR)

                return func(*args, **kwargs)

            return res(state=State.PARTNER_NOT_LOGIN)

        return sub_wrapper

    return wrapper
