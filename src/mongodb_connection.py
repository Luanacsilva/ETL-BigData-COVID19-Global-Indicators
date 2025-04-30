import os
from pymongo import MongoClient
from dotenv import load_dotenv

def conectar_mongo(db_name, collection_name):
      
    load_dotenv()
    mongo_url = os.getenv("MONGO_URL")
    client = MongoClient(mongo_url)
    db = client["covid19_project"]
    collection = db[collection_name]


    print(f"[OK] Conectado à coleção '{collection_name}' no banco '{db_name}'.")
    return collection

worldbank_collection = conectar_mongo(db_name="covid19_project", collection_name="dados_worldbank_transformado")
covid_collection = conectar_mongo(db_name="covid19_project", collection_name="dados_covid_historico")
raw_collection = conectar_mongo(db_name="covid19_project", collection_name="dados_worldbank")
transformed_collection = conectar_mongo(db_name="covid19_project", collection_name="dados_worldbank_transformado")
