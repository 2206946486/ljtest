# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""
from flask import jsonify


class State(object):

    FAILURE = 0
    SUCCESS = 1

    # 预留错误: 10001-11000
    ENV_ERROR = 10001
    PARAMS_ERROR = 10002
    SEND_MESSAGE_OFTEN = 10003
    SEND_MESSAGE_ONE_HOUR = 10004
    SEND_MESSAGE_ERROR = 10005
    SMS_ERROR_CODE = 10006
    SMS_HAS_EXPIRED = 10007

    # 代理商/账号错误码: 11001-12000
    PARTNER_NOT_LOGIN = 11001
    PARTNER_NOT_EXISTS = 11002
    PARTNER_LOGIN_ERROR = 11003
    PARTNER_HAS_DISABLED = 11004
    PARTNER_PHONE_HAS_REGISTER = 11005
    PARTNER_PHONE_NOT_REGISTER = 11006
    PARTNER_PWD_ERROR = 11007
    PARTNER_NEW_OLD_PWD_ERROR = 11008
    PARTNER_AUTHORITY_ERROR= 11009
    PARTNER_NICKNAME_EXISTS=11010
    PARTNER_NICKNAME_ERROR=11011
    PARTNER_MOBILE_LENGTH_ERROR=11012

    # 套餐错误码: 12001-13000
    PLAN_NAME_TOO_LONG = 12001
    PLAN_DAY_ERROR = 12002
    PLAN_TYPE_ERROR = 12003
    PLAN_BACK_PERSENTS_ERROR = 12004
    PLAN_COST_PRICE_ERROR = 12005

    # 用户订单错误码: 13001-14000

    # 卡券错误码: 14001-15000

    # 权限错误码: 15001-16000
    ROLE_NOT_EXISTS = 15001
    MENU_NOT_EXISTS = 15002

    err_msg = {
        FAILURE: "操作失败",
        SUCCESS: "操作成功",

        ENV_ERROR: "环境变量有问题, 请检查",
        PARAMS_ERROR: "参数不全或参数不正确",
        SEND_MESSAGE_OFTEN: "发送消息过于频繁，请稍后再试",
        SEND_MESSAGE_ONE_HOUR: "短信1小时内同一手机号发送次数不能超过3次",
        SEND_MESSAGE_ERROR: "消息服务错误",
        SMS_ERROR_CODE: "无效的验证码",
        SMS_HAS_EXPIRED: "验证码已过期",

        PARTNER_NOT_LOGIN: "账号未登录",
        PARTNER_NOT_EXISTS: "账号不存在",
        PARTNER_LOGIN_ERROR: "用户名或密码错误",
        PARTNER_HAS_DISABLED: "账号已经被禁用，请联系管理员",
        PARTNER_PHONE_HAS_REGISTER: "手机号已经注册过了",
        PARTNER_PHONE_NOT_REGISTER: "此手机号未注册过",
        PARTNER_PWD_ERROR: "密码不符合要求，请在6-16之间，并且不能包含特殊字符",
        PARTNER_NEW_OLD_PWD_ERROR: "新旧密码不可一致",
        PARTNER_AUTHORITY_ERROR: "当前账号权限不足",
        PARTNER_NICKNAME_EXISTS: "当前昵称已存在",
        PARTNER_NICKNAME_ERROR: "昵称/账号长度至少为2位",
        PARTNER_MOBILE_LENGTH_ERROR: "手机号只能为11位",

        PLAN_NAME_TOO_LONG: "套餐名字过长",
        PLAN_DAY_ERROR: "套餐有效期有误, 请检查",
        PLAN_TYPE_ERROR: "资费类型有误, 请检查",
        PLAN_BACK_PERSENTS_ERROR: "返利比例不能为空",
        PLAN_COST_PRICE_ERROR: "下级代理商价格不能小于原价",

        ROLE_NOT_EXISTS: "角色不存在",
        MENU_NOT_EXISTS: "节点不存在",
    }


def res(state=State.SUCCESS, data=None, msg=None):
    if not msg:
        msg = State.err_msg.get(state, "未知错误")

    state = state if state == 1 else 0
    return jsonify({"state": state, "data": data, "msg": msg})


class EnvError(Exception):

    def __init__(self, err="环境变量有误"):
        Exception.__init__(self, err)
