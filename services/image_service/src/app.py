import os
from flask import Flask

def create_app():
    try:
        if os.getenv("OPENAI_API_KEY") is None:
            print("Error: 当前环境未设置 OPENAI_API_KEY, 请使用 export OPENAI_API_KEY=sk-XXXXXX 设置该环境变量！")
            exit(0)
        
        # log 
        from src.utils import setup_logger
        log_file_path = setup_logger()
        print(f"日志存储位置：{log_file_path}")
        
        # storage engine
        from src.repository.storage_factory import get_storage
        get_storage().check_storage_health()
        
        # openai
        from src.infrastructure.llm import check_openai_health
        check_openai_health()                
        
        # selenium
        from src.infrastructure.browser import check_driver_health
        check_driver_health()                 
        
        # mongodb
        from src.infrastructure.db import check_mongodb_health
        check_mongodb_health()
        
        from src.api import api_bp
        app = Flask(__name__)
        app.register_blueprint(api_bp, url_prefix='/v1')
        print("服务启动成功！")
        return app
    
    except Exception as e:
        print(f"服务启动失败，出现错误：{e}")
        exit()
    