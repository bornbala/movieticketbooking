
import certifi
from . import utils as Utils
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def get_db_handle():
    db = None
    uri = Utils.read_properties().get('mongodb_url').data
    print(uri)
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db = client['test_database']
    except Exception as e:
        print(e)
    return db

def insert_test(data):
    db = get_db_handle()
    if db != None:
        test_collection = db['test_collection']
        return test_collection.insert_one({"email":data.get('email'),"password":data.get('password')})


def insert_user(data):
    db = get_db_handle()
    if db != None:
        user_collection = db['user_collection']
        return user_collection.insert_one({"email":data.get('email'),"password":data.get('password')})
