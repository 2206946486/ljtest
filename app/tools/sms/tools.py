# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/19 
"""

import pickle
import requests
from app.tools.redis.tools import rc_yun


class YunMessage(object):

    url = "http://sms-test-api.china-m2m.com/v1/sms"

    def __init__(self):
        self._sess = requests.Session()
        self._sess.keep_alive = False

    def send_message(self, mobile, text):
        data = dict(mobile=mobile, username='qhyl', password='szqhyl666', content=text)
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        try:
            resp = self._sess.post(self.url, data=data, headers=headers)
        except Exception:
            return
        data = resp.json()
        if not data['status']:
            return
        return data

    def send_code(self, mobile, code):
        text = u"【物联通】您的验证码是{}。有效期为10分钟，请尽快验证".format(code)
        return self.send_message(mobile, text)

    def send_info(self, mobile, text):
        info = text
        return self.send_message(mobile, info)

def set_messages(mobile, data):
    return rc_yun.set_key("IOT:MESSAGES:{}".format(mobile), pickle.dumps(data))


def get_messages(mobile):
    data = rc_yun.get("IOT:MESSAGES:{}".format(mobile))
    if not data:
        return data
    return pickle.loads(data)


def del_messages(mobile):
    return rc_yun.delete_key("IOT:MESSAGES:{}".format(mobile))
