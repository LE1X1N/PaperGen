from flask import Flask

from src.llm import check_openai_health
from src.browser import check_driver_health
from src.utils import setup_logger
from src.api import api_bp

def create_app():
    app = Flask(__name__)
    setup_logger()
    app.register_blueprint(api_bp, url_prefix='/v1')

    try:
        check_openai_health()                  # check OpenAI
        print("OpenAI 检查通过！")
        check_driver_health()                  # check chrome driver  
        print("Chrome Driver 检查通过！")
        
        print("服务启动成功！")
        return app
    
    except Exception as e:
        print(f"服务启动失败，出现错误：{e}")
        exit()
    