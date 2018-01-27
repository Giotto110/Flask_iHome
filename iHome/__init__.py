# -*- coding:utf-8 -*-

import redis
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

CSRFProtect(app)

Session(app)
