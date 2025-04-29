import requests
import pandas as pd
import time
from mongodb_connection import conectar_mongo

raw_collection = conectar_mongo(db_name="covid19_project", collection_name="dados_worldbank")
transformed_collection = conectar_mongo(db_name="covid19_project", collection_name="dados_worldbank_transformado")

anos_desejados = [str(ano) for ano in range(2000, 2024)]

indicadores_relevantes = {
    "PIB_Total": "NY.GDP.MKTP.CD",
    "PIB_per_capita": "NY.GDP.PCAP.CD",
    "Desemprego": "SL.UEM.TOTL.ZS",
    "Expectativa_vida": "SP.DYN.LE00.IN",
    "Gasto_saude": "SH.XPD.CHEX.GD.ZS",
    "Taxa_escolarizacao": "SE.PRM.ENRR",
    "Taxa_alfabetizacao": "SE.ADT.LITR.ZS"
}


def listar_paises():
    url = "http://api.worldbank.org/v2/country?format=json&per_page=500"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        paises = [pais["id"] for pais in dados[1] if pais.get("region", {}).get("id") not in ["", "NA"]]
        if "BRA" not in paises:
            paises.append("BRA")
            print("[OK] Brasil incluído manualmente.")
        return paises
    else:
        print("[ERRO] Falha ao obter países.")
        return []

def extrair_dados(pais, nome_indicador, codigo_indicador):
    url = f"http://api.worldbank.org/v2/country/{pais}/indicator/{codigo_indicador}?format=json&per_page=1000"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    dados = response.json()
    registros = []
    if isinstance(dados, list) and len(dados) > 1:
        for item in dados[1]:
            if item.get("date") in anos_desejados and item.get("value") is not None:
                registros.append({
                    "pais": item["country"]["id"],
                    "pais_nome": item["country"]["value"],
                    "indicador_nome": nome_indicador,
                    "indicador_codigo": codigo_indicador,
                    "ano": int(item["date"]),
                    "valor": item["value"]
                })
    return registros


def transformar_dados(df):
    """Adiciona taxas de crescimento e média móvel."""
    df["ano"] = df["ano"].astype(int)
    df.sort_values(by=["pais", "indicador_nome", "ano"], inplace=True)

    transformados = []

    for (pais, indicador), grupo in df.groupby(["pais", "indicador_nome"]):
        grupo = grupo.sort_values("ano")
        grupo["valor_anterior"] = grupo["valor"].shift(1)
        grupo["taxa_crescimento_pct"] = ((grupo["valor"] - grupo["valor_anterior"]) / grupo["valor_anterior"]) * 100

        if indicador in ["Desemprego", "Expectativa_vida", "Gasto_saude"]:
            grupo["media_movel_3anos"] = grupo["valor"].rolling(window=3).mean()
        else:
            grupo["media_movel_3anos"] = None

        grupo["taxa_crescimento_pct"] = grupo["taxa_crescimento_pct"].round(2).fillna(0)

        for _, row in grupo.iterrows():
            transformados.append({
                "pais": row["pais"],
                "pais_nome": row["pais_nome"],
                "indicador_nome": row["indicador_nome"],
                "indicador_codigo": row["indicador_codigo"],
                "ano": row["ano"],
                "valor": row["valor"],
                "taxa_crescimento_pct": row["taxa_crescimento_pct"],
                "media_movel_3anos": row["media_movel_3anos"]
            })

    return pd.DataFrame(transformados)


def etl_worldbank(paises_especificos=None):
    print("[INÍCIO] ETL Indicadores Socioeconômicos por País")

    raw_collection.delete_many({})
    transformed_collection.delete_many({})
    print("[OK] Coleções limpas!")

    paises = paises_especificos if paises_especificos else listar_paises()
    todos_registros = []

    for pais in paises:
        print(f"🌍 Coletando dados de: {pais}")
        for nome, codigo in indicadores_relevantes.items():
            registros = extrair_dados(pais, nome, codigo)
            todos_registros.extend(registros)
            time.sleep(0.1)

    if todos_registros:
        df_raw = pd.DataFrame(todos_registros)
        raw_collection.insert_many(df_raw.to_dict(orient="records"))
        print(f"[OK] {len(df_raw)} registros brutos inseridos.")

        df_transformado = transformar_dados(df_raw)
        transformed_collection.insert_many(df_transformado.to_dict(orient="records"))
        print(f"[OK] {len(df_transformado)} registros transformados inseridos.")
    else:
        print("[ERRO] Nenhum dado coletado!")

if __name__ == "__main__":
    etl_worldbank()
