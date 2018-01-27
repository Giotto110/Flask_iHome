# -*- coding:utf-8 -*-

from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
# from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate,Manager

class Config(object):

    SECRET_KEY = 'yJYu8Wf6/RdeJAye1ad4K238EXD+VHmdYKJ88qHYG02O0XqhvaEODrhxXwNQBtvb'

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS =False

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400*2

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

CSRFProtect(app)

Session(app)

manager = Manager(app)
Manager(app,db)
manager.add_command("db",MigrateCommand)

@app.route('/',methods=["GET","POST"])
def index():
    # redis_store.set("name","laowang")
    session["name"] = "xiaohua"
    return 'index'


if __name__ == '__main__':
    manager.run()
