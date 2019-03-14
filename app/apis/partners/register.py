# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/19 
"""
import time
import random
from app import db
from flask import request
from app.tools.sms.tools import YunMessage
from app.tools.errors import State, res
from app.apis.partners import partners
from app.models.partners.register import Register
from app.models.partners.partner import Partner
from app.tools.decorators import requires_logged_in
from app.tools.sms.tools import get_messages, set_messages
from app.tools.utils import checkdata, Security


@partners.route("/sms", methods=["POST"])
@requires_logged_in()
def sms():
    """
    发送验证码
    :return:
    """
    req = request.get_json(force=True)
    # 手机号码
    phone = req.get('phone', None)
    # 状态
    status = req.get('status', None)
    if not phone or not status:
        return res(state=State.PARAMS_ERROR)

    if status == 1:
        data = Register.query.filter_by(telphone=phone).with_entities(Register.id).first()
        if data:
            return res(state=State.PARTNER_PHONE_HAS_REGISTER)
    elif status == 2:
        data = Partner.query.filter_by(mobile=phone).with_entities(Partner.id).first()
        if not data:
            return res(state=State.PARTNER_PHONE_NOT_REGISTER)

    ym = YunMessage()
    msg = get_messages(mobile=phone)
    now = time.time()
    if msg:
        if now < msg['again']:
            return res(state=State.SEND_MESSAGE_OFTEN)
        if 'htime' not in msg.keys():
            msg['htime'] = now + 3600
            msg['count'] = 0
        if now < msg['htime']:
            if msg['count'] >= 3:
                return res(state=State.SEND_MESSAGE_ONE_HOUR)
        else:
            msg['count'] = 0
            msg['htime'] = now + 3600

    else:
        msg = dict()
        msg['count'] = 0
        msg['htime'] = now + 3600

    code = random.randint(1000, 9999)  # 生成随即验证码Ó
    data = ym.send_code(phone, code)
    if not data:
        raise res(state=State.SEND_MESSAGE_ERROR)
    count = msg['count'] + 1

    msg['code'] = code
    msg['again'] = now + 120
    msg['expired'] = now + 600
    msg['count'] = count
    set_messages(phone, msg)

    return res()


@partners.route("/reset_pwd", methods=["POST"])
@requires_logged_in()
def reset_pwd():
    """
    忘记密码
    :return:
    """
    req = request.get_json(force=True)
    # 密码
    password = req.get("password", None)
    # 手机号
    phone = req.get("phone", None)
    # 验证码
    code = req.get("verify", None)

    if not password or not phone or not code:
        return res(state=State.PARAMS_ERROR)

    msg = get_messages(phone)
    if not msg['code']:
        return res(state=State.SMS_ERROR_CODE)

    if msg["code"] != code:
        return res(state=State.SMS_ERROR_CODE)

    if time.time() > msg["expired"]:
        return res(state=State.SMS_HAS_EXPIRED)

    if not checkdata(password):
        return res(state=State.PARTNER_PWD_ERROR)

    info = Partner.query.filter_by(phone=phone).first()
    if not info:
        return res(state=State.PARTNER_NOT_EXISTS)

    pwd = Security()(password)
    if pwd == info.password:
        return res(state=State.PARTNER_NEW_OLD_PWD_ERROR)

    info.password = pwd
    db.session.add(info)
    db.session.commit()

    msg['code'] = ''
    set_messages(phone, msg)
    return res()
