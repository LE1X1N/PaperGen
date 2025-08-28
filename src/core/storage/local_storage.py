import base64
from pathlib import Path

from src.config import conf


LOCAL_FILE_DIR = conf["service"]["local_file_dir"]

def get_local_request_dir(request_id):
    return Path(LOCAL_FILE_DIR) / request_id
    
# def _get_request_dict_path(self, request_id):
#     return _get_request_dir(request_id) /  self.request_dict_name


def save_code(request_id: str, page_id: str, code: str):
    file_path = get_local_request_dir(request_id) / f"task_{page_id}.jsx"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return file_path

def save_img(request_id: str, page_id: str, img: str):
    """
        img: Base64 encoded images
    """
    file_path = get_local_request_dir(request_id) / f"task_{page_id}.png"
    
    if img.startswith("data:image"):
        img_base64 = img.split(",")[1]
    else:
        img_base64 = img
    
    # base64 to binary stream
    img_bytes = base64.b64decode(img_base64, validate=True)
    with open(file_path, "wb") as f:  
        f.write(img_bytes)
    
    return file_path

