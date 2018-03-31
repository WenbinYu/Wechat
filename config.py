# -*- coding:utf-8 -*-
import redis


class Config(object):

    TOKEN = 'wechat07'
    DEBUG = False
    SECRET_KEY = 'AK0j4NSomJQKm8gD/917OniOIC8DEMQRP+xPBvGanEBieaADMBTA0EBTrJdAiXgU'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@47.106.85.219:3306/wechat01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = '47.106.85.219'
    REDIS_PORT = 6379

    # 配置session数据存储到redis数据库
    SESSION_TYPE = 'redis'
    # 指定存储session数据的redis的位置
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启session数据的签名，意思是让session数据不以明文形式存储
    SESSION_USE_SIGNER = True
    # 設置session的会话的超时时长 ：一天
    PERMANENT_SESSION_LIFETIME = 3600 * 24

    APPID = ''
    APPSECRET = ''
    TOKEN = 'pythonproject07'


class DevelopmentConfig(Config):
    """创建调试环境下的配置类"""
    # 我们的爱家租房的房型，调试模式的配置和Config一致，所以pass
    pass


class ProductionConfig(Config):
    """创建线上环境下的配置类"""

    # 重写有差异性的配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.72.77:3306/wechat02'

configs =  {
    'default_config':Config,
    'development':DevelopmentConfig,
    'production': ProductionConfig,
}