import re, os
import requests
import mysql.connector
import datetime
import json
from requests.structures import CaseInsensitiveDict
from lxml import etree as etree
from decimal import Decimal
from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, make_response, url_for, request

app = Flask(__name__)
api = Api(app)

conn = mysql.connector.connect(user='root',
                               password='pass',
                               host='localhost',
                               database='metalsdb',
                               auth_plugin='mysql_native_password')

if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")

#url = "http://www.cbr.ru/scripts/xml_metall.asp?date_req1=01/03/2022&date_req2=02/03/2022"
# as CBR add captcha for it's site, I created CBR emulator
url = "http://cbr.example.com/metals.xml"

headers = {'User-Agent': 'Mozilla',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-encoding': 'none',
           'Connection': 'keep-alive',
           'Content-Type': 'application/xml; charset=windows-1251',
           'content-Encoding': 'gzip'}

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}, 404))

class Ping(Resource):
    def get(self):
        return 'pong'

class Update(Resource):
    def get(self):
        return 'OK'

    def post(self):
        resp = requests.get(url,timeout=3,headers=headers)
        print (resp.status_code)
        if resp.status_code == requests.codes.ok:
            root = etree.fromstring(resp.content)

            for child in root:
                dt = child.attrib.get('Date')
                code = child.attrib.get('Code')

                for elem in child.getchildren():
                    if not elem.text:
                        text = "None"
                    else:
                        text = elem.text
                        if elem.tag =="Buy":
                            buy = elem.text
                        if elem.tag == "Sell":
                            sell = elem.text

#                print(dt + "," +code +"," + buy.replace(',','.') +"," + sell.replace(',','.'))
                if conn.is_connected():
                    cursor = conn.cursor()
                    metalsdata = """REPLACE INTO metals_data (dt,code,buy,sell) VALUES (STR_TO_DATE(%s,'%d.%m.%Y'),%s,%s,%s)"""
                    cursor.execute(metalsdata, (dt, code, float(buy.replace(',','.')), float(sell.replace(',','.'))))
                    conn.commit()
            response = make_response(
               jsonify({"message": "Data was uploaded to Database"}, 200))
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(
                jsonify({"message": "Failed to upload xml to DATABASE. Error code="+ str(resp.status_code)}, 500))
            response.headers["Content-Type"] = "application/json"
            return response

class Metals(Resource):
    def get(self):
        if conn.is_connected():
            metalsdata = "SELECT * from metalsdb.metalls_v"
            cursor = conn.cursor(dictionary=True)
            cursor.execute(metalsdata)
            result = cursor.fetchall()
            return(f"json: {json.dumps(result, default=str)}")


api.add_resource(Metals, '/metals')  # add endpoints
api.add_resource(Update, '/update')  # add endpoints
api.add_resource(Ping, '/ping')  # add endpoints

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
