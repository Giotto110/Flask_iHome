# -*- coding:utf-8 -*-
import functools

from flask import session, jsonify,g
from werkzeug.routing import BaseConverter

from iHome.utils.response_code import RET



def login_required(func):

    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify(errno=RET.SESSIONERR,errmsg="用户未登录")
        else:
            g.user_id = user_id
            return func(*args,**kwargs)

    return wrapper

class RegexConverter(BaseConverter):
    """自定义正则转换器"""

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

