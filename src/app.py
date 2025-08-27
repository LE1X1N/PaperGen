from flask import Flask
from src.utils import setup_logger
from src.api import api_bp

def create_app():
    app = Flask(__name__)
    setup_logger()

    app.register_blueprint(api_bp, url_prefix='/v1')

    return app