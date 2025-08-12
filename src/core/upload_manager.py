import requests
from config import conf
from .parser import DataParser


class UploadManager:
    def __init__(self):
        self.url = conf["upload_url"]
        self.service_type = conf["service_type"]

    def upload_files(self, data: dict):
        paths = []
        for res in data:
            paths.append(res["path"])
        return [self._upload_single_file(path) for path in paths]

    def _upload_single_file(self, file_path):
        files = {'file': open(file_path, 'rb')}
        data = {'service_type': self.service_type}

        response = requests.post(self.url, files=files, data=data)
        return response





