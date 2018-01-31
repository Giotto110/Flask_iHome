# -*- coding:utf-8 -*-
from flask import current_app, jsonify
from flask import session

from iHome.models import User
from iHome.api_1_0 import api
from iHome.utils.response_code import RET



@api.route('/user')
def get_user_info():
    user_id = session.get(user_id)

    try:
        user = User.querry.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询数据错误")
    if not user:
        return jsonify(errno=RET.USERERR,errmsg="用户不存在")
    resp = {
        "name":user.name,
        "avartar_url": user.avatar_url,
        "user_id" : user.id
    }
    return jsonify(errno=RET.OK,errmsg="OK",data=user.to_dict())