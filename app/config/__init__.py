# -*- coding: UTF-8 -*-
"""
@author: lj
@date: 2019/3/5
"""
import os


def load_config():
    env = os.environ.get("MODE", "LOCAL")
    if env == 'LOCAL':
        from app.config.local import OnlineConfig
        return OnlineConfig
    elif env == 'ONLINE':
        from app.config.local import OnlineConfig
        return OnlineConfig