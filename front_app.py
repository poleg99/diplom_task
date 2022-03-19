import re, os
import requests
import datetime
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify
from flask import Flask, render_template

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metals', methods=['GET'])
def getdata_back():
    response = requests.get('http://localhost:8000/metals')
    return render_template('metals.html', title='Metals Table',metals=response)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
