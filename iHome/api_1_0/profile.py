# -*- coding:utf-8 -*-
from flask import current_app, jsonify
from flask import session

from iHome.models import User
from . import api
from iHome.utils.response_code import RET



@api.route('/user')
def get_user_info():
    """
    获取用户信息
    1. 获取到当前登录的用户模型
    2. 返回模型中指定内容
    :return:
    """
    user_id = session.get("user_id")

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误")

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户不存在")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())