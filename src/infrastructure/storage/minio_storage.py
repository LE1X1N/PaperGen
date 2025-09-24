import os
import io
import base64

from minio import Minio
from minio.error import S3Error


class MinioStorage:
    
    def __init__(self):
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


    def save_code(self, request_id: str, page_id: str, code: str):
        try: 
            code_bytes = code.encode("utf-8") # str to bytes stream
            object_name = f"{request_id}/code/task_{page_id}.tsx"
            
            # upload to MinIO
            self.client.put_object(
                bucket_name= self.bucket,
                object_name = object_name,
                data = io.BytesIO(code_bytes),
                length = len(code_bytes),
                content_type = "text/typescript-jsx"
            )
            return f"http://localhost:{os.getenv("MINIO_CONSOLE_PORT")}/{self.bucket}/{object_name}"
            
        except S3Error as e:
            raise
    
    
    def save_img(self, request_id: str, page_id: str, img: str):
        try:
            object_name = f"{request_id}/img/task_{page_id}.png"
            
            # base64 to binary stream
            if img.startswith("data:image"):
                img_base64 = img.split(",")[1]
            else:
                img_base64 = img
            img_bytes = base64.b64decode(img_base64, validate=True)
            
            # upload to Minio
            self.client.put_object(
                bucket_name = self.bucket,
                object_name = object_name,
                data = io.BytesIO(img_bytes),
                length=len(img_bytes),
                content_type="image/png"
            )
            return f"http://localhost:{os.getenv("MINIO_CONSOLE_PORT")}/{bucket}/{object_name}"
            
        except S3Error as e:
            raise


    def check_storage_health(self):
        try:
            self._create_bucket(self.client, self.bucket)
        except S3Error as e:
            raise