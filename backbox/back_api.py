import os
import requests
import mysql.connector
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from lxml import etree as etree
from mysql.connector import errorcode
from flask_restful import Resource, Api
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
api = Api(app)

db_user = os.getenv('db_user')
db_userpass = os.getenv('db_userpass')
db_host = os.getenv('db_host')
db_name = os.getenv('db_name')
back_port = os.getenv('back_port', 8000)
cbr_url = str(os.getenv('cbr_url'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+db_user+':'+db_userpass+'@'+db_host+'/'+db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class metals_codes(db.Model):
    __tablename__ = 'metals_codes'
    code = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    db.UniqueConstraint(code, name)


class metals_data(db.Model):
    __tablename__ = 'metals_data'
    dt = db.Column(db.Date)
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False)
    buy = db.Column(db.Float(10, 2))
    sell = db.Column(db.Float(10, 2))
    db.UniqueConstraint(dt, code)


config = {
  'user': db_user,
  'password': db_userpass,
  'host': db_host,
  'database': db_name,
  'raise_on_warnings': True,
  'auth_plugin': 'mysql_native_password',
  'autocommit': True
}

# print(config)

# url = "http://www.cbr.ru/scripts/xml_metall.asp?date_req1=01/03/2022&date_req2=02/03/2022"
# as CBR add captcha for it's site, I created CBR emulator
# url = "http://172.17.0.2/metals.xml"
url = cbr_url

# print(url)

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
    def post(self):
        try:
            resp = requests.get(url, timeout=3, headers=headers, verify=False)
            resp.raise_for_status()
            if resp.status_code == requests.codes.ok:
                conn = mysql.connector.connect(**config)
                root = etree.fromstring(resp.content)

                for child in root:
                    dt = child.attrib.get('Date')
                    code = child.attrib.get('Code')

                    for elem in child.getchildren():
                        if not elem.text:
                            text = "None"
                        else:
                            text = elem.text
                            if elem.tag == "Buy":
                                buy = elem.text
                            if elem.tag == "Sell":
                                sell = elem.text

#                print(dt + "," +code +"," + buy.replace(',','.') +"," + sell.replace(',','.'))
                    if conn.is_connected():
                        cursor = conn.cursor()
                        metalsdata = """REPLACE INTO metals_data (dt,code,buy,sell) VALUES (STR_TO_DATE(%s,'%d.%m.%Y'),%s,%s,%s)"""
                        cursor.execute(metalsdata, (dt, code, float(buy.replace(',', '.')), float(sell.replace(',', '.'))))
                cursor.close
                conn.close
                return("Data was uploaded to Database")
            else:
                return("Failed to upload xml file to DATABASE. Error code = " + str(resp.status_code))

        except requests.exceptions.RequestException as err:
            return("Failed to upload xml file to DATABASE. Error code = " + str(err))
        except requests.exceptions.HTTPError as errh:
            return("Failed to upload xml file to DATABASE. Error code = " + str(errh))
        except requests.exceptions.ConnectionError as errc:
            return("Failed to upload xml file to DATABASE. Error code = " + str(errc))
        except requests.exceptions.Timeout as errt:
            return("Failed to upload xml file to DATABASE. Error code = " + str(errt))


class Prepare(Resource):
    def post(self):
        try:
            conn = mysql.connector.connect(**config)
            if conn:
                checkcodes = "SELECT COUNT(*) FROM metals_codes"
                cursor = conn.cursor()
                cursor.execute(checkcodes)
                result = cursor.fetchone()[0]
                if not result:
                    upddata = """INSERT INTO metals_codes(code,name) VALUES ('1','gold');
                                INSERT INTO metals_codes(code,name) VALUES ('2','silver');
                                INSERT INTO metals_codes(code,name) VALUES ('3','platina');
                                INSERT INTO metals_codes(code,name) VALUES ('4','palladium');"""
                    cursor.execute(upddata)
                    cursor.close
                    conn.close
                    return("Table with codes was populated to the database")
                else:
                    conn.close
                    return("Codes are already exists in database")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


class Metals(Resource):
    def get(self):
        try:
            conn = mysql.connector.connect(**config)
            if conn:
                metalsdata = """select md.dt AS dt, md.buy AS buy, md.sell AS sell, mc.name AS name
                                from metals_codes mc
                                join metals_data md
                                where mc.code = md.code """
                cursor = conn.cursor(dictionary=True)
                cursor.execute(metalsdata)
                result = cursor.fetchall()
                cursor.close
                conn.close
                return(json.dumps(result, default=str))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


class Filter(Resource):
    def get(self):
        metals_name = request.args.get('metal')
        try:
            conn = mysql.connector.connect(**config)
            if conn:
                metalsdata = """select md.dt AS dt, md.buy AS buy, md.sell AS sell, mc.name AS name
                                from metals_codes mc
                                join metals_data md
                                where (mc.code = md.code and name = %s)"""
                cursor = conn.cursor(dictionary=True)
                cursor.execute(metalsdata, [metals_name])
                result = cursor.fetchall()
                cursor.close
                conn.close
                return(json.dumps(result, default=str))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


api.add_resource(Metals, '/metals')  # add endpoints
api.add_resource(Update, '/update')  # add endpoints
api.add_resource(Ping, '/ping')  # add endpoints
api.add_resource(Filter, '/filter')  # add endpoints
api.add_resource(Prepare, '/prepare')  # add endpoints


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=back_port)
