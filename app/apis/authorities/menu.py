# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/23 
"""
from app import db
from flask import request
from collections import defaultdict
from app.apis.authorities import authorities
from app.tools.errors import res, State
from app.tools.decorators import requires_logged_in
from app.models.authorities.authority import Authority
from app.models.authorities.authority_group import AuthorityGroup
from app.models.authorities.authority_role_relation import AuthorityRoleRelation
from app.models.authorities.authority_group_relation import AuthorityGroupRelation


@authorities.route("/menu_list")
@requires_logged_in(is_top_partner=True)
def menu_list():
    """
    菜单列表
    :return:
    """
    data = AuthorityGroup.query.filter_by(type=0)\
                               .with_entities(AuthorityGroup.id,
                                              AuthorityGroup.group_name)\
                               .all()
    result = [{"group_id": item[0], "group_name": item[1]} for item in data]

    authority_data = Authority.query.filter(Authority.group_id.in_([item["group_id"] for item in result])) \
                                    .with_entities(Authority.id,
                                                   Authority.group_id,
                                                   Authority.name)\
                                    .all()
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


@authorities.route("/add_menu", methods=["POST"])
@requires_logged_in(is_top_partner=True)
def add_menu():
    """
    添加菜单
    :return:
    """
    partner = request.partner.partner
    partner_id = partner.id

    req = request.get_json(force=True)
    # 节点名称
    name = req.get("name", None)
    # 节点地址
    url = req.get("url", None)
    # 节点排序
    order = req.get("order", None)
    # 节点图标
    icon = req.get("icon", None)
    # 是否菜单：0 菜单 1 非菜单
    menu_type = req.get("type", None)
    # 层级：0 主节点 1 子节点
    level = req.get('level', None)
    # 状态 0 开启 1 关闭
    status = req.get('status', None)
    # 父节点ID
    parent_id = req.get("parent_id", None)

    if not name or not url or order is None or not icon \
            or menu_type is None or level is None or status is None:
        return res(state=State.PARAMS_ERROR)

    if level == 1 and not parent_id:    # 子节点情况需传递父节点ID
        return res(state=State.PARAMS_ERROR)

    if level == 0:  # 主节点
        all_group = AuthorityGroup.query.filter_by(type=0).all()
        group_len = len(all_group)
        if order < 1:
            for item in all_group:
                item.order += 1
                db.session.add(item)

            order = 1
        elif order >= group_len:
            order = group_len + 1
        elif 1 <= order < group_len:
            for item in all_group:
                if item.order >= order:
                    item.order += 1
                    db.session.add(item)

        ag = AuthorityGroup(name=name, describe="", partner_id=partner_id, icon=icon,
                            url=url, type=menu_type, order=order, status=status)
        db.session.add(ag)
        db.session.commit()
    else:
        all_auth = Authority.query.filter_by(group_id=partner_id).all()
        auth_len = len(all_auth)
        if order < 1:
            for a in all_auth:
                a.order += 1
                db.session.add(a)
            order = 1
        elif order >= auth_len:
            order = auth_len + 1
        elif 1 <= order < auth_len:
            for a in all_auth:
                if a.order >= order:
                    a.order += 1
                    db.session.add(a)

        a = Authority(name=name, describe="", icon=icon, parent_id=parent_id, partner_id=partner_id,
                      url=url, type=menu_type, order=order, status=status)
        db.session.add(a)
        db.session.commit()

        agr = AuthorityGroupRelation(group_id=parent_id, authority_id=a.id)
        db.session.add(agr)
        db.session.commit()

    return res()


@authorities.route("/update_menu", methods=["POST"])
@requires_logged_in(is_top_partner=True)
def update_menu():
    """
    更新菜单
    :return:
    """
    req = request.get_json(force=True)
    # 节点ID
    menu_id = req.get("menu_id", None)
    # 节点名称
    name = req.get("name", None)
    # 节点地址
    url = req.get("url", None)
    # 节点排序
    order = req.get("order", None)
    # 节点图标
    icon = req.get("icon", None)
    # 是否菜单：0 菜单 1 非菜单
    menu_type = req.get("type", None)
    # 层级：0 主节点 1 子节点
    level = req.get('level', None)
    # 状态 0 开启 1 关闭
    status = req.get('status', None)
    # 父节点ID
    parent_id = req.get("parent_id", None)

    if not menu_id or not name or not url or order is None \
            or not icon or menu_type is None or level is None \
            or status is None:
        return res(state=State.PARAMS_ERROR)

    if level == 1 and not parent_id:    # 子节点情况需传递父节点ID
        return res(state=State.PARAMS_ERROR)

    # todo 迭代更新太多，考虑使用redis
    if level == 0:  # 主节点
        group = AuthorityGroup.query.filter_by(id=menu_id).first()
        if not group:
            return res(state=State.MENU_NOT_EXISTS)

        all_group = AuthorityGroup.query.filter_by(type=0).all()
        group_len = len(all_group)

        if order > group.order:
            num = order - group.order
            for i in range(1, num + 1):
                next_group_order = group.order + i
                for a in all_group:
                    if a.order == next_group_order:
                        a.order = next_group_order - 1
                        db.session.add(a)

        elif order <= group.order:
            num = group.order - order
            for i in range(1, num + 1):
                next_group_order = group.order - i
                for a in all_group:
                    if a.order == next_group_order:
                        a.order = next_group_order + 1
                        db.session.add(a)

        if order < 1:
            order = 1
        elif order >= group_len:
            order = group_len

        group.order = order
        db.session.add(group)
        db.session.commit()

    else:
        auth = Authority.query.filter_by(id=menu_id).first()
        if not auth:
            return res(state=State.MENU_NOT_EXISTS)

        all_auth = Authority.query.filter_by(group_id=auth.group_id).all()
        auth_len = len(all_auth)

        if order > auth.order:
            num = order - auth.order
            for i in range(1, num + 1):
                next_auth_order = auth.order + i
                for a in all_auth:
                    if a.order == next_auth_order:
                        a.order = next_auth_order - 1
                        db.session.add(a)

        elif order <= auth.order:
            num = auth.order - order
            for i in range(1, num + 1):
                next_auth_order = auth.order - i
                for a in all_auth:
                    if a.order == next_auth_order:
                        a.order = next_auth_order + 1
                        db.session.add(a)

        if order <= 1:
            order = 1
        elif order >= auth_len:
            order = auth_len

        auth.order = order
        db.session.add(auth)
        db.session.commit()

    return res()


@authorities.route("/delete_menu", methods=["POST"])
@requires_logged_in(is_top_partner=True)
def delete_menu():
    """
    删除节点
    :return:
    """
    req = request.get_json(force=True)
    # 节点ID
    menu_id = req.get("menu_id", None)
    # 等级 0 主节点 1 子节点
    level = req.get('level', None)

    if not menu_id or level is None:
        return res(state=State.PARAMS_ERROR)

    if level == 0:  # 主节点
        group = AuthorityGroup.query.filter_by(id=menu_id).first()
        if not group:
            return res(state=State.MENU_NOT_EXISTS)

        count = AuthorityGroupRelation.query.filter_by(group_id=group.id)\
                                            .with_entities(AuthorityGroupRelation.id)\
                                            .count()
        if count > 0:
            return res(state=State.FAILURE, msg="删除失败,此父节点还有{}个子节点".format(count))

        all_group = AuthorityGroup.query.filter(AuthorityGroup.type == 0, AuthorityGroup.order > group.order).all()
        for item in all_group:
            item.order -= 1
            db.session.add(item)

        db.session.delete(group)
        db.session.commit()
    else:
        auth = Authority.query.filter_by(id=menu_id).first()
        if not auth:
            return res(state=State.MENU_NOT_EXISTS)

        count = AuthorityRoleRelation.query.filter_by(authority_id=menu_id)\
                                           .with_entities(AuthorityRoleRelation.id)\
                                           .count()
        if count > 0:
            return res(state=State.FAILURE, msg="删除失败,此节点还有{}个角色正在使用".format(count))

        relation = AuthorityGroupRelation.query.filter_by(authority_id=auth.id, group_id=auth.group_id).first()
        if relation:
            db.session.delete(relation)

        all_auth = Authority.query.filter(Authority.group_id == auth.group_id, Authority.order > auth.order).all()
        for item in all_auth:
            item.order -= 1
            db.session.add(item)

        db.session.delete(auth)
        db.session.commit()

    return res()
