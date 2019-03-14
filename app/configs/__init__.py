# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18
"""

import os
from app.tools.errors import EnvError

def load_config():
    env = os.environ.get("MODE", "LOCAL")
    if env == "ONLINE":
        from app.configs.online import OnlineConfig
        return OnlineConfig
    elif env == "TESTING":
        from app.configs.testing import TestingConfig
        return TestingConfig
    elif env == "LOCAL":
        from app.configs.local import LocalConfig
        return LocalConfig
    elif env == "DOCKER":
        from app.configs.docker import DockerConfig
        return DockerConfig
    else:
        raise EnvError

