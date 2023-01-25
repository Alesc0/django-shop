import sys
from pymongo import MongoClient
import os
import environ
from bson.objectid import ObjectId

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

def create_user(user_id, username, email,_type=1,company=None):
    if company is None:
        return db.users.insert_one({'_id': user_id,'username': username, 'email': email, 'type': _type})
    return db.users.insert_one({'_id': user_id,'username': username, 'email': email, 'type': _type, "company": company})

def create_product(name, price, description, image):
    return db.products.insert_one({'name': name, 'price': price, 'description': description, 'image': image})

def get_product(product_id):
    return db.products.find_one({'_id': ObjectId(product_id)})


def list_products():
    return db.products.find()