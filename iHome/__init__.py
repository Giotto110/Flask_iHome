# -*- coding:utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config
from iHome.utils.commons import RegexConverter

db = SQLAlchemy()

redis_store = None

def setup_logging(level):
    # 设置日志的记录等级
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):

    setup_logging(config[config_name].LOGGING_LEVEL)

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)

    # CSRFProtect(app)

    Session(app)

    app.url_map.converters["re"] = RegexConverter

    from iHome.api_1_0 import api
    app.register_blueprint(api,url_prefix="/api/v1.0")

    from iHome.web_html import html
    app.register_blueprint(html)

    return app
