# -*- coding:utf-8 -*-

import logging
from flask import current_app
from . import api
from iHome import redis_store

@api.route('/index', methods=["GET", "POST"])
def index():
    redis_store.set("name","laowang")
    # session["name"] = "xiaohua"

    logging.debug("DEBUG LOG")
    logging.info("INFO LOG")
    logging.warn("WARN LOG")
    logging.error("ERROR LOG")
    logging.fatal("FATAL LOG")

    current_app.logger.debug("DEBUG LOG")
    current_app.logger.info("INFO LOG")
    current_app.logger.warn("WARN LOG")
    current_app.logger.error("ERROR LOG")
    current_app.logger.fatal("FATAL LOG")
    return 'index'
