# -*- coding:utf-8 -*-


import redis


class Config(object):
    SECRET_KEY = 'yJYu8Wf6/RdeJAye1ad4K238EXD+VHmdYKJ88qHYG02O0XqhvaEODrhxXwNQBtvb'



    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400 * 2


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome2"


class TestingConfig(Config):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}