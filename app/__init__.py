import os
from flask import Flask
from config import Config #MONGO_URI
from flask_pymongo import PyMongo
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
CORS(app)
#mongo = PyMongo(app, MONGO_URI)

from app.upload_andretrieve_file_to_s3 import app
