# -*- coding:utf-8 -*-
# 验证码的提供：图片验证码和短信验证码
import random
import re

from flask import abort
from flask import current_app
from flask import json
from flask import make_response
from flask import request, jsonify

from iHome import constants
from iHome.utils.response_code import RET
from iHome.utils.sms import CCP
from . import api
from iHome import redis_store
from iHome.utils.captcha.captcha import captcha




@api.route("/sms_code",methods=["POST"])
def send_sms_code():
    json_data = request.data

    json_dict = json.loads(json_data)
    mobile = json_dict.get("mobile")
    image_code = json_dict.get("image_code")
    image_code_id = json_dict.get("image_code_id")

    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    if not re.match("^1[34578][0-9]{9}$",mobile):
        return jsonify(errno=RET.PARAMERR,errmsg="手机号格式有误")

    try:
        real_image_code = redis_store.get("ImageCode" + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询验证码出错")

    if not real_image_code:
        return jsonify(errno=RET.NODATA,errmsg="验证码已过期")

    if image_code.lower()!=real_image_code.lower():
        return jsonify(errno=RET.DATAERR,errmsg="验证码输入不正确")

    sms_code = "%06d" % random.randint(0,999999)
    current_app.logger.debug("短信验证码为：" + sms_code)

    result = CCP().send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],"1")
    if result != 1:
        return jsonify(errno=RET.THIRDERR,errmsg="发送短信失败")

    try:
        redis_store.set("Mobile:" + mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="保存验证码失败")
    return jsonify(errno=RET.OK,errmsg="发送成功")


@api.route("/image_code")
def get_image_code():
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")

    if not cur_id:
        abort(403)
    name,text,image = captcha.generate_captcha()
    current_app.logger.debug("图片验证码为:" + text)

    try:
        redis_store.set("ImageCode:" + cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            # print pre_id
            redis_store.delete("ImageCode:" + pre_id)
    except Exception as e:
        print e
        return jsonify(errno=RET.DBERR,errmsg="保存验证码数据失败")

    response = make_response(image)
    response.headers["Content-Type"] = "image/jpg"
    return image