# -*- coding: UTF-8 -*-
"""
@author: lj
@date: 2019/3/5
"""
from app.apis.partner import partners


@partners.route("/login", methods=["GET"])
def login():
    return 'hello world!'
