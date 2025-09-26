import os
from src.app import create_app

app = create_app()

"""
    测试
"""
if __name__ == "__main__":
    app.run(host=os.getenv("SVR_HOST"), port=os.getenv("SVR_HTTP_PORT"), debug=False, processes=1, threaded=False)
