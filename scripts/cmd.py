# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/25 
"""

from flask_script import Command
from app.models.partners.partner import Partner


class Cmd(Command):

    def run(self):
        data = Partner.query.filter_by(id=1).first()
        print(data.nickname, data.mobile)

