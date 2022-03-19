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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()  # run our Flask app
