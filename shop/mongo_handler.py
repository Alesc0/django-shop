from pymongo import MongoClient
import os
import environ

env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


client = MongoClient(env('MONGO_STRING'))
db = client.dbproj

def get_user(user_id):
    return db.users.find_one({'_id': user_id})

def list_users():
    #pagination https://www.mongodb.com/docs/manual/reference/method/cursor.skip/
    return db.users.find()

def create_user(user_id, username, email,type=1):
    return db.users.insert_one({'_id': user_id,'username': username, 'email': email, 'type': type})


def create_product(name, price, description):
    return db.products.insert_one({'name': name, 'price': price, 'description': description})

def list_products():
    return db.products.find()