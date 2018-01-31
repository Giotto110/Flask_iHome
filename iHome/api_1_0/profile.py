# -*- coding:utf-8 -*-
import user

from flask import current_app, jsonify
from flask import request
from flask import session
from flask import g

from iHome.utils.commons import login_required
from iHome import constants
from iHome import db
from iHome.models import User
from . import api
from iHome.utils.response_code import RET
from iHome.utils.image_storage import upload_image


@api.route("/user/name",methods=["POST"])
@login_required
def set_user_name():
    user_name = request.json.get("name")
    if not user_name:
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    # user_id = session.get("user_id")
    user_id = g.user_id

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询数据出错")

    if not user:
        return jsonify(errno=RET.NODATA,errmsg="当前用户不存在")

    user.name = user_name

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg="保存数据失败")

    return jsonify(errno=RET.OK,errmsg="保存成功")

@api.route('/user/avatar',methods=['POST'])
@login_required
def set_user_avatar():
    try:
        avatar_data = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg="获取文件失败")
    try:
        key = upload_image(avatar_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="用户不存在")

    user.avatar_url = key

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg="保存数据失败")

    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK,errmsg="上传",data={"avatar_url":avatar_url})

@api.route('/user')
@login_required
def get_user_info():
    """
    获取用户信息
    1. 获取到当前登录的用户模型
    2. 返回模型中指定内容
    :return:
    """
    # user_id = session.get("user_id")
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误")

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户不存在")

    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())