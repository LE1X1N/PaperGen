from flask import Flask

from src.utils import setup_logger
from src.config import LOCAL_FILE_DIR, LOG_BASE_DIR

from src.infrastructure.llm import check_openai_health
from src.infrastructure.db import check_mongodb_health
from src.infrastructure.browser import check_driver_health


def create_app():
    try:
        if not LOCAL_FILE_DIR.exists():
            LOCAL_FILE_DIR.mkdir(exist_ok=True)
            print(f"创建文件存储路径：{LOCAL_FILE_DIR}")
        print(f"本地文件存储位置：{LOCAL_FILE_DIR}")
            
        if not LOG_BASE_DIR.exists():
            LOG_BASE_DIR.mkdir(exist_ok=True)
            print(f"创建日志路径：{LOCAL_FILE_DIR}")  
            
        log_file_path = setup_logger()
        print(f"日志存储位置：{log_file_path}")
    
        check_openai_health()                
        print("OpenAI 检查通过！")
        
        check_driver_health()                 
        print("Chrome Driver 检查通过！")
        
        check_mongodb_health()
        print("MongoDB 检查通过！")
        
        from src.api import api_bp
        
        app = Flask(__name__)
        app.register_blueprint(api_bp, url_prefix='/v1')
        print("服务启动成功！")
        return app
    
    except Exception as e:
        print(f"服务启动失败，出现错误：{e}")
        exit()
    