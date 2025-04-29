import pandas as pd
from mongodb_connection import conectar_mongo

# =============== ETL 5 - Visualização Interativa ===============
# Versão com suporte a países com dados parciais

# =============== CONEXÃO MONGO ===============
worldbank_collection = conectar_mongo(db_name="covid19_project", collection_name="dados_worldbank_transformado")
covid_collection = conectar_mongo(db_name="covid19_project", collection_name="dados_covid_historico")

# =============== FUNÇÕES ===============

def listar_paises_disponiveis():
    """Lista os países presentes no banco."""
    paises = sorted(worldbank_collection.distinct("pais_nome"))
    print("\n🌍 Países disponíveis:")
    for idx, pais in enumerate(paises, 1):
        print(f"{idx}. {pais}")
    return paises

def extrair_economico(iso3):
    """Extrai indicadores econômicos ano a ano."""
    indicadores = ["PIB_Total", "PIB_per_capita", "Desemprego", "Expectativa_vida"]

    dados = list(worldbank_collection.find({
        "pais": iso3,
        "indicador_nome": {"$in": indicadores},
        "valor": {"$ne": None}
    }, {"ano": 1, "indicador_nome": 1, "valor": 1, "_id": 0}))

    if not dados:
        return pd.DataFrame()

    df = pd.DataFrame(dados)
    df["ano"] = df["ano"].astype(int)
    return df.pivot(index="ano", columns="indicador_nome", values="valor").reset_index()

def extrair_covid(pais_nome):
    """Extrai dados históricos de COVID por ano."""
    dados = list(covid_collection.find({
        "pais": pais_nome
    }, {"data": 1, "novos_casos": 1, "_id": 0}))

    if not dados:
        return pd.DataFrame()

    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"])
    df["ano"] = df["data"].dt.year
    df_ano = df.groupby("ano")["novos_casos"].sum().reset_index()
    df_ano.rename(columns={"novos_casos": "casos_covid_ano"}, inplace=True)
    return df_ano

def montar_dataset(pais_nome, iso3):
    """Combina dados de economia e COVID — aceita parciais com checagem."""
    df_economico = extrair_economico(iso3)
    df_covid = extrair_covid(pais_nome)

    if df_economico.empty and df_covid.empty:
        print(f"[AVISO] Nenhum dado encontrado para {pais_nome}.")
        return pd.DataFrame()

    # Garantir coluna "ano" nos dois
    if "ano" not in df_economico.columns:
        df_economico["ano"] = pd.Series(dtype=int)
    if "ano" not in df_covid.columns:
        df_covid["ano"] = pd.Series(dtype=int)

    df_final = pd.merge(df_economico, df_covid, on="ano", how="outer")

    # Foco nos anos entre 2019 e 2023
    df_final = df_final[df_final["ano"].between(2019, 2023)]

    # Corrige casos_covid_ano
    if "casos_covid_ano" in df_final.columns:
        df_final["casos_covid_ano"] = df_final["casos_covid_ano"].fillna(0).astype(int)
    else:
        df_final["casos_covid_ano"] = 0

    df_final.fillna("-", inplace=True)

    return df_final


def salvar_dataset(df, pais_nome):
    """Salva CSV com dados do país."""
    caminho = f"../data/tendencias_interativo_{pais_nome.replace(' ', '_')}.csv"
    df.to_csv(caminho, index=False)
    print(f"[💾] CSV salvo: {caminho}\n")

# =============== EXECUÇÃO INTERATIVA ===============

if __name__ == "__main__":
    paises = listar_paises_disponiveis()

    escolhas = input("\nDigite os números dos países desejados (separados por vírgula): ")
    indices = [int(x.strip()) - 1 for x in escolhas.split(",")]

    for idx in indices:
        try:
            pais_nome = paises[idx]
        except IndexError:
            print(f"[ERRO] Número {idx + 1} inválido! Pulando...")
            continue

        print(f"\n🔎 Processando país: {pais_nome}")

        iso3_doc = worldbank_collection.find_one({"pais_nome": pais_nome}, {"pais": 1, "_id": 0})
        if not iso3_doc:
            print(f"[ERRO] ISO3 não encontrado para {pais_nome}.")
            continue

        iso3 = iso3_doc["pais"]
        df_final = montar_dataset(pais_nome, iso3)

        if df_final.empty:
            print(f"[AVISO] Nenhum dado útil encontrado para {pais_nome}.")
            continue

        print("\n📊 Preview dos dados:")
        print(df_final.head(10))

        salvar_dataset(df_final, pais_nome)

    print("\n🎯 Todos os países selecionados foram processados com sucesso!")
