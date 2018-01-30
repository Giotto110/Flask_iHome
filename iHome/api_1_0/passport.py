# -*- coding:utf-8 -*-
from flask import current_app
from flask import request, jsonify

from iHome import redis_store, db
from iHome.models import User
from iHome.utils.response_code import RET
from . import api

@api.route('/users',method=["POST"])
def register():
    data_dict =request.json
    mobile =data_dict.get("mobile")
    phonecode = data_dict.get("phonecode")
    password = data_dict.get("password")
    if not all([mobile,phonecode,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    try:
        real_phonecode = redis_store.get("Mobile" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询短信验证码失败")

    if not real_phonecode:
        return jsonify(errno=RET.NODATA,errmsg="短信验证码过期")

    if phonecode != real_phonecode:
        return jsonify(errno=RET.DATAERR,errmsg="短信验证码输入错误")

    user =User()
    user.mobile = mobile
    user.name = mobile
    # TODO save password

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="保存用户数据失败")

    return jsonify(errno=RET.OK,errmsg="注册成功")