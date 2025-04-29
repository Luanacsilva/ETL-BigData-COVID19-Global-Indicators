import os
from pymongo import MongoClient
from dotenv import load_dotenv

def conectar_mongo(db_name, collection_name):
    #Função para conectar no MongoDB Atlas e retornar a coleção.
    load_dotenv()
    mongo_url = os.getenv("MONGO_URL")

    client = MongoClient(mongo_url)
    db = client[db_name]
    collection = db[collection_name]

    print(f"[OK] Conectado à coleção '{collection_name}' no banco '{db_name}'.")
    return collection
