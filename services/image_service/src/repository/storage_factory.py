from src.config import conf

from src.infrastructure.storage import LocalStorage, MinioStorage

def get_storage():
    backend = conf["service"]["storage"]["type"]
    if backend == "local":
        return LocalStorage(conf["service"]["storage"]["local"]["base_dir"])
    elif backend == "minio":
        return MinioStorage()