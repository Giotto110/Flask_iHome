# -*- coding:utf-8 -*-

from iHome import app, db
# from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate, Manager

manager = Manager(app)
Manager(app, db)
manager.add_command("db", MigrateCommand)


@app.route('/', methods=["GET", "POST"])
def index():
    # redis_store.set("name","laowang")
    # session["name"] = "xiaohua"
    return 'index'


if __name__ == '__main__':
    manager.run()
