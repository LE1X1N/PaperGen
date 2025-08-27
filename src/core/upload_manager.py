import requests
from requests.exceptions import ConnectTimeout

from src.errors import *
from src.config import conf

class UploadManager:
    
    @staticmethod
    def upload_single_file(file_path):
        try:
            files = {'file': open(file_path, 'rb')}
            data = {'service_type': conf["dfs"]["service_name"]}
            res = requests.post(conf["dfs"]["upload_url"], files=files, data=data).json()

            if res['code'] != 0:
                raise UploadError(res["message"])
            
            return conf["dfs"]["download_prefix"] + res["result"]
        
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            raise FileSystemError(f"文件上传失败: {error_msg}") from e

    @staticmethod
    def upload_files(data: dict):
        paths = []
        for res in data:
            paths.append(res["path"])
        return [UploadManager.upload_single_file(path) for path in paths]


        
        


