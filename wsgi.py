# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/18
"""

from app import create_app
from schema import SchemaError
from app.tools.errors import res, State, EnvError

app = create_app()


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "X-Requested-With")
    response.headers.add("Access-Control-Allow-Methods", "POST,GET")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response


@app.errorhandler(EnvError)
def env_error(e):
    return res(State.ENV_ERROR)


@app.errorhandler(SchemaError)
def schema_error(e):
    return res(State.PARAMS_ERROR)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)