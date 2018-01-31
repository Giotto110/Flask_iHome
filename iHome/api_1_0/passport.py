# -*- coding:utf-8 -*-
import logging
import re

from flask import current_app
from flask import request, jsonify
from flask import session

from iHome import redis_store, db
from iHome.models import User
from iHome.utils.response_code import RET
from . import api


@api.route('/session',methods=["DELETE"])
def logout():

    session.pop("name")
    session.pop("user_id")
    session.pop("mobile")

    return jsonify(errno=RET.OK,errmsg="OK")



@api.route("/session", methods=["POST"])
def login():
    """
    1. 获取参数和判断是否有值
    2. 从数据库查询出指定的用户
    3. 校验密码
    4. 保存用户登录状态
    5. 返回结果
    :return:
    """

    # 1. 获取参数和判断是否有值
    data_dict = request.json

    mobile = data_dict.get("mobile")
    password = data_dict.get("password")

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    # 2. 从数据库查询出指定的用户
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误")

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户不存在")

    # 3. 校验密码
    if not user.check_passowrd(password):
        return jsonify(errno=RET.PWDERR, errmsg="密码错误")

    # 4. 保存用户登录状态
    session["user_id"] = user.id
    session["name"] = user.name
    session["mobile"] = user.mobile

    # 5. 返回结果
    return jsonify(errno=RET.OK, errmsg="登录成功")

@api.route('/users',methods=["POST"])
def register():
    data_dict = request.json
    mobile = data_dict.get("mobile")
    phonecode = data_dict.get("phonecode")
    password = data_dict.get("password")
    # 判断参数是否都有值
    if not all([mobile, phonecode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2. 取到真实的短信验证码
    try:
        real_phonecode = redis_store.get("Mobile:" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询短信验证码失败")

    if not real_phonecode:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码过期")

    # 3. 进行验证码的对比
    if phonecode != real_phonecode:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码输入错误")

    #  3.1 判断当前手机是否已被注册
    if User.query.filter(User.mobile == mobile).first:
        return  jsonify(errno=RET.DATAEXIST,errmsg="该手机号已被注册")

    # 4. 初始化User模型，保存相关数据
    user = User()
    user.mobile = mobile
    user.name = mobile
    # save password
    user.password = password


    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="保存用户数据失败")

    return jsonify(errno=RET.OK,errmsg="注册成功")