# 异步编程基础库
import asyncio
# 异步HTTP 客户端/服务端编程库
import aiohttp
# 异步redis使用
import aioredis
from pathlib import Path


# 用于异步的分布式内存缓存，需要配合memcache使用 MemcacheSessionInterface
import aiomcache
from sanic import Sanic
from sanic.request import Request as _Request
from sanic.response import text
from sanic_session import Session, MemcacheSessionInterface

import config
from ext import auth, mako, sentry, init_db, context


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

# 注册服务启动前监听器
@app.listener('before_server_start')
async def setup_db(app, loop):
    global client
    # 初始化orm
    await init_db()

    # 创建缓存链路
    client = aiomcache.Client(config.MEMCACHED_HOST, config.MEMCACHED_PORT, loop=loop)  # noqa
    # session初始化
    session.init_app(app, interface=MemcacheSessionInterface(client))
    # 设置loop.create_task()使用的任务  context用于协程上下文切换
    loop.set_task_factory(context.task_factory)
    # 创建一个http请求会话（session）对象async_session
    app.async_session = aiohttp.ClientSession()
    # UPLOAD_FOLDER路径下创建文件
    Path(config.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# 服务关闭后的监听器
@app.listener('after_server_stop')
async def close_aiohttp_session(sanic_app, _loop) -> None:
    await sanic_app.async_session.close()

# 注册request中间件
@app.middleware('request')
async def setup_context(request):
    global redis
    loop = asyncio.get_event_loop()
    if redis is None:
        redis = await aioredis.create_redis_pool(config.REDIS_URL, minsize=5, maxsize=20, loop=loop)
    # 其他协程会使用到redis和client
    context.set('redise', redis)
    context.set('memcache', client)


@app.route("/")
async def test(request):
    return text('blogbook test ok !')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=config.DEBUG)
