# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18 
"""
import re
import hmac
import string
import random
import hashlib
from schema import SchemaError
from datetime import datetime


class Security(object):
    def __init__(self, key="zouweicheng@gmail.com", method=hashlib.sha256):
        self.key = bytes(key, encoding="utf-8")
        self.method = method

    def encrypt(self, raw):
        hashed = hmac.new(self.key, bytes(raw, encoding="utf-8"), self.method)
        return hashlib.sha1(bytes(hashed.hexdigest(), encoding="utf-8")).hexdigest()

    def __call__(self, raw):
        return self.encrypt(raw)

    def check(self, encrypted, raw):
        return encrypted == self.encrypt(raw)

    def __str__(self):
        return "Security<{0}>".format(self.key)

    __repr__ = __str__


def randstr(length):
    char = string.ascii_letters + string.digits
    return "".join(random.choice(char) for _ in range(length))


def id_key():
    app_key = datetime.now().strftime("%y%m%d") + "{}".format(random.randint(100, 999))
    app_secret = randstr(32)
    return app_key, app_secret


def checkdata(data):
    """
    合法校验
    :param data: 数据
    :return:
    """

    if data == '':
        return 0
    if len(data) < 6 or len(data) > 16:
        return 0
    res = re.findall(r'~|!|@|#|%|&|\*|\$\^', data)
    if res:
        return 0
    return 1


class DateTimeUse(object):

    def validate(self, data):
        try:
            if "." in data:
                return datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f")
            else:
                return datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(e)
            raise SchemaError('格式化数据错误')
