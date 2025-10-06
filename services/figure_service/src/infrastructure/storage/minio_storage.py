import os
import io
import base64

from minio import Minio
from minio.error import S3Error

from src.repository.storage_repository import StorageRepository


class MinioStorage(StorageRepository):
    
    def __init__(self):
        super().__init__()
        self.client = Minio(
                endpoint=f"{os.getenv("MINIO_HOST")}:{os.getenv("MINIO_PORT")}",
                access_key=os.getenv("MINIO_USER"),
                secret_key=os.getenv("MINIO_PASSWORD"),
                secure=False
            )
        self.bucket = os.getenv("MINIO_BUCKET")

    def _create_bucket(self, client, bucket):
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)

    def save_code(self, code: str, path: str):
        try: 
            code_bytes = code.encode("utf-8") # str to bytes stream
            
            # upload to MinIO
            self.client.put_object(
                bucket_name= self.bucket,
                object_name = path,
                data = io.BytesIO(code_bytes),
                length = len(code_bytes),
                content_type = "text/typescript-jsx"
            )
            return f"http://localhost:{os.getenv("MINIO_CONSOLE_PORT")}/{self.bucket}/{path}"
            
        except S3Error:
            raise
        except Exception:
            raise
    
    def save_img(self, img: str, path: str):
        try:    
            # base64 to binary stream
            if img.startswith("data:image"):
                img_base64 = img.split(",")[1]
            else:
                img_base64 = img
            img_bytes = base64.b64decode(img_base64, validate=True)
            
            # upload to Minio
            self.client.put_object(
                bucket_name = self.bucket,
                object_name = path,
                data = io.BytesIO(img_bytes),
                length=len(img_bytes),
                content_type="image/png"
            )
            return f"http://localhost:{os.getenv("MINIO_CONSOLE_PORT")}/{self.bucket}/{path}"
            
        except S3Error:
            raise
        except Exception:
            raise

    def check_storage_health(self):
        try:
            self._create_bucket(self.client, self.bucket)
            print(f"MinIO 检查通过！使用桶：{self.bucket}")
        except S3Error as e:
            raise
