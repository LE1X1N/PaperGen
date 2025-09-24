import base64
from pathlib import Path
import os

from src.config import conf

class LocalStorage():
    def __init__(self):
        self.local_file_dir = Path(conf["service"]["storage"]["local"]["base_dir"])
        
    def _get_local_request_dir(self, request_id):
        request_dir = self.local_file_dir / request_id
        if not os.path.exists(request_dir):
            os.mkdir(request_dir)
        if not os.path.exists(request_dir / "code"):
            os.mkdir(request_dir / "code")
        if not os.path.exists(request_dir / "img"):
            os.mkdir(request_dir / "img")
        return request_dir

    def save_code(self, request_id: str, page_id: str, code: str):
        file_path = self._get_local_request_dir(request_id) / "code" / f"task_{page_id}.jsx"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return file_path

    def save_img(self, request_id: str, page_id: str, img: str):
        """
            img: Base64 encoded images
        """
        file_path = self._get_local_request_dir(request_id) / "img" / f"task_{page_id}.png"
        
        if img.startswith("data:image"):
            img_base64 = img.split(",")[1]
        else:
            img_base64 = img
        
        # base64 to binary stream
        img_bytes = base64.b64decode(img_base64, validate=True)
        with open(file_path, "wb") as f:  
            f.write(img_bytes)
        return file_path

    def check_storage_health(self):
        if not self.local_file_dir.exists():
            self.local_file_dir.mkdir(exist_ok=True)
            print(f"创建文件存储路径：{self.local_file_dir}")
        