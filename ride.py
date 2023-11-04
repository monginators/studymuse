from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()
import os
import json

#uri = "mongodb+srv://rayant:gcVuoLoTz830GZmx@cluster0.4eebirt.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
db = client[os.getenv("MONGODB_DATABASE")]

def test_conn():
# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def upload_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Create a new client and connect to the server
    collection = db[os.getenv("MONGODB_COLLECTION")]
    collection.insert_many(data)