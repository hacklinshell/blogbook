
# 导入权限验证模块
from sanic_auth import Auth
# 导入mako模板
from sanic_mako import SanicMako
# 用于协程之间上下文传递
import aiotask_context as context




mako = SanicMako()
auth = Auth()


