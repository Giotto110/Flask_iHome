# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CsrfProtect


class Config(object):

    SECRET_KEY = 'yJYu8Wf6/RdeJAye1ad4K238EXD+VHmdYKJ88qHYG02O0XqhvaEODrhxXwNQBtvb'

    DEBUG = True

    SQLAlchemy_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome"
    SQLAlchemy_TRACK_MODIFICATIONS =False

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

CsrfProtect(app)

@app.route('/',methods=["GET","POST"])
def index():
    # redis_store.set("name","laowang")
    return 'index'


if __name__ == '__main__':
    app.run()
