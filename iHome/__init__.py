# -*- coding:utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config
from iHome.utils.common import RegexConverter


# 创建 SQLAlchemy的 db 对象
db = SQLAlchemy()

redis_store = None

def setup_logging(level):
    # 设置日志的记录等级
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 工厂方法：根据传入的参数，创建出指定参数所对应的对象
def create_app(config_name):
    # 调用设置日志的函数，并且=传入当前配置的日志等级
    setup_logging(config[config_name].LOGGING_LEVEL)

    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])
    # 数据库
    # db = SQLAlchemy(app)
    # 关联app
    db.init_app(app)
    # redis
    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    # 开启CSRF保护，只做校验
    # 需要我们自己做以下两步操作才能完成csrf_token整个工作流程
    # 1. 在响应中添加csrf_token的cookie
    # 2. 在发起POST/PUT/DELETE 请求的时候需要带上csrf_token
    CSRFProtect(app)
    # 指定Session保存的位置
    Session(app)

    # 添加正则路由转换器,因为下面要使用转换器，所以先添加转换器再注册路由
    app.url_map.converters["re"] = RegexConverter

    # 注册蓝图
    from iHome.api_1_0 import api
    app.register_blueprint(api, url_prefix="/api/v1.0")
    from iHome.web_html import html
    app.register_blueprint(html)

    print app.url_map

    return app
