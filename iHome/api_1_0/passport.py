# -*- coding:utf-8 -*-
import logging
from flask import current_app
from flask import request, jsonify
from flask import session

from iHome import redis_store, db
from iHome.models import User
from iHome.utils.response_code import RET
from . import api

@api.route('/session',methods=["POST"])
def login():
    dict_json = request.get_json()
    mobile = dict_json.get('mobile')
    password = dict_json.get('password')

    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    if not re.match(u"^1[345678]\d{9}$",mobile):
        return jsonify(errno=RET.PARAMERR,errmsg="手机号码格式不正确")

    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR,errmsg='数据库查询错误')

    if user is None:
        return jsonify(errno=RET.USERERR,errmsg='用户不存在')

    if not user.check_password(password):
        return jsonify(errno=RET.LOGINERR,errmgs="密码错误")

    session['user_id']=user.id
    session['mobile']=user.mobile
    session['name']=user.name

    return jsonify(errno=RET.OK,errmsg='登录成功')

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