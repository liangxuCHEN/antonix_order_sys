from flask import Flask, url_for, request, jsonify, Response, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

import os

base_dir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



app.config['SQLALCHEMY_DATABASE_URI'] = \
         "mssql+pymssql://sa:123456@192.168.0.209:1433/AnToNio1.0?charset=utf8"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['UPLOAD_FOLDER'] = os.getcwd() + '/uploads'
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPBasicAuth()

db = SQLAlchemy(app)
api = Api(app)