# -*- coding:utf-8 -*-

from flask import session
from iHome import create_app, db, models
# from flask_script import Manager  # 如果要集成迁移扩展的话，可以直接从迁移扩展里面导入
from flask_migrate import MigrateCommand, Migrate, Manager

# 在此直接指定app创建的时候是以什么样的环境去创建
app = create_app("development")
manager = Manager(app)
# 将app与db进行关联
Migrate(app, db)
# 添加迁移命令
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
