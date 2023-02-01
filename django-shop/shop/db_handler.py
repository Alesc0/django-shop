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
    if mg != None:
        mg.update(user.__dict__)
    return mg

def list_users(user_id,filter=None):
    # pagination https://www.mongodb.com/docs/manual/reference/method/cursor.skip/
    users = []
    if filter != None:
        pg = User.objects.filter(first_name__icontains = filter) | User.objects.filter(last_name__icontains = filter) | User.objects.filter(email__icontains = filter)
    else :
        pg = User.objects.all()
        
    mg = db.users.find()
    for mg_user in mg:
        for pg_user in pg:
            if pg_user.id == mg_user['_id'] and mg_user['_id'] != user_id:
                users.append({**mg_user, **pg_user.__dict__})
    return users


def create_user(username, password, first_name, last_name, email, _type=1,admin=False, company=None,is_active=True):
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_superuser=admin,
            is_active=is_active
        )
        user.save()
    except Exception as e:
        print(e, file=sys.stderr)
        return None
    if _type != 3:
        db.users.insert_one({'_id': user.id, 'type': _type})
    else:
        db.users.insert_one(
            {'_id': user.id, 'type': _type, 'company': company})
    return user

def edit_user(id, username, first_name, last_name, email, _type=1,admin=False, company=None,is_active=True,reset_password=None):
    try:
        user = User.objects.get(id=id)
        user.username=username
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.is_superuser=admin
        user.is_active=is_active
        if reset_password != None:
            user.set_password(reset_password)
        user.save()
    except Exception as e:
        print(e, file=sys.stderr)
        return None
    if _type != 3:
        db.users.update_one({'_id': user.id}, {'$set': {'type': _type}})
    else:
        db.users.update_one({'_id': user.id}, {'$set': {'type': _type, 'company': company}})
    return user



def create_product(name, description, price, stock,  image,user_id):
    mg_user = db.users.find_one({'_id': user_id})
    product = Product(price=price, stock=stock, promo=0)
    product.save()
    data = {}
    data['_id'] = product.id
    data['name'] = name
    data['description'] = description
    data['image'] = image
    if mg_user['type'] == 3:
        data['sold_by'] = mg_user['company']
    return db.products.insert_one(data)

def edit_product(id, name, description, price, stock,  image):
    product = Product.objects.get(id=id)
    product.price = price
    product.stock = stock
    product.save()
    data = {}
    data['_id'] = product.id
    data['name'] = name
    data['description'] = description
    if image != None:
        data['image'] = image
    return db.products.update_one({"_id": product.id}, {'$set': data})

def get_product(product_id):
    pg = Product.objects.get(id=product_id)
    mg = db.products.find_one({'_id': int(product_id)})
    product = {**mg, **pg.__dict__}
    return product, pg


def list_products(user_id=None,filter=None):
    final_products = []
    pg = Product.objects.all()
    
    if user_id != None:
        mg_user = db.users.find_one({'_id': user_id})
        products = db.products.find({'sold_by': mg_user['company']})
    else:
        if filter != None:
            products = db.products.find({"name": {"$regex": filter, "$options": "i"}})
        else:
            products = db.products.find()
    
    for product in products:
        for p in pg:
            if p.id == product["_id"]:
                product["price"] = p.price
                product["stock"] = p.stock
        final_products.append(product)
    return final_products

def most_bought_date(date1,date2,lim):
    pg = []
    res = []
    c = connection.cursor()
    
    try:
        c.execute("BEGIN")
        c.callproc("fn_most_bought_date", (date1,date2,lim))
        pg = c.fetchall()
        c.execute("COMMIT")
    finally:
        c.close()
        for item in pg:
            res.append(db.products.find_one({"_id": item[0]}))
    return res

def get_products_in_promo():
    pg = []
    res = []
    c = connection.cursor()
    
    try:
        c.execute("BEGIN")
        c.callproc("fn_products_in_promo")
        pg = c.fetchall()
        c.execute("COMMIT")
    finally:
        c.close()
        for item in pg:
            res.append(db.products.find_one({"_id": item[0]}))
    return res

def get_product_orders(product_id):
    pg = []
    res = []
    c = connection.cursor()
    
    try:
        c.execute("BEGIN")
        c.callproc("fn_get_orders_for_product", (product_id,))
        pg = c.fetchall()
        c.execute("COMMIT")
    finally:
        c.close()
        
    for item in pg:
        i = {}
        i['id'] = item[0]
        i['user_id'] = item[1]
        i['buyer'] = item[2] + ' ' + item[3]
        i['quantity'] = item[4]
        i['price'] = item[5]
        i['date'] = item[6]
        res.append(i)
        
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

def authorize_order (user_id,id):
    auth_user = User.objects.get(id=user_id)
    sale = Sales.objects.get(id=id)
    sale.state = 'Authorized'
    sale.auth_user = auth_user
    sale.save()
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

def cancel_order(user_id, sale_id):
    user = User.objects.get(id=user_id)
    sale = Sales.objects.get(id=sale_id, user=user)
    sale.state = 'canceled'
    sale.save()
    return sale

def search(user_id,search):
    products = list_products(filter=search)
    users = list_users(user_id,filter=search)
    return products, users
    