import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.config import conf

# global mongodb client
mongo_client = None

def _get_mongo_client():
    global mongo_client
    if mongo_client is None:
        try:
            mongo_client = MongoClient(os.getenv("MONGODB_URI"))
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
        return count
    except PyMongoError:
        raise
    