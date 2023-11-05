## This shows how to load your pre-indexed data from mongo and query it
## Note that you MUST manually create a vector search index before this will work
## and you must pass in the name of that index when connecting to Mongodb below 
from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Turns on really noisy logging
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex

# Create a new client and connect to the server
client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
anthropic = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'),)

def queriana(query):
    # connect to Atlas as a vector store
    store = MongoDBAtlasVectorSearch(
        client,
        db_name=os.getenv('MONGODB_DATABASE'), # this is the database where you stored your embeddings
        collection_name=os.getenv('MONGODB_VECTORS'), # this is where your embeddings were stored in 2_load_and_index.py
        index_name=os.getenv('MONGODB_VECTOR_INDEX') # this is the name of the index you created after loading your data
    )
    index = VectorStoreIndex.from_vector_store(store)

    # query your data!
    query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(query)
    print("yooooo", type(response.response))
    if response.response == "Empty Response" or response.response.__contains__("not enough information"):
        response = anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=f'({HUMAN_PROMPT} {query} {AI_PROMPT}',
        )
        response = f'This information has been AI generated and is not from your notes: {response.completion}'

    return response