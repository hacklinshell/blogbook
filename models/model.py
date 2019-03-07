from gino import Gino
from config import DB_URL

db = Gino()
# 异步ORM数据库初始化
async def init_db():
    await db.set_bind(DB_URL)
    await db.gino.create_all()
