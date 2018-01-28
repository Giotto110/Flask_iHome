# -*- coding:utf-8 -*-

from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    """自定义正则转换器"""

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def create_app(config_name):
    """创建应用实例"""
    app = Flask(__name__)
    ...

    # 向app中添加自定义的路由转换器
    app.url_map.converters['re'] = RegexConverter

    # 注册蓝图，在使用的时候再引入
    from iHome.api_1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1.0')

    # 注册html静态文件的蓝图
    import web_html
    app.register_blueprint(web_html.html)

    return app