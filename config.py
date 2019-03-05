import os
#测试时候数据库用户名root  密码password   
DB_URL = 'mysql://root:password@127.0.0.1:3306/test?charset=utf8'
REDIS_URL = 'redis://localhost:6379'

DEBUG = False
MEMCACHED_HOST = '127.0.0.1'
MEMCACHED_PORT = 11211



#应用程序监控,错误报告
SENTRT_DSN = ''

HERE = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(HERE, 'static/upload')