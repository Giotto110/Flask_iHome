# -*- coding:utf-8 -*-


from . import api
from iHome import redis_store

@api.route('/', methods=["GET", "POST"])
def index():
    # redis_store.set("name","laowang")
    # session["name"] = "xiaohua"
    return 'index'