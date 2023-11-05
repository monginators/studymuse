from dotenv import load_dotenv
load_dotenv()

import os
from llama_index.readers.mongo import SimpleMongoReader
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext

def embed():
    # load objects from mongo and convert them into LlamaIndex Document objects
    # llamaindex has a special class that does this for you
    # it pulls every object in a given collection
    query_dict = {}
    reader = SimpleMongoReader(uri=os.getenv("MONGODB_URI"))
    documents = reader.load_data(
        os.getenv("MONGODB_DATABASE"),
        os.getenv("MONGODB_COLLECTION"), # this is the collection where the objects you loaded in 1_import got stored
        field_names=["text"], # these is a list of the top-level fields in your objects that will be indexed
                                # make sure your objects have a field called "full_text" or that you change this value
        query_dict=query_dict # this is a mongo query dict that will filter your data if you don't want to index everything
    )

    # Create a new client and connect to the server
    client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))

    # create Atlas as a vector store
    store = MongoDBAtlasVectorSearch(
        client,
        db_name=os.getenv('MONGODB_DATABASE'),
        collection_name=os.getenv('MONGODB_VECTORS'), # this is where your embeddings will be stored
        index_name=os.getenv('MONGODB_VECTOR_INDEX') # this is the name of the index you will need to create
    )

    # now create an index from all the Documents and store them in Atlas
    storage_context = StorageContext.from_defaults(vector_store=store)
    index = VectorStoreIndex.from_documents(
        documents=[documents[-1]], storage_context=storage_context,
        show_progress=True, # this will show you a progress bar as the embeddings are created
    )

    # you can't query your index yet because you need to create a vector search index in mongodb's UI now

if __name__ == "__main__":
    embed()