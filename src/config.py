import os
from pymongo import MongoClient
from dotenv import load_dotenv

def conectar_mongo(collection_name):
      
    load_dotenv()
    mongo_url = os.getenv("MONGO_URL")
    client = MongoClient(mongo_url)
    db = client["covid19_project"]
    collection = db[collection_name]


    print(f"[OK] Conectado à coleção '{collection_name}' no banco covid19_project.")
    return collection

historico_collection = conectar_mongo("dados_covid_historico")
worldbank_collection = conectar_mongo("dados_worldbank_transformado")
covid_collection = conectar_mongo("dados_covid_historico")
raw_collection = conectar_mongo("dados_worldbank")
transformed_collection = conectar_mongo("dados_worldbank_transformado")
