import pandas as pd
from config import worldbank_collection,covid_collection

def extrair_economico_por_ano(iso3):
    """Extrai indicadores econômicos por ano para um país (ISO3)."""
    indicadores = ["PIB_Total", "PIB_per_capita", "Desemprego", "Expectativa_vida"]

    dados = list(worldbank_collection.find({
        "pais": iso3,
        "indicador_nome": {"$in": indicadores},
        "valor": {"$ne": None}
    }, {"ano": 1, "indicador_nome": 1, "valor": 1, "_id": 0}))

    if not dados:
        print(f"[AVISO] Nenhum dado econômico encontrado para {iso3}.")
        return pd.DataFrame()

    df = pd.DataFrame(dados)
    df["ano"] = df["ano"].astype(int)
    df_pivot = df.pivot(index="ano", columns="indicador_nome", values="valor").reset_index()

    print(f"[OK] Indicadores econômicos extraídos para {iso3}: {df_pivot.shape[0]} anos disponíveis.")
    return df_pivot

def extrair_covid_por_ano(pais_nome):
    """Extrai dados históricos de COVID por ano (somando novos casos)."""
    dados = list(covid_collection.find(
        {"pais": pais_nome}, {"data": 1, "novos_casos": 1, "_id": 0}
    ))

    if not dados:
        print(f"[AVISO] Nenhum dado de COVID encontrado para {pais_nome}.")
        return pd.DataFrame()

    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"])
    df["ano"] = df["data"].dt.year
    df_ano = df.groupby("ano")["novos_casos"].sum().reset_index()
    df_ano.rename(columns={"novos_casos": "casos_covid_ano"}, inplace=True)

    print(f"[OK] Casos de COVID agregados por ano para {pais_nome}: {df_ano.shape[0]} anos.")
    return df_ano


def montar_temporal(pais_nome, pais_iso3):
    """Combina dados econômicos e COVID por ano."""
    df_economico = extrair_economico_por_ano(pais_iso3)
    df_covid = extrair_covid_por_ano(pais_nome)

    if df_economico.empty or df_covid.empty:
        print(f"[ERRO] Dataset incompleto para {pais_nome}.")
        return pd.DataFrame()

    df_final = pd.merge(df_economico, df_covid, on="ano", how="left")
    return df_final

def salvar_csv(df, pais_nome):
    """Salva o DataFrame final em CSV."""
    if df.empty:
        print(f"[ERRO] Nenhum dado a salvar para {pais_nome}.")
        return

    caminho = f"data/tendencias_{pais_nome.replace(' ', '_')}.csv"
    caminho = f"data/tendencias_{pais_nome.replace(' ', '_')}.csv"
    df.to_csv(caminho, index=False)
    print(f"[OK] CSV salvo com sucesso: {caminho}")


def etl_tendencias():
    """Executa o pipeline completo para um país específico."""
    pais_nome = "Brazil"
    pais_iso3 = "BRA"
    df = montar_temporal(pais_nome, pais_iso3)
    salvar_csv(df, pais_nome)

if __name__ == "__main__":
    etl_tendencias()