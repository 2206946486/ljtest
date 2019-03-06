# -*- coding: UTF-8 -*-
"""
@author: lj
@date: 2019/3/5
"""
from app.apis.html import html
from flask import redirect, request, render_template


@html.route('/')
def login_info():
    return redirect('/login')


@html.route('/login', methods=['GET'])
def login():
    return render_template('./html/login.html')

