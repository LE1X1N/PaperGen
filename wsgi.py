from src.app import create_app
from src.config import conf

app = create_app()

"""
    测试
"""
if __name__ == "__main__":
    app.run(host=conf["papergen"]["host"], port=conf["papergen"]["http_port"], debug=False, processes=1, threaded=False)
