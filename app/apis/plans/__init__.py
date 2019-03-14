# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18
"""
from flask import Blueprint

plans = Blueprint("plans", __name__)

from . import plan