# -*- coding:utf-8 -*-
from flask import current_app, jsonify
from flask import request

from iHome import db
from iHome.api_1_0 import api
from iHome.models import Area, House, Facility, HouseImage
from iHome.utils import image_storage
from iHome.utils.commons import login_required
from iHome.utils.response_code import RET
from iHome import constants



@api.route('/houses/image',methods=["POST"])
@login_required
def upload_house_image():
    try:
        house_image = request.files.get("house_image").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    house_id = request.form.get("house_id")

    if not house_id:
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询房屋数据失败")

    if not house:
        return jsonify(errno=RET.NODATA,errmsg="当前房屋不存在")

    try:
        key = image_storage.upload_image(house_image)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    house_image_model = HouseImage()

    house_image_model.house_id = house_id
    house_image_model.url = key

    try:
        db.session.add(house_image_model)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="添加数据失败")

    return jsonify(errno=RET.OK, errmsg="上传成功",data={"image_url": constants.QINIU_DOMIN_PREFIX + key})



@api.route("/houses",methods=["POST"])
@login_required
def add_house():
    data_dict = request.json
    title = data_dict.get('title')
    price = data_dict.get('price')
    address = data_dict.get('address')
    area_id = data_dict.get('area_id')
    room_count = data_dict.get('room_count')
    acreage = data_dict.get('acreage')
    unit = data_dict.get('unit')
    capacity = data_dict.get('capacity')
    beds = data_dict.get('beds')
    deposit = data_dict.get('deposit')
    min_days = data_dict.get('min_days')
    max_days = data_dict.get('max_days')

    if not all([title,price,address,area_id,room_count,acreage,unit,capacity,beds,deposit,min_days,max_days]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    try:
        price = int(float(price)*100)
        deposit = int(float(deposit)*100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    house = House()
    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    facilities = data_dict.get("facility")

    house.facilities = Facility.query.filter(Facility.id.in_(facilities)).all()

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg="添加数据失败")

    return jsonify(errno=RET.OK,errmsg="OK")


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