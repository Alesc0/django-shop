import datetime
import sys
from pymongo import MongoClient
import os
import environ
from django.contrib.auth.models import User
from django.db import transaction
from shop.models import Product, Sales, Sales_Item

env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


client = MongoClient(env('MONGO_STRING'))
db = client.dbproj


def get_user(user_id):
    return db.users.find_one({'_id': user_id})


def list_users():
    # pagination https://www.mongodb.com/docs/manual/reference/method/cursor.skip/
    users = []
    pg = User.objects.all()
    for mg_user in db.users.find():
        for pg_user in pg:
            if pg_user.id == mg_user['_id']:
                users.append({**mg_user, **pg_user.__dict__})
    return users


def create_user(username, password, first, last, email, _type=1, company=None, admin=False):
    user = User.objects.create_user(username=username, password=password,
                                    email=email, first_name=first, last_name=last, is_superuser=admin)
    user.save()

    if _type == 1:
        db.users.insert_one({'_id': user.id, 'type': _type})
    else:
        db.users.insert_one(
            {'_id': user.id, 'type': _type, 'company': company})
    return user


def create_comercial(username, password, first, last, email, _type, company):
    user = User.objects.create_user(
        username=username, password=password, email=email, first_name=first, last_name=last,)
    user.save()
    db.users.insert_one({'_id': user.id, 'type': _type, 'company': company})
    return user


def create_product(name, description, price, stock,  image):
    product = Product(price=price, stock=stock, promo=0)
    product.save()
    return db.products.insert_one({"_id": product.id, 'name': name, 'description': description, 'image': image})


def get_product(product_id):
    pg = Product.objects.get(id=product_id)
    mg = db.products.find_one({'_id': int(product_id)})
    product = {**mg, **pg.__dict__}
    return product, pg


def list_products():
    products = []
    pg = Product.objects.all()
    for product in db.products.find():
        for p in pg:
            if p.id == product["_id"]:
                product["price"] = p.price
                product["stock"] = p.stock
        products.append(product)
    return products


@transaction.atomic
def create_order(user, cart):
    usr = User.objects.get(id=user)
    sale = Sales(user=usr, state='pending', date=datetime.datetime.now())
    sale.save()
    for item in cart:
        product = Product.objects.get(id=item['product_id'])
        sales_item = Sales_Item.objects.create(
            sale=sale, product=product, price=item['price'], promo=item['promo'], quantity=item['quantity'])
        sales_item.save()
    return 0
