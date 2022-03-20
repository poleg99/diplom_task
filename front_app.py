import re, os
import requests
import datetime
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, make_response, url_for, request
from flask import Flask, render_template

app = Flask(__name__)
api = Api(app)

url_back_get="http://localhost:8000/metals"
url_back_update="http://localhost:8000/update"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}, 404))

@app.route('/ping')
def ping():
    return render_template('index.html',title='Metals Table Data', data="pong")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metals', methods=['GET'])
def getdata_back():
    response = requests.get(url_back_get, timeout=3)
    if response.status_code == requests.codes.ok:
      jresponse = response.text
      data = json.loads(jresponse)
      return render_template('metals.html',title='Metals Table Data', data=data)
    else:
      response = make_response(
                    jsonify({"message": "Failed to get data from backend. Error code ="+ str(response.status_code)}, 500))
      response.headers["Content-Type"] = "application/json"
      return response

@app.route('/update', methods=['GET','POST'])
def update_data():
    response = requests.post(url_back_update, timeout=10)

    return

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
