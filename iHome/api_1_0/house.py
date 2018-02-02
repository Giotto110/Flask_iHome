# -*- coding:utf-8 -*-
# 房屋相关的视图函数
from flask import current_app
from flask import g
from flask import jsonify
from flask import request
from flask import session

from iHome import constants
from iHome import db
from iHome.utils.commons import login_required
from iHome.utils.response_code import RET
from iHome.api_1_0 import api
from iHome.models import Area, House, Facility, HouseImage
from iHome.utils import image_storage


@api.route('/houses/<int:house_id>')
def get_house_detail(house_id):
    """
    1. 通过house_id查询指定的房屋模型
    2. 将房屋的详细信息封装成字典
    3. 进行返回
    :return:
    """

    # 1. 通过house_id查询指定的房屋模型
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")
    # 2. 将房屋的详细信息封装成字典
    resp_dict = house.to_full_dict()

    user_id = session.get("user_id",-1)
    # 3. 进行返回
    return jsonify(errno=RET.OK, errmsg="OK", data={"house": resp_dict,"user_id":user_id})


@api.route('/houses/image', methods=["POST"])
@login_required
def upload_house_image():
    """
    1. 取到参数，图片，房屋的id
    2. 获取到指定id的房屋模型
    3. 上传图片到七牛云
    4. 初始化房屋图片的模型
    5. 设置数据并且保存到数据库
    6. 返回响应-->图片的url
    :return:
    """

    # 1. 取到参数，图片，房屋的id
    try:
        house_image = request.files.get("house_image").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 取到房屋id
    house_id = request.form.get("house_id")

    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2. 获取到指定id的房屋模型
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询房屋数据失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="当前房屋不存在")

    # 3. 上传图片到七牛云
    try:
        key = image_storage.upload_image(house_image)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    # 判断当前房屋是否设置了index_image，如果没有设置就设置
    if not house.index_image_url:
        house.index_image_url = key

    # 4. 初始化房屋图片的模型
    house_image_model = HouseImage()

    # 5. 设置数据并且保存到数据库
    house_image_model.house_id = house_id
    house_image_model.url = key

    try:
        db.session.add(house_image_model)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="添加数据失败")

    # 6. 返回响应-->图片的url
    return jsonify(errno=RET.OK, errmsg="上传成功", data={"image_url": constants.QINIU_DOMIN_PREFIX + key})


@api.route('/houses', methods=["POST"])
@login_required
def add_house():
    """
    添加新房屋
    1. 接收所有参数
    2. 判断参数是否有值&参数是否符合规范
    3. 初始化房屋模型，并设置数据
    4. 保存到数据库
    5. 返回响应
    :return:
    """

    # 1. 接收所有参数
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

    # 2. 判断参数是否有值&参数是否符合规范
    if not all(
            [title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        # 以分的形式进行保存
        price = int(float(price) * 100)
        deposit = int(float(deposit)*100)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 3. 初始化房屋模型，并设置数据
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

    # 取到当前房屋的设置列表
    facilities = data_dict.get("facility")
    # [1, 3, 4, 6]

    # 当前房屋对应的所有设置
    house.facilities = Facility.query.filter(Facility.id.in_(facilities)).all()

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="添加数据失败")

    return jsonify(errno=RET.OK, errmsg="OK", data={"house_id": house.id})


@api.route("/areas")
def get_areas():
    """
    获取所有的城区信息
    1. 查询所有的Areas数据
    2. 返回
    :return:
    """

    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    # 定义空列表，用于保存遍历的时候所转换的字典
    areas_dict_li = []
    # 转模型转字典
    for area in areas:
        areas_dict_li.append(area.to_dict())
    # 返回
    return jsonify(errno=RET.OK, errmsg="ok", data=areas_dict_li)
