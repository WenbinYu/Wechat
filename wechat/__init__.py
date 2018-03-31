from flask import  Flask,Blueprint
from  flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import configs


wechat_blue = Blueprint('/',__name__)

db = SQLAlchemy()

redis_store = None

def get_app(config_name):
    app = Flask(__name__)

    app.config.from_object(configs[config_name])

    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)

    CSRFProtect(app)

    Session(app)
    return app
from wechat.views import *