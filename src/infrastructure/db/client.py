import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# global mongodb client
mongo_client = None

def _get_mongo_client():
    global mongo_client
    if mongo_client is None:
        try:
            mongo_client = MongoClient(f"mongodb://{os.getenv("MONGODB_USER")}:{os.getenv("MONGODB_PASSWORD")}@{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/")
        except PyMongoError:
            raise
    return mongo_client
            
            
def get_mongo_collection():
    # init once
    try:
        client = _get_mongo_client()
        db = client[os.getenv("MONGODB_DB")]
        collection = db[os.getenv("MONGODB_COLLECTION")]
        return collection
    except PyMongoError:
        raise

def check_mongodb_health():
    try:
        client = _get_mongo_client()
        client.admin.command("ping")
        
        db = client[os.getenv("MONGODB_DB")]
        collection = db[os.getenv("MONGODB_COLLECTION")]
        count = collection.count_documents({})  # try to read
        print(f"MongoDB 检查通过！当前存储条目: {count}")
    except PyMongoError:
        raise
    