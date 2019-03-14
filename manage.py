# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""

from app import create_app
from scripts.cmd import Cmd
from flask_script import Manager


app = create_app()
manager = Manager(app)
manager.add_command("test", Cmd())

if __name__ == "__main__":
    manager.run()
