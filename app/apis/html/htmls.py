# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/11/26 
"""
from flask import render_template
from app.apis.html import html


@html.route("/home")
def home():
    return render_template("home.html")
