# 导入tortoise-orm模块   异步ORM
from tortoise import Tortoise
# 导入权限验证模块
from sanic_auth import Auth
# 导入mako模板
from sanic_mako import SanicMako
# 用于协程之间上下文传递
import aiotask_context as context

from config import SENTRT_DSN, DB_URL


mako = SanicMako()
auth = Auth()

# 异步ORM数据库初始化
async def init_db(create_db=False):
    await Tortoise.init(db_url=DB_URL, modules={'models': ['models']}, _create_db=create_db)

if SENTRT_DSN:
    from sanic_sentry import SanicSentry
    sentry = SanicSentry()
else:
    sentry = None
