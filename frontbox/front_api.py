import re, os
import requests
import datetime
import json
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify, request, render_template
from flask import Flask

app = Flask(__name__)
api = Api(app)

front_port = os.getenv('front-port-var')
url_back = os.getenv('url-back')

print(front_port)
print(url_back)

url_back_get=   "http://"+url_back+"/metals"
url_back_update=   "http://"+url_back+"/update"
url_back_filter=   "http://"+url_back+"/filter"
#url_back_update="http://backbox:8000/update"
#url_back_filter="http://backbox:8000/filter"

print(url_back_get)

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html',title='Metals Table Data', error="Page not found - 404 error")

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metals', methods=['GET'])
def getdata_back():
    response = requests.get(url_back_get, timeout=3)
    if response.status_code == requests.codes.ok:
      data = response.json()
      columns = ['dt', 'buy', 'sell', 'name']
      df = pd.DataFrame(eval(data), columns=columns)
      table = df.to_html(index=False)
      return render_template('index.html',title='Metals Table Data', table=table)
    else:
      return render_template('index.html',title='Metals Table Data', error="Failed to get data from backend. Error code = "+ str(response.status_code))

@app.route('/filter', methods=['GET'])
def filterdata_back():
    metals_name = request.args.get('metal')
    print(metals_name)
    url = url_back_filter+"?name="+metals_name
    print(url)
    response = requests.get(url_back_filter+"?metal="+metals_name, timeout=3)
    if response.status_code == requests.codes.ok:
      data = response.json()
      columns = ['dt', 'buy', 'sell', 'name']
      df = pd.DataFrame(eval(data), columns=columns)
      table = df.to_html(index=False)
      return render_template('index.html',title='Metals Table Data', table=table)
    else:
      return render_template('index.html',title='Metals Table Data', error="Failed to get data from backend. Error code = "+ str(response.status_code))


@app.route('/update', methods=['GET','POST'])
def update_data():
    response = requests.post(url_back_update, timeout=10)
    if response.status_code == requests.codes.ok:
      return render_template('index.html',title='Metals Table Data', error=response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=front_port)
