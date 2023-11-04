from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()
import os
import json
from run import app


# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI2'), server_api=ServerApi('1'))
db = client[os.getenv("MONGODB_DATABASE")]
collection = db[os.getenv("MONGODB_COLLECTION")]

def test_conn():
# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

@app.route("/submit-text", method=['POST'])
def upload_file(json_file):
    with open(json_file, 'r') as f:
        curr_note = json.load(f)

    collection.insert_one(curr_note)

if __name__ == "__main__":
    test_conn()
