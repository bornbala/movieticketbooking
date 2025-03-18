
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
        db = client[Utils.read_properties().get('database_name').data]
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
    
def get_user_by_email(data):
    db = get_db_handle()
    if db != None:
        user_collection = db['user_collection']
        user = user_collection.find_one({"email":data.get('email')})
        return user


def insert_otp(email,otp):
    db = get_db_handle()
    if db != None:
        otp_collection = db['otp_collection']
        otp = otp_collection.find_one_and_update({"email":email},{"$set":{"otp":otp}},upsert=True)
        print(otp)
        return otp


def verify_otp(data):
    db = get_db_handle()
    if db != None:
        verify_otp_collection = db['otp_collection']
        verify_otp_data = verify_otp_collection.find_one({'email':data.get('email')},{'_id':0})
        if(verify_otp_data != None):
            stored_otp = verify_otp_data.get('otp')
            if(stored_otp == data.get('otp')):
                return True
            else:
                return False
        else:
            return False
        

def delete_otp(data):
    db = get_db_handle()
    if db != None:
        verify_otp_collection = db['otp_collection']
        response = verify_otp_collection.delete_one({'email':data.get('email')})
        print(response.deleted_count)