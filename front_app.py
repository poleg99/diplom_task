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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}, 404))

@app.route('/ping')
def ping():
    response = make_response(
            jsonify({"message": "pong"}, 200))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metals', methods=['GET'])
def getdata_back():
    response = requests.get("http://localhost:8000/metals")
    jresponse = response.text
    data = json.loads(jresponse)

    return render_template('metals.html',title='Metals Table Data', data=data)

@app.route('/update', methods=['POST'])
def update_data():
    response = requests.get("http://localhost:8000/update")
    jresponse = response.text
    data = json.loads(jresponse)

    return data

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
