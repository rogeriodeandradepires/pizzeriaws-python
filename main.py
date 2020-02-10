# -*- coding: utf-8 -*-
import itertools

from flask import Flask, jsonify, request, render_template
import os
import io
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials, firestore
from google.cloud import storage
from PIL import Image
import requests
from io import BytesIO
import urllib.request as req
from PIL import Image
import glob
import json
import base64
import threading
from datetime import datetime
# from sqlalchemy import create_engine
# from flask_mysqldb import MySQL
from products import Product
from users import User
from datetime import date
from ast import literal_eval
from decimal import Decimal
import pysftp
import sys
import uuid

app = Flask(__name__)
# application.config['MYSQL_HOST'] = 'aad4ceauedwkx7.ctvp1qfizfsm.us-east-2.rds.amazonaws.com'
# application.config['MYSQL_USER'] = 'root'
# application.config['MYSQL_PASSWORD'] = '27031984As'
# application.config['MYSQL_DB'] = 'ebdb'

# mysql = MySQL(application)

cred = credentials.Certificate("dom-marino-ws-firebase-adminsdk-x049u-1128490a39.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dom-marino-ws-firebase-adminsdk-x049u-1128490a39.json"
firebase_admin.initialize_app(cred)
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://dom-marino-ws.firebaseio.com/',
#     'storageBucket': 'dom-marino-ws.appspot.com'
# })

# category = 'non_alcoholic_beverages'
# category = 'alcoholic_beverages'
# category = 'beers'
# category = 'candy_pizzas'
# category = 'flapts'
category = 'gourmet_pizzas'
# category = 'pizza_edges'
# category = 'traditional_pizzas'
# category = 'wines'
document_id = ''
imageurl = ''
thumbnailurl = ''

client = storage.Client()
# https://console.cloud.google.com/storage/browser/[bucket-id]/
bucket = client.get_bucket('dom-marino-ws.appspot.com')
# Then do other things...
# blob = bucket.get_blob('categories/beers/beer_icon.png')
# # print(blob.download_as_string())
# blob.upload_from_file('pictures/products/')
# blob2 = bucket.blob('products/' + category + document_id)
# blob2.upload_from_filename(filename='teste.txt')

# imgurl ="https://i.pinimg.com/originals/68/7c/ec/687cec1f523e3ee2b666c38e055a4d6d.png"
# req.urlretrieve(imgurl, "soft_drinks.png")


db = firestore.client()
todo_ref = db.collection('todos')
categories_ref = db.collection('categories')
users_ref = db.collection('users')
orders_ref = db.collection('orders')
non_alcoholic_beverages_ref = db.collection('products').document('non_alcoholic_beverages').collection(
    'non_alcoholic_beverages')
alcoholic_beverages_ref = db.collection('products').document('alcoholic_beverages').collection('alcoholic_beverages')
beers_ref = db.collection('products').document('beers').collection('beers')
candy_pizzas_ref = db.collection('products').document('candy_pizzas').collection('candy_pizzas')
flapts_ref = db.collection('products').document('flapts').collection('flapts')
gourmet_pizzas_ref = db.collection('products').document('gourmet_pizzas').collection('gourmet_pizzas')
pizza_edges_ref = db.collection('products').document('pizza_edges').collection('pizza_edges')
traditional_pizzas_ref = db.collection('products').document('traditional_pizzas').collection('traditional_pizzas')
wines_ref = db.collection('products').document('wines').collection('wines')
promotions_ref = db.collection('products').document('promotions').collection('promotions')
two_flavored_pizzas_ref = db.collection('products').document('two_flavored_pizzas').collection('two_flavored_pizzas')
users_ref = db.collection('users')
# get all the png files from the current folder
# for infile in glob.glob("*.png"):
# for infile in glob.glob("soft_drinks.png"):
#   im = Image.open(infile)

#   # don't save if thumbnail already exists
#   if infile[0:2] != "T_":
#     # prefix thumbnail file with T_
#     im.save("T_" + infile, "PNG")
#
# data = {}
# with open('T_soft_drinks.png', mode='rb') as file:
#     img = file.read()
# data['img'] = base64.encodebytes(img).decode("utf-8")
#
# print(json.dumps(data))

accounts = [
    {'name': "Billy", 'balance': 450.0},
    {'name': "Kelly", 'balance': 250.0}
]

all_categories = []
all_non_alcoholic_beverages = []
all_alcoholic_beverages = []
all_beers = []
all_pizza_edges = []
all_flapts = []
all_candy_pizzas = []
all_gourmet_pizzas = []
all_traditional_pizzas = []
all_wines = []
all_promotions = []
all_two_flavored_pizzas = []
all_orders = []
all_users = []


# HTTP GET
# HTTP POST
# HTTP PUT
# HTTP DELETE
# HTTP PATCH

# @app.route('/heroes', methods=['POST'])
# def create_hero():
#     req = request.json
#     hero = SUPERHEROES.push(req)
#     return jsonify({'id': hero.key}), 201
# Create a callback on_snapshot function to capture changes


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))


def on_categories_snapshot(doc_snapshot, changes, read_time):
    # print("entrou")
    # print("on_categories_snapshot, closed=", cat_watch._closed)

    global all_categories
    all_categories = []

    for doc in doc_snapshot:
        category = doc.to_dict()
        all_categories.append(category)
        # print(category["description"])


def on_nab_snapshot(doc_snapshot, changes, read_time):
    global all_non_alcoholic_beverages
    all_non_alcoholic_beverages = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = non_alcoholic_beverages_ref.document(doc.id).collection('images').stream()
        price_broto_stream = non_alcoholic_beverages_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = non_alcoholic_beverages_ref.document(doc.id).collection('prices').document(
            'inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_non_alcoholic_beverages.append(product)


def on_ab_snapshot(doc_snapshot, changes, read_time):
    global all_alcoholic_beverages
    all_alcoholic_beverages = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = alcoholic_beverages_ref.document(doc.id).collection('images').stream()
        price_broto_stream = alcoholic_beverages_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = alcoholic_beverages_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_alcoholic_beverages.append(product)


def on_beers_snapshot(doc_snapshot, changes, read_time):
    global all_beers
    all_beers = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = beers_ref.document(doc.id).collection('images').stream()
        price_broto_stream = beers_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = beers_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_beers.append(product)


def on_candy_pizzas_snapshot(doc_snapshot, changes, read_time):
    global all_candy_pizzas
    all_candy_pizzas = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = candy_pizzas_ref.document(doc.id).collection('images').stream()
        price_broto_stream = candy_pizzas_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = candy_pizzas_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_candy_pizzas.append(product)


def on_flapts_snapshot(doc_snapshot, changes, read_time):
    global all_flapts
    all_flapts = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = flapts_ref.document(doc.id).collection('images').stream()
        price_broto_stream = flapts_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = flapts_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_flapts.append(product)


def on_pizza_edges_snapshot(doc_snapshot, changes, read_time):
    global all_pizza_edges
    all_pizza_edges = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = pizza_edges_ref.document(doc.id).collection('images').stream()
        price_broto_stream = pizza_edges_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = pizza_edges_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_pizza_edges.append(product)


def on_traditional_pizzas_snapshot(doc_snapshot, changes, read_time):
    global all_traditional_pizzas
    all_traditional_pizzas = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = traditional_pizzas_ref.document(doc.id).collection('images').stream()
        price_broto_stream = traditional_pizzas_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = traditional_pizzas_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_traditional_pizzas.append(product)


def on_gourmet_pizzas_snapshot(doc_snapshot, changes, read_time):
    global all_gourmet_pizzas
    all_gourmet_pizzas = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = gourmet_pizzas_ref.document(doc.id).collection('images').stream()
        price_broto_stream = gourmet_pizzas_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = gourmet_pizzas_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_gourmet_pizzas.append(product)


def on_wines_snapshot(doc_snapshot, changes, read_time):
    global all_wines
    all_wines = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = wines_ref.document(doc.id).collection('images').stream()
        price_broto_stream = wines_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = wines_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_wines.append(product)


def on_promotions_snapshot(doc_snapshot, changes, read_time):
    global all_promotions
    all_promotions = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = promotions_ref.document(doc.id).collection('images').stream()
        price_broto_stream = promotions_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = promotions_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_promotions.append(product)


def on_two_flavored_pizzas_snapshot(doc_snapshot, changes, read_time):
    global all_two_flavored_pizzas
    all_two_flavored_pizzas = []

    for doc in doc_snapshot:
        product = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        images = two_flavored_pizzas_ref.document(doc.id).collection('images').stream()
        price_broto_stream = two_flavored_pizzas_ref.document(doc.id).collection('prices').document('broto').get()
        price_inteira_stream = two_flavored_pizzas_ref.document(doc.id).collection('prices').document('inteira').get()

        price_broto = price_broto_stream.to_dict().get('price', '')
        price_inteira = price_inteira_stream.to_dict().get('price', '')

        if price_broto != None:
            product.update({'price_broto': price_broto})
        else:
            product.update({'price_broto': None})

        if price_inteira != None:
            product.update({'price_inteira': price_inteira})
        else:
            product.update({'price_inteira': None})

        for image in images:
            product.update({'image': image.to_dict().get('url', '')})
            # doc.collection('images').on_snapshot(on_nab_images_snapshot)

        all_two_flavored_pizzas.append(product)


def on_users_snapshot(doc_snapshot, changes, read_time):
    global all_users
    all_users = []

    for doc in doc_snapshot:
        user = doc.to_dict()
        # print(u'Document snapshot: {}'.format(doc.to_dict()))
        # product = Product.from_dict(doc.to_dict())
        all_users.append(user)


# Watch the document
cat_watch = categories_ref.on_snapshot(on_categories_snapshot)
nab_watch = non_alcoholic_beverages_ref.on_snapshot(on_nab_snapshot)
ab_watch = alcoholic_beverages_ref.on_snapshot(on_ab_snapshot)
beers_watch = beers_ref.on_snapshot(on_beers_snapshot)
candy_pizzas_watch = candy_pizzas_ref.on_snapshot(on_candy_pizzas_snapshot)
flapts_watch = flapts_ref.on_snapshot(on_flapts_snapshot)
pizza_edges_watch = pizza_edges_ref.on_snapshot(on_pizza_edges_snapshot)
traditional_pizzas_watch = traditional_pizzas_ref.on_snapshot(on_traditional_pizzas_snapshot)
gourmet_pizzas_watch = gourmet_pizzas_ref.on_snapshot(on_gourmet_pizzas_snapshot)
wines_watch = wines_ref.on_snapshot(on_wines_snapshot)
promotions_watch = promotions_ref.on_snapshot(on_promotions_snapshot)
two_flavored_pizzas_watch = two_flavored_pizzas_ref.on_snapshot(on_two_flavored_pizzas_snapshot)
users_watch = users_ref.on_snapshot(on_users_snapshot)


def monitor_watches():
    global cat_watch
    global nab_watch
    global ab_watch
    global beers_watch
    global candy_pizzas_watch
    global flapts_watch
    global pizza_edges_watch
    global traditional_pizzas_watch
    global gourmet_pizzas_watch
    global wines_watch
    global promotions_watch
    global two_flavored_pizzas_watch
    global users_watch

    threading.Timer(30.0, monitor_watches).start()

    if cat_watch._closed:
        cat_watch = categories_ref.on_snapshot(on_categories_snapshot)

    if nab_watch._closed:
        nab_watch = non_alcoholic_beverages_ref.on_snapshot(on_nab_snapshot)

    if ab_watch._closed:
        ab_watch = alcoholic_beverages_ref.on_snapshot(on_ab_snapshot)

    if beers_watch._closed:
        beers_watch = beers_ref.on_snapshot(on_beers_snapshot)

    if candy_pizzas_watch._closed:
        candy_pizzas_watch = candy_pizzas_ref.on_snapshot(on_candy_pizzas_snapshot)

    if flapts_watch._closed:
        flapts_watch = flapts_ref.on_snapshot(on_flapts_snapshot)

    if pizza_edges_watch._closed:
        pizza_edges_watch = pizza_edges_ref.on_snapshot(on_pizza_edges_snapshot)

    if traditional_pizzas_watch._closed:
        traditional_pizzas_watch = traditional_pizzas_ref.on_snapshot(on_traditional_pizzas_snapshot)

    if gourmet_pizzas_watch._closed:
        gourmet_pizzas_watch = gourmet_pizzas_ref.on_snapshot(on_gourmet_pizzas_snapshot)

    if wines_watch._closed:
        wines_watch = wines_ref.on_snapshot(on_wines_snapshot)

    if promotions_watch._closed:
        promotions_watch = promotions_ref.on_snapshot(on_promotions_snapshot)

    if two_flavored_pizzas_watch._closed:
        two_flavored_pizzas_watch = two_flavored_pizzas_ref.on_snapshot(on_two_flavored_pizzas_snapshot)

    if users_watch._closed:
        users_watch = users_ref.on_snapshot(on_users_snapshot)


monitor_watches()


def setImageUrl(url):
    global imageurl
    imageurl = url


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/accounts", methods=["GET"])
def getAccounts():
    return jsonify(accounts)


# @app.route("/img", methods=["GET"])
# def getImages():
#     return json.dumps(data)


@app.route("/account/<id>", methods=["GET"])
def getAccount(id):
    id = int(id) - 1
    return jsonify(accounts[id])


@app.route("/add", methods=['GET', 'POST'])
def create():
    """
            create() : Add document to Firestore collection with request body
            Ensure you pass a custom ID as part of json body in post request
            e.g. json={'id': '1', 'title': 'Write a blog post'}
        """
    try:
        data = {
            u'name': u'Los Angeles',
            u'state': u'CA',
            u'country': u'USA'
        }
        # id = request.json['id']
        id = todo_ref.document().id
        user = User(uid=u'Tokyo', register_date=u'21/09/2019', main_address_id=u'main_address_id', image=u'image',
                    name=u'Tokyo', phone=None, email=u'Japan')
        todo_ref.add(user.to_dict())
        # todo_ref.document(id).set(request.json)
        # todo_ref.document(id).set(data)
        # todo_ref.add(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route("/makeorder", methods=['POST'])
def makeorder():

    # dd/mm/YY
    # today = datetime.now()
    # # today = today.strftime("%d-%m-%Y")
    # today = today.strftime("%Y-%m-%d %H:%M:%S")

    today = request.get_json().get('date_time')


    startdata = {
        u'id': u'{0}'.format(today)
    }

    thisOrderRef = orders_ref.document(today)

    thisOrderRef.set(startdata)
    thisOrderRef = thisOrderRef.collection(today)
    order_ref_for_update = thisOrderRef

    # print("hoje é: {0}".format(today))

    try:
        coupon_id = request.get_json().get('coupon_id')
        delivery = request.get_json().get('delivery')
        payment_method = request.get_json().get('payment_method')
        total = request.get_json().get('total')
        userId = request.get_json().get('userId')
        id = thisOrderRef.document().id
        products_id = request.get_json().get('products_id')

        # print(products_id)

        data = {
            u'coupon_id': u'{}'.format(coupon_id),
            u'dateTime': u'{}'.format(today),
            u'id': u'{}'.format(id),
            u'delivery': u'{}'.format(delivery),
            u'payment_method': u'{}'.format(payment_method),
            u'total': u'{}'.format(total),
            u'userId': u'{}'.format(userId)
        }

        thisOrderRef.document(id).set(data)
        thisOrderRef = thisOrderRef.document(id).collection('products_id')

        #product.update({'price_broto': None})
        # product_dict = literal_eval(products_id)
        json_acceptable_string = products_id.replace("'", "\"")
        product_dict = json.loads(json_acceptable_string)
        # print(product_dict)

        total_paid = Decimal('0.00')

        for key, value in product_dict.items():
            product = value
            thisId = thisOrderRef.document().id

            paid_price = 0.00
            pizza_edge_price = 0.00
            pizza_edge_description = ""
            product_description = ""
            img_url = ""
            all_items = []

            if product.get("isTwoFlavoredPizza") == 0:
                if product.get("product1_category") == "beers":
                    all_items.extend(all_beers)
                elif product.get("product1_category") == "alcoholic_beverages":
                    all_items.extend(all_alcoholic_beverages)
                elif product.get("product1_category") == "flapts":
                    all_items.extend(all_flapts)
                elif product.get("product1_category") == "non_alcoholic_beverages":
                    all_items.extend(all_non_alcoholic_beverages)
                elif product.get("product1_category") == "promotions":
                    all_items.extend(all_promotions)
                elif product.get("product1_category") == "wines":
                    all_items.extend(all_wines)
                elif product.get("product1_category") == "candy_pizzas":
                    all_items.extend(all_candy_pizzas)
                elif product.get("product1_category") == "gourmet_pizzas":
                    all_items.extend(all_gourmet_pizzas)
                elif product.get("product1_category") == "traditional_pizzas":
                    all_items.extend(all_traditional_pizzas)

                if "pizza" not in product.get("product1_category"):
                    for item in all_items:
                        if item.get('id') == product.get("product_id"):
                            paid_price = item.get("price")
                            product_description = item.get('description')
                            img_url = item.get('image')

                else:
                    if product.get("pizza_edge_id") != "null":
                        for pizza_edge in all_pizza_edges:
                            if pizza_edge.get('id') == product.get("pizza_edge_id"):
                                pizza_edge_description = pizza_edge.get("description")
                                if product.get("size") == "Broto":
                                    pizza_edge_price = pizza_edge.get("price_broto")
                                if product.get("size") == "Inteira":
                                    pizza_edge_price = pizza_edge.get("price_inteira")

                    for item in all_items:
                        if item.get('id') == product.get("product_id"):
                            product_description = item.get('description')
                            img_url = item.get('image')

                            if product.get("size") == "Broto":
                                paid_price = item.get("price_broto")
                            if product.get("size") == "Inteira":
                                paid_price = item.get("price_inteira")

                    new_price = Decimal(paid_price)+Decimal(pizza_edge_price)
                    paid_price = round(new_price, 2)
            else:
                product1_price = 0.00
                product2_price = 0.00

                if product.get("pizza_edge_id") != "null":
                    for pizza_edge in all_pizza_edges:
                        if pizza_edge.get('id') == product.get("pizza_edge_id"):
                            pizza_edge_description = pizza_edge.get("description")
                            if product.get("size") == "Broto":
                                pizza_edge_price = pizza_edge.get("price_broto")
                            if product.get("size") == "Inteira":
                                pizza_edge_price = pizza_edge.get("price_inteira")

                if product.get("product1_category") == "traditional_pizzas":
                    all_items.extend(all_traditional_pizzas)
                elif product.get("product1_category") == "gourmet_pizzas":
                    all_items.extend(all_gourmet_pizzas)
                elif product.get("product1_category") == "candy_pizzas":
                    all_items.extend(all_candy_pizzas)

                for product1 in all_items:
                    if product1.get('id') == product.get("product_id"):
                        product_description = product1.get('description')
                        img_url = "https://storage.googleapis.com/dom-marino-ws.appspot.com/categories/custom/two_flavored_pizza_image.png"

                        if product.get("size") == "Broto":
                            product1_price = product1.get("price_broto")
                        if product.get("size") == "Inteira":
                            product1_price = product1.get("price_inteira")

                all_items = []
                if product.get("product2_category") == "traditional_pizzas":
                    all_items.extend(all_traditional_pizzas)
                elif product.get("product2_category") == "gourmet_pizzas":
                    all_items.extend(all_gourmet_pizzas)
                elif product.get("product2_category") == "candy_pizzas":
                    all_items.extend(all_candy_pizzas)

                for product2 in all_items:
                    if product2.get('id') == product.get("product2_id"):
                        product_description += " + "+product2.get('description')
                        if product.get("size") == "Broto":
                            product2_price = product2.get("price_broto")
                        if product.get("size") == "Inteira":
                            product2_price = product2.get("price_inteira")

                product1_decimal_price = Decimal(product1_price)
                product2_decimal_price = Decimal(product2_price)

                max_price = max(product1_decimal_price, product2_decimal_price)

                pizza_edge_decimal_price = Decimal(pizza_edge_price)
                max_price_decimal = Decimal(max_price)

                new_price = max_price_decimal+pizza_edge_decimal_price
                paid_price = new_price

            thisProduct = {
                u'category': u'{}'.format(product.get("category")),
                u'notes': u'{}'.format(product.get("notes")),
                u'id': u'{}'.format(thisId),
                u'paid_price': u'{}'.format(paid_price),
                u'pizza_edge_id': u'{}'.format(product.get("pizza_edge_id")),
                u'pizza_edge_description': u'{}'.format(pizza_edge_description),
                u'pizza_edge_paid_price': u'{}'.format(pizza_edge_price),
                u'product1_category': u'{}'.format(product.get("product1_category")),
                u'product2_category': u'{}'.format(product.get("product2_category")),
                u'product2_id': u'{}'.format(product.get("product2_id")),
                u'product_description': u'{}'.format(product_description),
                u'product_id': u'{}'.format(product.get("product_id")),
                u'product_image_url': u'{}'.format(img_url),
                u'quantity': u'{}'.format(product.get("quantity")),
                u'isTwoFlavoredPizza': u'{}'.format(product.get("isTwoFlavoredPizza")),
                u'size': u'{}'.format(product.get("size"))
            }

            total_paid += Decimal(paid_price)*Decimal(product.get("quantity"))
            
            thisOrderRef.document(thisId).set(thisProduct)

        order_ref_for_update.document(id).update({u'total': str(round(total_paid, 2))})


        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_user_orders', methods=['GET'])
def list_user_orders():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    all_orders=[]
    user_id = request.args.get('id')
    docSnapshot = orders_ref.stream()

    for doc in docSnapshot:
        data_stream = orders_ref.document(doc.id).collection(doc.id).where(u'userId', u'==', user_id).stream()

        for order in data_stream:
            thisOrder = order.to_dict()
            tempMap = dict()
            products_stream = orders_ref.document(doc.id).collection(doc.id).document(order.id).collection("products_id").stream()
            # thisProductDict = {}
            for product in products_stream:
                thisProduct = product.to_dict()
                # thisOrder["products_id"][product.id] = thisProduct
                tempMap[product.id] = thisProduct


            thisOrder.update({"products_id": tempMap})
            # print(thisProduct)

            all_orders.append(thisOrder)


    try:
        # Check if ID was passed to URL query
        return jsonify(all_orders), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list_categories', methods=['GET'])
def list_categories():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        cat_id = request.args.get('id')
        if cat_id:
            category = object
            for element in all_categories:
                if element['id'] == cat_id:
                    category = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(category), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_categories), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # user_id = users_ref.document().id

    # print("Posted file: {}".format(request.files['image_file']))
    # file = request.files['image_file']
    # files = {'file': file.read()}

    uid = request.form['uid']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    imgUrl = request.form['img_url']
    isRegisterComplete = request.form['isRegisterComplete']

    # print('entrou2', file=sys.stdout, flush=True)

    if request.form['hasImageFile'] == "True":
        image = request.files['image_file'].read()
        print('imagem não é nula', file=sys.stdout, flush=True)
        # print(u'Received document snapshot: {}'.format(doc.id))

        # session = ftplib.FTP_TLS('157.230.167.73', 'root', '27031984As')
        # # file = open('kitten.jpg', 'rb')  # file to send
        # session.storbinary('STOR /var/www/powermemes.com/dommarino/{}.jpg'.format(uid), image)  # send the file
        # image.close()  # close file and FTP
        # session.quit()

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(host='157.230.167.73', username='root', password='27031984As', cnopts=cnopts) as sftp:
            print("Connection succesfully stablished ... ")

            # Switch to a remote directory

            if not sftp.isdir('/var/www/powermemes.com/htdocs/dommarino/userimg/{}'.format(uid)):
                sftp.mkdir('/var/www/powermemes.com/htdocs/dommarino/userimg/{}'.format(uid))


            sftp.cwd('/var/www/powermemes.com/htdocs/dommarino/userimg/{}'.format(uid))

            img_id = str(uuid.uuid1())

            print('imge id={}'.format(img_id))

            f = sftp.open('/var/www/powermemes.com/htdocs/dommarino/userimg/{0}/{1}.png'.format(uid, img_id), 'wb')
            f.write(image)

            # sftp.put(image.file.name, '/var/www/powermemes.com/dommarino/{}.jpg'.format(uid))

        # print(products_id)
        imgUrl = "https://powermemes.com/dommarino/userimg/{0}/{1}.png".format(uid, img_id)

    elif imgUrl=="":
        imgUrl="https://powermemes.com/dommarino/userimg/avatar.png"

    data = {
        u'uid': u'{}'.format(uid),
        u'name': u'{}'.format(name),
        u'email': u'{}'.format(email),
        u'phone': u'{}'.format(phone),
        u'image_url': u'{}'.format(imgUrl),
        u'isRegisterComplete': u'{}'.format(isRegisterComplete),
    }

    users_ref.document(uid).set(data)

    print(data)
    return jsonify({"success": True}), 200
    # print(image)


@app.route('/list_users', methods=['GET'])
def list_users():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """

    try:
        # Check if ID was passed to URL query
        user_id = request.args.get('uid')

        if user_id:
            user_snapshot = users_ref.document(user_id).get()
            user = user_snapshot.to_dict()
            return jsonify(user), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_users), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_non_alcoholic_beverages', methods=['GET'])
def list_non_alcoholic_beverages():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        nab_id = request.args.get('id')
        if nab_id:
            nab = object
            for element in all_non_alcoholic_beverages:
                if element['id'] == nab_id:
                    nab = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(nab), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_non_alcoholic_beverages), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_alcoholic_beverages', methods=['GET'])
def list_alcoholic_beverages():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        ab_id = request.args.get('id')
        if ab_id:
            ab = object
            for element in all_alcoholic_beverages:
                if element['id'] == ab_id:
                    ab = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(ab), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_alcoholic_beverages), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_beers', methods=['GET'])
def list_beers():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        beer_id = request.args.get('id')
        if beer_id:
            beer = object
            for element in all_beers:
                if element['id'] == beer_id:
                    beer = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(beer), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_beers), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_candy_pizzas', methods=['GET'])
def list_candy_pizzas():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        candypizza_id = request.args.get('id')
        if candypizza_id:
            candypizza = object
            for element in all_candy_pizzas:
                if element['id'] == candypizza_id:
                    candypizza = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(candypizza), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_candy_pizzas), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_flapts', methods=['GET'])
def list_flapts():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        flapts_id = request.args.get('id')
        if flapts_id:
            flapt = object
            for element in all_flapts:
                if element['id'] == flapts_id:
                    flapt = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(flapt), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_flapts), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_pizza_edges', methods=['GET'])
def list_pizza_edges():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        pizza_edge_id = request.args.get('id')
        if pizza_edge_id:
            pizza_edge = object
            for element in all_pizza_edges:
                if element['id'] == pizza_edge_id:
                    pizza_edge = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(pizza_edge), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_pizza_edges), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_traditional_pizzas', methods=['GET'])
def list_traditional_pizzas():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        trad_pizza_id = request.args.get('id')
        if trad_pizza_id:
            trad_pizza = object
            for element in all_traditional_pizzas:
                if element['id'] == trad_pizza_id:
                    trad_pizza = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(trad_pizza), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_traditional_pizzas), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_gourmet_pizzas', methods=['GET'])
def list_gourmet_pizzas():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        gourmet_pizza_id = request.args.get('id')
        if gourmet_pizza_id:
            gourmet_pizza = object
            for element in all_gourmet_pizzas:
                if element['id'] == gourmet_pizza_id:
                    gourmet_pizza = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(gourmet_pizza), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_gourmet_pizzas), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_wines', methods=['GET'])
def list_wines():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        wine_id = request.args.get('id')
        if wine_id:
            wine = object
            for element in all_wines:
                if element['id'] == wine_id:
                    wine = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(wine), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_wines), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_promotions', methods=['GET'])
def list_promotions():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        promotion_id = request.args.get('id')
        if promotion_id:
            promotion = object
            for element in all_promotions:
                if element['id'] == promotion_id:
                    promotion = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(promotion), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_promotions), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list_two_flavored_pizzas', methods=['GET'])
def list_two_flavored_pizzas():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        # Check if ID was passed to URL query
        two_flavored_pizza_id = request.args.get('id')
        if two_flavored_pizza_id:
            two_flavored_pizza = object
            for element in all_two_flavored_pizzas:
                if element['id'] == two_flavored_pizza_id:
                    two_flavored_pizza = element
            # nab = non_alcoholic_beverages_ref.document(nab_id).get()
            return jsonify(two_flavored_pizza), 200
        else:
            # all_nab = [doc.to_dict() for doc in non_alcoholic_beverages_ref.stream()]
            return jsonify(all_two_flavored_pizzas), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/user', methods=['GET'])
def retrieve_user():
    try:
        id = request.args.get('id')
        user_snapshot = users_ref.document(id).get()
        user = user_snapshot.to_dict()
        orders_id_snapshot = users_ref.document(id).collection("orders_id").stream()
        user['orders_id'] = {}
        for order in orders_id_snapshot:
            # print(order.to_dict())
            # orders.append(order.to_dict())
            user['orders_id'][order.id] = {}
            user['orders_id'][order.id]["id"] = order.id


        # print(user)
        # pedidos = dict(itertools.zip_longest(*[iter(orders)] * 2, fillvalue=""))
        # print(orders)
        # user.update(orders)
        return jsonify(user), 200
        # return jsonify({"success": True}), 200
    except Exception as e:
        print('error')
        return f"An Error Occured: {e}"


@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route("/account", methods=['GET', 'POST'])
def addAccount():
    # import requests
    #
    # # Data
    # data = {
    #     'data1': 'something',
    #     'data2': 'otherthing'
    # }
    #
    # # Custom headers
    # headers = {
    #     'content-type': 'multipart/form-data'
    # }
    #
    # # Get response from server
    # response = requests.post('http://localhost/', data=data, headers=headers)
    #
    # # If you care about the response
    # print(response.json())

    #  with application.app_context():
    #     cur = mysql.connection.cursor()
    #    cur.execute('INSERT INTO users(id, name, email, phone) VALUES (%s, %s, %s, %s)',
    #           ('27siod037581984', 'Rogério Pires', 'l2othujk7857jkrs2703@gmail.com', '+5518988021682'))
    #  mysql.connection.commit()
    # cur.close()

    return jsonify(accounts[1])


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    # application.run(debug=True)#, host='0.0.0.0',port=5000)
    app.run(threaded=True, host='0.0.0.0', port=port)
