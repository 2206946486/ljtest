# -*- coding: UTF-8 -*-
"""
@author: lj
@date: 2019/3/5
"""
from flask import Blueprint

partners = Blueprint("partners", __name__)

from . import partner