# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
import os
# from sqlalchemy import create_engine
# from models import User


application = Flask(__name__)
application.config['MYSQL_HOST'] = 'aad4ceauedwkx7.ctvp1qfizfsm.us-east-2.rds.amazonaws.com'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = '27031984As'
application.config['MYSQL_DB'] = 'ebdb'

mysql = MySQL(application)


accounts = [
        {'name': "Billy", 'balance': 450.0},
        {'name': "Kelly", 'balance': 250.0}
    ]
# HTTP GET
# HTTP POST
# HTTP PUT
# HTTP DELETE
# HTTP PATCH


@application.route("/")
def home():
    return render_template("index.html")


@application.route("/accounts", methods=["GET"])
def getAccounts():
    return jsonify(accounts)


@application.route("/account/<id>", methods=["GET"])
def getAccount(id):
    id = int(id) -1
    return jsonify(accounts[id])


@application.route("/account", methods=['GET', 'POST'])
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


if __name__ == '__main__':
    application.run(debug=True)#, host='0.0.0.0',port=5000)
