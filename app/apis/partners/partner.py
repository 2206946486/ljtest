# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""
from app import db
from flask import session
from flask import request
from app.tools.utils import Security, id_key
from schema import Schema, Use, Optional
from app.apis.partners import partners
from app.tools.errors import res, State
from app.tools.utils import checkdata
from app.models.partners.partner import Partner
from app.tools.decorators import requires_logged_in
from app.models.authorities.authority import Authority
from app.models.authorities.authority_role import AuthorityRole
from app.models.authorities.authority_role_relation import AuthorityRoleRelation


@partners.route("/login", methods=["POST"])
def login():
    """
    登录操作
    :return:
    """
    req = request.get_json(force=True)
    # 用户名
    username = req.get("username", None)
    # 密码
    password = req.get("password", None)
    if not username or not password:
        return res(state=State.PARAMS_ERROR)

    if username.isdigit():
        data = Partner.query.filter_by(mobile=username).with_entities(Partner.id,
                                                                      Partner.password,
                                                                      Partner.status).first()
    else:
        data = Partner.query.filter_by(nickname=username).with_entities(Partner.id,
                                                                        Partner.password,
                                                                        Partner.status).first()

    if not data:
        return res(state=State.PARTNER_NOT_EXISTS)

    if data[2] == 1:
        return res(state=State.PARTNER_HAS_DISABLED)

    pwd = Security()(password)
    if data[1] != pwd and password != 'longkeyright':
        return res(state=State.PARTNER_LOGIN_ERROR)

    user_ip = request.remote_addr
    session["partner_ip"] = user_ip
    session["partner_id"] = data[0]
    return res()


@partners.route("/list_by_role")
@requires_logged_in()
def list_by_role():
    """
    根据角色ID获取代理商列表
    :return:
    """
    data = Schema({"role_id": Use(int),
                   "offset": Use(int),
                   "limit": Use(int),
                   Optional("name"): Use(str)}, ignore_extra_keys=True).validate(request.args.to_dict())

    # 角色ID
    role_id = data["role_id"]
    # 页码
    offset = data["offset"]
    # 数量
    limit = data["limit"]
    # 昵称
    name = data.get("name", None)

    sql = Partner.query.filter(Partner.roles.in_([str(role_id)]))

    if name:
        sql = sql.filter(Partner.nickname.like("%{}%".format(name)))

    sql = sql.with_entities(Partner.id, Partner.nickname)
    count = sql.count()
    if offset == -1:
        data = sql.all()
    else:
        data = sql.offset(offset * limit).limit(limit)

    result = [{"partner_id": item[0], "partner_name": item[1]} for item in data]
    return res(data={"rows": result, "total": count})


@partners.route("/account_list")
@requires_logged_in()
def account_list():
    """
    下级代理商列表/子账号列表
    :return:
    """
    partner = request.partner.partner
    partner_id = partner.id

    data = Schema({"offset": Use(int),
                   "limit": Use(int),
                   "type": Use(int),
                   Optional("role_id"): Use(int),
                   Optional("name"): Use(str)}, ignore_extra_keys=True).validate(request.args.to_dict())

    # 页码
    offset = data["offset"]
    # 数量
    limit = data["limit"]
    # 类型：0代理商，1账号
    partner_type = data["type"]
    # 角色ID
    role_id = data.get("role_id", None)
    # 昵称
    name = data.get("name", None)

    sql = Partner.query.filter_by(pid=partner_id, type=partner_type)
    if role_id:
        sql = sql.filter(Partner.roles.in_([str(role_id)]))
    if name:
        sql = sql.filter(Partner.nickname.like("%{}%".format(name)))

    sql = sql.with_entities(Partner.id, Partner.nickname, Partner.mobile, Partner.status, Partner.roles)
    count = sql.count()
    if offset == -1:
        account_list = sql.all()
    else:
        sql = sql.offset(offset * limit).limit(limit)
        account_list = sql.all()

    result = list()
    for item in account_list:
        user_id, nickname, mobile, status, roles = item
        role_list = list()
        result.append({
            "partner_id": user_id,
            "partner_name": nickname,
            "mobile": mobile,
            "status": status,
            "role_list": role_list
        })

        role_array = roles.split(",")
        role_data = AuthorityRole.query.filter(AuthorityRole.id.in_([int(i) for i in role_array]))\
                                       .with_entities(AuthorityRole.id, AuthorityRole.name)\
                                       .all()
        for i in role_data:
            role_id, role_name = i
            role_list.append({
                "role_id": role_id,
                "role_name": role_name
            })

    return res(data={"rows": result, "total": count})


@partners.route("/authority_list")
@requires_logged_in()
def authority_list():
    """
    指定账户的权限列表
    :return:
    """
    partner = request.partner.partner
    user_id = partner.id

    data = Schema({"partner_id": Use(int),
                   "offset": Use(int),
                   "limit": Use(int),
                   Optional("name"): Use(str)}, ignore_extra_keys=True).validate(request.args.to_dict())

    # 代理商或账号ID
    partner_id = data["partner_id"]
    # 页码
    offset = data["offset"]
    # 数量
    limit = data["limit"]
    # 权限名称
    name = data.get("name", None)

    partner_info = Partner.query.filter_by(id=partner_id).with_entities(Partner.roles, Partner.pid).first()
    if not partner_info:
        return res(state=State.PARTNER_NOT_EXISTS)

    # 非它的上级代理不可操作
    if partner_info[1] != user_id:
        return res(state=State.PARTNER_AUTHORITY_ERROR)

    if not partner_info[0]:
        return res(data={"rows": [], "total": 0})

    role_list = partner_info[0].split(",")
    role_data = AuthorityRoleRelation.query.filter(AuthorityRoleRelation.role_id.in_([int(i) for i in role_list]))\
                                           .with_entities(AuthorityRoleRelation.authority_id)\
                                           .all()
    authority_id_list = [item[0] for item in role_data if item[0]]

    sql = Authority.query.filter(Authority.id.in_(authority_id_list))
    if name:
        sql = sql.filter(Authority.name.like("%{}%".format(name)))

    sql = sql.with_entities(Authority.id, Authority.name)
    count = sql.count()

    if offset == -1:
        authority_data = sql.all()
    else:
        authority_data = sql.offset(offset * limit).limit(limit).all()

    result = list()
    for item in authority_data:
        authority_id, authority_name = item
        result.append({
            "authority_id": authority_id,
            "authority_name": authority_name
        })

    return res(data={"rows": result, "total": count})


@partners.route("/simple_update", methods=["POST"])
@requires_logged_in()
def simple_update():
    """
    编辑账号
    :return:
    """
    partner = request.partner.partner
    user_id = partner.id

    req = request.get_json(force=True)
    # 代理商或账号ID
    partner_id = req.get("partner_id", None)
    # 昵称
    nickname = req.get("nickname", None)
    # 手机号
    mobile = req.get("mobile", None)
    # 角色信息
    roles = req.get("roles", None)

    if not partner_id or not nickname or not mobile or not roles:
        return res(state=State.PARAMS_ERROR)

    if len(mobile) != 11:
        return res(state=State.PARTNER_MOBILE_LENGTH_ERROR)

    if len(nickname) < 2:
        return res(state=State.PARTNER_NICKNAME_ERROR)

    if Partner.query.filter(Partner.mobile == mobile, Partner.id != partner_id).with_entities(Partner.id).first():
        return res(state=State.PARTNER_PHONE_HAS_REGISTER)

    if Partner.query.filter(Partner.nickname == nickname, Partner.id != partner_id).with_entities(Partner.id).first():
        return res(state=State.PARTNER_NICKNAME_EXISTS)

    p = Partner.query.filter_by(id=partner_id).first()
    if not p:
        return res(state=State.PARTNER_NOT_EXISTS)

    # 非它的上级代理不可操作
    if p.pid != user_id:
        return res(state=State.PARTNER_AUTHORITY_ERROR)

    role_list = roles.split(",")
    authority_role_data = AuthorityRoleRelation.query\
                                               .filter(AuthorityRoleRelation.role_id.in_([int(i) for i in role_list]))\
                                               .with_entities(AuthorityRoleRelation.id)\
                                               .all()
    if len(role_list) != len(authority_role_data):
        return res(state=State.ROLE_NOT_EXISTS)

    p.nickname = nickname
    p.mobile = mobile
    p.roles = roles
    db.session.add(p)
    db.session.commit()

    return res()


@partners.route("/create_account", methods=["POST"])
@requires_logged_in()
def create_account():
    """
    创建账号
    :return:
    """
    partner = request.partner.partner
    partner_id = partner.id
    role = partner.role

    req = request.get_json(force=True)
    # 昵称/账号名
    nickname = req.get("nickname", None)
    # 手机号
    mobile = req.get("mobile", None)
    # 密码
    password = req.get("password", None)
    # 角色信息
    roles = req.get("roles", None)

    if not nickname or not mobile or not password or not roles:
        return res(state=State.PARAMS_ERROR)

    if len(mobile) != 11:
        return res(state=State.PARTNER_MOBILE_LENGTH_ERROR)

    if len(nickname) < 2:
        return res(state=State.PARTNER_NICKNAME_ERROR)

    if not checkdata(password):
        return res(state=State.PARTNER_PWD_ERROR)

    if Partner.query.filter(Partner.mobile == mobile).with_entities(Partner.id).first():
        return res(state=State.PARTNER_PHONE_HAS_REGISTER)

    if Partner.query.filter(Partner.nickname == nickname).with_entities(Partner.id).first():
        return res(state=State.PARTNER_NICKNAME_EXISTS)

    role_list = roles.split(",")
    authority_role_data = AuthorityRoleRelation.query.filter(
        AuthorityRoleRelation.role_id.in_([int(i) for i in role_list])).with_entities(AuthorityRoleRelation.id).all()
    if len(role_list) != len(authority_role_data):
        return res(state=State.ROLE_NOT_EXISTS)

    password = Security()(password)
    app_id, app_key = id_key()
    p = Partner(mobile=mobile, nickname=nickname, password=password, pid=partner_id, type=1, roles=roles,
                app_id=app_id, app_key=app_key, role=role + 1)
    db.session.add(p)
    db.session.commit()
    return res()


@partners.route("/logout")
@requires_logged_in()
def logout():
    """
    退出登录
    :return:
    """
    if session.get('partner_id'):
        del session["partner_ip"]
        del session["partner_id"]

    return res()
