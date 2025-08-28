import requests

from src.errors import FileSystemError
from src.config import conf

"""
    Upload files to DFS
"""
def upload_single_file(file_path):
    try:
        files = {'file': open(file_path, 'rb')}
        data = {'service_type': conf["dfs"]["service_name"]}
        res = requests.post(conf["dfs"]["upload_url"], files=files, data=data).json()

        if res['code'] != 0:
            raise FileSystemError(res["message"])
            
        return conf["dfs"]["download_prefix"] + res["result"]
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        raise FileSystemError(f"文件上传失败: {error_msg}") from e


def upload_files(data: dict):
    paths = []
    for res in data:
        paths.append(res["path"])
    return [upload_single_file(path) for path in paths]


def check_dfs_health():
    try:
        res = requests.get(conf["dfs"]["health_check_url"])
        if res.status_code != 200:
            raise FileSystemError
    except FileSystemError:
        raise