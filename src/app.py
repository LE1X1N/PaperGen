from flask import Flask

from src.config import conf
from src.api.routes import api_bp
from src.utils import setup_logger


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/v1')
    
    # config
    setup_logger(conf["service_type"])
    
    return app