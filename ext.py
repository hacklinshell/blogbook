#导入权限验证模块
from sanic_auth import Auth
#导入mako模板
from sanic_mako import SanicMako

from config import SENTRT_DSN


mako = SanicMako()
auth = Auth()


if SENTRT_DSN:
    from sanic_sentry import SanicSentry
    sentry = SanicSentry()
else:
    sentry = None