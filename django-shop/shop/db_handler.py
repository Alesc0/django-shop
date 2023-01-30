import datetime
import sys
from pymongo import MongoClient
import os
import environ
from django.contrib.auth.models import User
from django.db import transaction
from shop.models import Product, Sales, Sales_Item, Billing, Shipping
from django.utils import timezone
import shop.cart as cartUtils
from django.db import connection

env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


client = MongoClient(env('MONGO_STRING'))
db = client.dbproj


def get_user(user_id):
    user = User.objects.get(id=user_id)
    mg = db.users.find_one({'_id': user_id})
    mg.update(user.__dict__)
    return user

def list_users():
    # pagination https://www.mongodb.com/docs/manual/reference/method/cursor.skip/
    users = []
    pg = User.objects.all()
    for mg_user in db.users.find():
        for pg_user in pg:
            if pg_user.id == mg_user['_id']:
                users.append({**mg_user, **pg_user.__dict__})
    return users


def create_user(username, password, first, last, email, _type=1, company=None, admin=False,is_active=True):
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first,
            last_name=last,
            is_superuser=admin,
            is_active=is_active
        )
        user.save()
    except:
        return None
    if _type != 3:
        db.users.insert_one({'_id': user.id, 'type': _type})
    else:
        db.users.insert_one(
            {'_id': user.id, 'type': _type, 'company': company})
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

def most_bought_today():
    pg = []
    res = []
    c = connection.cursor()
    
    try:
        c.execute("BEGIN")
        c.callproc("fn_most_bought_today")
        pg = c.fetchall()
    finally:
        c.close()
    for item in pg:
        res.append(db.products.find_one({"_id": item[0]}))
    print(res,file=sys.stderr) 
    return res

def create_order(user_id, cart):
    user = User.objects.get(id=user_id)
    sale = Sales(user=user,
                 state='billing info necessary',
                 date=timezone.now())
    sale.save()
    for item in cart:
        sales_item = Sales_Item.objects.create(
            sale=sale,
            product=item.product,
            price=item.product.price,
            promo=item.product.promo,
            quantity=item.quantity)
        sales_item.save()
    return sale


def link_billing(sale_id, nif, address, city, zip, country):
    sale = Sales.objects.get(id=sale_id)
    billing = Billing(sale=sale,
                      nif=nif,
                      address=address,
                      city=city,
                      zip=zip,
                      country=country)
    billing.save()
    sale.state = 'shipping info necessary'
    sale.save()
    return billing


def link_shipping(sale_id, address, city, zip, country):
    sale = Sales.objects.get(id=sale_id)
    shipping = Shipping(sale=sale,
                        address=address,
                        city=city,
                        zip=zip,
                        country=country)
    shipping.save()
    sale.state = 'awaiting approval'
    sale.save()
    return shipping


def get_orders(user_id):
    user = User.objects.get(id=user_id)
    sales = Sales.objects.filter(user=user).order_by('-date')

    for sale in sales:
        sale.products = []
        for item in Sales_Item.objects.filter(sale=sale):
            product = db.products.find_one({'_id': item.product.id})
            product.update(item.product.__dict__)
            product.update(item.__dict__)
            sale.products.append(product)
    return sales


def validate_sale_id(user_id, sale_id):
    user = User.objects.get(id=user_id)
    try:
        sale = Sales.objects.get(id=sale_id, user=user)
        return True
    except:
        return False
