# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/22 
"""

from app import db
from flask import request
from collections import defaultdict
from app.tools.errors import res, State
from app.apis.authorities import authorities
from app.models.partners.partner import Partner
from app.tools.decorators import requires_logged_in
from app.models.authorities.authority import Authority
from app.models.authorities.authority_role import AuthorityRole
from app.models.authorities.authority_group import AuthorityGroup
from app.models.authorities.authority_role_relation import AuthorityRoleRelation


@authorities.route("/role_list")
@requires_logged_in()
def role_list():
    """
    角色列表
    :return:
    """
    partner = request.partner.partner
    partner_id = partner.id

    p = Partner.query.filter_by(id=partner_id).with_entities(Partner.type, Partner.pid).first()
    if not p:
        return res(state=State.PARTNER_NOT_EXISTS)

    correct_id = p[1] if p[0] == 1 else partner_id
    data = AuthorityRole.query.filter_by(partner_id=correct_id).with_entities(AuthorityRole.id,
                                                                              AuthorityRole.name,
                                                                              AuthorityRole.describe).all()
    result = list()
    for item in data:
        authority_role_id, name, describe = item

        count = 0

        partners = Partner.query.filter(
            Partner.roles.like('%' + str(authority_role_id) + '%')).with_entities(Partner.roles).all()
        for p in partners:
            partner_roles, = p
            role_ids = partner_roles.split(',')
            for role_id in role_ids:
                if int(role_id) == authority_role_id:
                    count = count + 1

        result.append({
            "authority_role_id": authority_role_id,
            "name": name,
            "describe": describe,
            "role_partners": count
        })

    return res(data=result)


@authorities.route("/add_role", methods=["POST"])
@requires_logged_in()
def add_role():
    """
    添加角色
    :return: 
    """
    partner = request.partner.partner
    partner_id = partner.id

    req = request.get_json(force=True)
    # 角色名称
    name = req.get("name", None)
    # 描述
    describe = req.get("describe", None)

    if not name or not describe:
        return res(State.PARAMS_ERROR)

    ar = AuthorityRole(name=name, describe=describe, partner_id=partner_id, type=0, status=0)
    db.session.add(ar)
    db.session.commit()
    return res()


@authorities.route("/update_role", methods=["POST"])
@requires_logged_in()
def update_role():
    """
    更新角色
    :return:
    """
    req = request.get_json(force=True)
    # 角色ID
    authority_role_id = req.get("authority_role_id", None)
    # 角色名称
    name = req.get("name", None)
    # 描述
    describe = req.get("describe", None)

    if not authority_role_id or not name or not describe:
        return res(state=State.PARAMS_ERROR)

    ar = AuthorityRole.query.filter_by(id=authority_role_id).first()
    if not ar:
        return res(state=State.ROLE_NOT_EXISTS)

    ar.name = name
    ar.describe = describe

    db.session.add(ar)
    db.session.commit()

    return res()


@authorities.route("/del_role", methods=["POST"])
@requires_logged_in()
def del_role():
    """
    删除角色
    :return:
    """
    req = request.get_json(force=True)
    # 角色ID
    authority_role_id = req.get("authority_role_id", None)

    if not authority_role_id:
        return res(state=State.PARAMS_ERROR)

    data = AuthorityRole.query.filter_by(id=authority_role_id).with_entities(AuthorityRole.id).first()
    if not data:
        return res(state=State.ROLE_NOT_EXISTS)

    count = 0
    partners = Partner.query.filter(
        Partner.roles.like('%' + str(authority_role_id) + '%')).with_entities(Partner.roles).all()

    for p in partners:
        partner_roles, = p
        role_ids = partner_roles.split(',')
        for role_id in role_ids:
            if int(role_id) == authority_role_id:
                count = count + 1

    if count > 0:
        return res(state=State.FAILURE, msg="删除失败，此角色还有{count}个用户使用".format(count=count))

    AuthorityRoleRelation.query.filter_by(role_id=authority_role_id).delete()
    AuthorityRole.query.filter_by(id=authority_role_id).delete()
    db.session.commit()
    return res()


@authorities.route("/get_auth_by_role_id")
@requires_logged_in()
def get_auth_by_role_id():
    """
    根据角色ID获取权限列表
    :return:
    """
    # 角色ID
    role_id = request.args.get("role_id", None)
    if not role_id:
        return res(state=State.PARAMS_ERROR)

    role_id = int(role_id)

    data = AuthorityRoleRelation.query.filter_by(role_id=role_id)\
                                      .with_entities(AuthorityRoleRelation.authority_id,
                                                     AuthorityRoleRelation.parent_auth_id)\
                                      .all()
    parent_auth_id_list, authority_id_list = list(), list()
    for item in data:
        authority_id, parent_auth_id = item
        authority_id_list.append(authority_id)
        parent_auth_id_list.append(parent_auth_id)

    result = list()
    parent_auth_data = AuthorityGroup.query.filter(AuthorityGroup.id.in_(parent_auth_id_list))\
                                           .with_entities(AuthorityGroup.id, AuthorityGroup.group_name).all()
    for item in parent_auth_data:
        group_id, group_name = item
        result.append({
            "group_id": group_id,
            "group_name": group_name
        })

    authority_data = Authority.query.filter(Authority.id.in_(authority_id_list))\
                                    .with_entities(Authority.id, Authority.group_id, Authority.name).all()
    info = defaultdict(list)
    for item in authority_data:
        authority_id, group_id, name = item
        info[group_id].append({
            "authority_id": authority_id,
            "authority_name": name
        })

    for item in result:
        sub = info.get(item["group_id"], [])
        item["sub"] = sub

    return res(data=result)


@authorities.route("/update_auth_by_role_id", methods=["POST"])
@requires_logged_in()
def update_auth_by_role_id():
    """
    根据角色ID更新权限
    :return:
    """
    req = request.get_json(force=True)
    # 角色ID
    role_id = req.get("role_id", None)
    # 父节点列表
    parent_auth_id_list = req.get("parent_auth_id_list", None)
    # 子节点列表
    child_auth_id_list = req.get("child_auth_id_list", None)

    if not role_id or not parent_auth_id_list or not child_auth_id_list:
        return res(state=State.PARAMS_ERROR)

    AuthorityRoleRelation.query.filter_by(role_id=role_id).delete()

    for parent_auth_id in parent_auth_id_list:
        arr = AuthorityRoleRelation(role_id=role_id, parent_auth_id=parent_auth_id)
        db.session.add(arr)

    for child_auth_id in child_auth_id_list:
        arr = AuthorityRoleRelation(role_id=role_id, authority_id=child_auth_id)
        db.session.add(arr)

    db.session.commit()
    return res()
