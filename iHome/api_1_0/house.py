# -*- coding:utf-8 -*-
from flask import current_app, jsonify

from iHome.api_1_0 import api
from iHome.models import Area
from iHome.utils.response_code import RET


@api.route("/areas")
def get_areas():
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询数据失败")

    areas_dict_li = []
    for area in areas:
        areas_dict_li.append(area.to_dict())

    return jsonify(errno=RET.OK,errmsg="ok",data=areas_dict_li)