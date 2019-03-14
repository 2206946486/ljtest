# -*- coding: UTF-8 -*-
"""
@author: cc
@date: 2018/10/23
"""

from flask import Blueprint

cards = Blueprint("cards", __name__)

from . import card