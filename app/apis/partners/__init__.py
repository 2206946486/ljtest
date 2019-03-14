# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18
"""

from flask import Blueprint

partners = Blueprint("partners", __name__)

from . import partner, register