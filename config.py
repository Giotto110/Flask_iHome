# -*- coding:utf-8 -*-

import redis
import logging


class Config(object):
    SECRET_KEY = "euy+joaUnBIUwBPuHom5DZ849QRyyQKrZcqe98agqkLmJfLyOfR+ZhBqkgwceAkG"

    # 数据库的配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome"
    # 关闭修改跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis的配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 设置session保存参数
    SESSION_TYPE = "redis"
    # 设置session保存redis的相关链接信息，如果不设置的话会以默认的ip和端口设置
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启session签名
    SESSION_USE_SIGNER = True
    # 设置session的生命周期
    PERMANENT_SESSION_LIFETIME = 86400 * 2
    # 开发环境日志的等级为调用模式
    LOGGING_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    """开发环境的配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境下的配置"""
    # 数据库的配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome6"
    # 生产环境下日志等级为警告
    LOGGING_LEVEL = logging.WARN

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
