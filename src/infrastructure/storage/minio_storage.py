import os
import io
import base64

from minio import Minio
from minio.error import S3Error

minio_client = None


def _get_minio_client():
    global minio_client
    if minio_client is None:
        try:
            minio_client = Minio(
                endpoint=f"{os.getenv("MINIO_HOST")}:{os.getenv("MINIO_PORT")}",
                access_key=os.getenv("MINIO_USER"),
                secret_key=os.getenv("MINIO_PASSWORD"),
                secure=False
            )
            _create_bucket(minio_client, os.getenv("MINIO_BUCKET"))
            
        except S3Error:
            raise
    return minio_client

def _create_bucket(client, bucket):
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)


def save_code(request_id: str, page_id: str, code: str):
    try: 
        client = _get_minio_client()
        bucket = os.getenv("MINIO_BUCKET")
        code_bytes = code.encode("utf-8") # str to bytes stream
        object_name = f"{request_id}/code/task_{page_id}.tsx"
        
        # upload to MinIO
        client.put_object(
            bucket_name= bucket,
            object_name = object_name,
            data = io.BytesIO(code_bytes),
            length = len(code_bytes),
            content_type = "text/typescript-jsx"
        )
        return f"http://localhost:{os.getenv("MINIO_CONSOLE_PORT")}/{bucket}/{object_name}"
        
    except S3Error as e:
        raise
    
    

def save_img(request_id: str, page_id: str, img: str):
    try:
        client = _get_minio_client() 
        bucket = os.getenv("MINIO_BUCKET")
        object_name = f"{request_id}/img/task_{page_id}.png"
        
        # base64 to binary stream
        if img.startswith("data:image"):
            img_base64 = img.split(",")[1]
        else:
            img_base64 = img
        img_bytes = base64.b64decode(img_base64, validate=True)
        
        # upload to Minio
        client.put_object(
            bucket_name = os.getenv("MINIO_BUCKET"),
            object_name = object_name,
            data = io.BytesIO(img_bytes),
            length=len(img_bytes),
            content_type="image/png"
        )
        return f"http://localhost:{os.getenv("MINIO_CONSOLE_PORT")}/{bucket}/{object_name}"
        
    except S3Error as e:
        raise
