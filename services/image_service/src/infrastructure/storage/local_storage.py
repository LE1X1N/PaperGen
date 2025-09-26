import base64
from pathlib import Path

from src.repository.storage_repository import StorageRepository


class LocalStorage(StorageRepository):
    def __init__(self, local_file_dir):
        super().__init__()
        self.local_file_dir = Path(local_file_dir)

    def save_code(self, code: str, path: str):
        file_path = self.local_file_dir / path
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return file_path

    def save_img(self, img: str, path: str):
        """
            img: Base64 encoded images
        """
        file_path = self.local_file_dir / path
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
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
        print(f"Storage检查通过，本地文件存储位置：{self.local_file_dir}")