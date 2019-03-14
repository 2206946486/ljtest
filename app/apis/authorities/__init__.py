# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/22 
"""
from flask import Blueprint

authorities = Blueprint("authorities", __name__)

from . import role, menu