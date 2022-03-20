import re, os
import requests
import datetime
import json
import ast
import json2table
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
    return render_template('index.html',title='Metals Table Data', error="Page not found - 404 error")

@app.route('/ping')
def ping():
    return render_template('index.html',title='Metals Table Data', healthcheck="pong")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metals', methods=['GET'])
def getdata_back():
    response = requests.get(url_back_get, timeout=3)
    if response.status_code == requests.codes.ok:
      data = json.loads(response.text)
      res = ast.literal_eval(data)
      dictOfWords = { i : res[i] for i in range(0, len(res) ) }
#      print(data)
#      print(type(data))
#      print(type(res))
#      print(type(dictOfWords))
      for x in range(len(dictOfWords)):
        print(dictOfWords[x])

#      fields = data[0].keys() if len(data) > 0 else []
      return render_template('metals.html',title='Metals Table Data', data=dictOfWords)

    else:
      return render_template('index.html',title='Metals Table Data', error="Failed to get data from backend. Error code = "+ str(response.status_code))

@app.route('/update', methods=['GET','POST'])
def update_data():
    response = requests.post(url_back_update, timeout=10)
    return render_template('index.html',title='Metals Table Data', error=response.json())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
