# -*- coding:utf-8 -*-

import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)

    CSRFProtect(app)

    Session(app)

    return app

def create_app(config_name):
    from iHome.api_1_0 import api
    app.register_blueprint(api,url_prefix='/api/v1.0')

    import web_html
    app.register_blueprint(web_html.html)

    return app