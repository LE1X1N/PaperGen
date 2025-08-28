from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.config import conf

def get_mongo_collection():
    client = MongoClient(conf["mongodb"]["uri"])
    db = client[conf["mongodb"]["db_name"]]
    collection = db[conf["mongodb"]["collection_name"]]
    return collection

def check_mongodb_health():
    try:
        client = MongoClient(conf["mongodb"]["uri"])
        client.admin.command("ping")
        
        db = client[conf["mongodb"]["db_name"]]
        collection = db[conf["mongodb"]["collection_name"]]
        count = collection.count_documents({})  # try to read
        return count
    except PyMongoError:
        raise
    