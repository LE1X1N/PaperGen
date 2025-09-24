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
        from src.config import conf
        print(f"文件存储引擎：{conf["service"]["storage"]["type"]}")
        if conf["service"]["storage"]["type"] == "local":
            from src.infrastructure.storage.local_storage import LocalStorage
            LocalStorage().check_storage_health()
            print(f"本地文件存储位置：{conf["service"]["storage"]["local"]["base_dir"]}")
            
        elif conf["service"]["storage"]["type"] == "minio":
            from src.infrastructure.storage.minio_storage import MinioStorage
            MinioStorage().check_storage_health()
            print(f"MinIO 检查通过！使用桶：{os.getenv("MINIO_BUCKET")}")

        # openai
        from src.infrastructure.llm import check_openai_health
        check_openai_health()                
        print(f"OpenAI 检查通过！默认模型：{os.getenv("OPENAI_MODEL")}")
        
        # selenium
        from src.infrastructure.browser import check_driver_health
        check_driver_health()                 
        print("Chrome Driver 检查通过！")
        
        # mongodb
        from src.infrastructure.db import check_mongodb_health
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
    