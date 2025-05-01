import requests
import pandas as pd
import time
from config import conectar_mongo

historico_collection = conectar_mongo("dados_covid_historico")

# ======= FUNÇÕES =======

def extrair_dados_historicos(pais_nome):
    url = f"https://disease.sh/v3/covid-19/historical/{pais_nome}?lastdays=all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def transformar_dados(dados, pais_nome):
    if "timeline" not in dados or "cases" not in dados["timeline"]:
        return pd.DataFrame()

    casos = dados["timeline"]["cases"]
    df = pd.DataFrame(list(casos.items()), columns=["data", "casos_acumulados"])
    df["data"] = pd.to_datetime(df["data"], format="%m/%d/%y")

    df["novos_casos"] = df["casos_acumulados"].diff().fillna(0).astype(int)
    df["novos_casos"] = df["novos_casos"].apply(lambda x: max(x, 0))

    df["media_movel_7d"] = df["novos_casos"].rolling(7).mean().round(2)
    df["taxa_crescimento_dia"] = df["novos_casos"].pct_change().fillna(0) * 100
    df["taxa_crescimento_dia"] = df["taxa_crescimento_dia"].round(2)
    df["pais"] = pais_nome
    return df

def carregar_no_mongo(df, pais_nome):
    if not df.empty:
        historico_collection.delete_many({"pais": pais_nome})
        historico_collection.insert_many(df.to_dict(orient="records"))
        print(f"[✅] {pais_nome}: {df.shape[0]} registros salvos.")
    else:
        print(f"[⚠️] {pais_nome}: Nenhum dado válido.")

# ======= EXECUÇÃO GLOBAL =======

def etl_covid_global():
    print("🌍 Iniciando ETL de COVID para todos os países...")

    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    if response.status_code != 200:
        print("[ERRO] Não foi possível obter a lista de países.")
        return

    paises = [item["country"] for item in response.json()]

    for pais in paises:
        try:
            dados = extrair_dados_historicos(pais)
            if dados:
                df = transformar_dados(dados, pais)
                carregar_no_mongo(df, pais)
            else:
                print(f"[❌] {pais}: Falha na extração.")
        except Exception as e:
            print(f"[ERRO] {pais}: {e}")
        time.sleep(0.3)  # 👈 pra não sobrecarregar a API

    print("\n🎯 ETL de COVID finalizada com sucesso!")

if __name__ == "__main__":
    etl_covid_global()
