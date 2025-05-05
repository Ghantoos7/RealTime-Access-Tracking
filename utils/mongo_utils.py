from pymongo import MongoClient
from .config import MONGO_URI, MONGO_DB

def get_mongo_collection(collection_name):
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[collection_name]
