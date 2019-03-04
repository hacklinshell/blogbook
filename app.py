from sanic import Sanic
from sanic.request import Request as _Request
from sanic.response import text
from sanic_session import Session, MemcacheSessionInterface

import config
from ext import auth, mako, sentry


from werkzeug.utils import find_modules, import_string


# 定义蓝图注册函数，用于注册全部蓝图
def register_blueprints(root, app):
    for name in find_modules(root, recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bd'):
            app.register_blueprint(mod.bp)


class Request(_Request):
    # 返回当前登陆的用户
    @property
    def user(self):
        return auth.current_user(self)

    @property
    def user_id(self):
        return self.user_id if self.user else 0


# sanic实例化
app = Sanic(__name__, request_class=Request)
# 加载配置文件
app.config.from_object(config)
# auth模块设置应用程序配置文件
auth.setup(app)
# mako 模板初始化
mako.init_app(app, context_processors=())
# 如果配置了应用程序监控配置项，就初始化
if sentry is not None:
    sentry.init_app(app)
# 注册views目录下的所有蓝图
register_blueprints('views', app)
# 静态文件注册
app.static('static', './static')
# session实例化
session = Session()
client = None
redis = None

@app.route("/")
async def test(request):
    return text('blogbook test ok !')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000,debug=config.DEBUG)