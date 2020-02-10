# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
# from flask_mysqldb import MySQL
import os
# from sqlalchemy import create_engine
# from models import User


application = Flask(__name__)
application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = '27031984As'
application.config['MYSQL_DB'] = 'lucaspossettiDB'

# mysql = MySQL(application)

# db_connect = create_engine('sqlite:///lucaspossetti.db')


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), nullable=False)
#     phone = db.Column(db.Float(asdecimal=False))
#
#     def __init__(self,  name, email, phone):
#         self.name = name
#         self.email = email
#         self.phone = phone
#
#     def __repr__(self):
#         return '<Usuário %d>' % self.id


# user = User("Rogerio Pires", "rogeriodeandradepires@live.com", "18988021682")
# user = User("Rogerio Pires", "rogeriodeandradepires@live.com", "18988021682")

accounts = [
        {'name': "Billy", 'balance': 450.0},
        {'name': "Kelly", 'balance': 250.0}
    ]

@application.route("/")
def home():
    return render_template("index.html")


@application.route("/accounts",methods=["GET"])
def getAccounts():
    return jsonify(accounts)

@application.route("/account/<id>", methods=["GET"])
def getAccount(id):
    id = int(id) -1
    return jsonify(accounts[id])

@application.route("/account",methods=["POST"])
def addAccount():
    name = request.json['name']
    balance = request.json['balance']
    data = {'name': name, 'balance': balance}
    accounts.append(data)

    return jsonify(data)

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0',port=80)
