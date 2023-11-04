# extensions.py

from flask_sqlalchemy import SQLAlchemy
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()
import os

db = SQLAlchemy()

client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
mongodb = client[os.getenv("MONGODB_DATABASE")]