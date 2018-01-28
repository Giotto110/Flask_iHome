# -*- coding:utf-8 -*-


from . import api


@api.route('/', methods=["GET", "POST"])
def index():
    # redis_store.set("name","laowang")
    # session["name"] = "xiaohua"
    return 'index'
