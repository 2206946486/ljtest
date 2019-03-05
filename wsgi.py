# -*- coding: UTF-8 -*-
"""
@author: lj
@date: 2019/3/5
"""
from app import create_app
from schema import SchemaError

app = create_app()


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "X-Requested-With")
    response.headers.add("Access-Control-Allow-Methods", "POST,GET")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8100)