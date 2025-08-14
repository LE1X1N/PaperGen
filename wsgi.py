from src.app import create_app

app = create_app()

"""
    测试
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8687, debug=False, processes=1, threaded=False)
