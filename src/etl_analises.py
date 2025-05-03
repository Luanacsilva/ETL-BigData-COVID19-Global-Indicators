import pandas as pd
from config import covid_collection,worldbank_collection


def extrair_casos_covid():
    """Agrupa dados históricos de COVID por país, somando os novos casos."""
    dados = covid_collection.find({}, {"pais": 1, "novos_casos": 1, "_id": 0})
    df = pd.DataFrame(dados)

    if df.empty:
        print("[AVISO] Nenhum dado de COVID encontrado.")
        return pd.DataFrame()

    df_covid = df.groupby("pais")["novos_casos"].sum().reset_index()
    df_covid.rename(columns={"pais": "pais_nome", "novos_casos": "cases"}, inplace=True)

    print(f"[OK] Casos de COVID agregados: {df_covid.shape[0]} países.")
    return df_covid


def extrair_indicadores_socioeconomicos():
    """Extrai os indicadores mais recentes por país."""
    indicadores = [
        "PIB_Total", "PIB_per_capita", "Desemprego",
        "Expectativa_vida", "Gasto_saude",
        "Taxa_escolarizacao", "Taxa_alfabetizacao"
    ]

    dados = worldbank_collection.find({
        "indicador_nome": {"$in": indicadores},
        "valor": {"$ne": None}
    }, {"pais": 1, "pais_nome": 1, "indicador_nome": 1, "ano": 1, "valor": 1, "_id": 0})

    df = pd.DataFrame(dados)

    if not df.empty:
        df["ano"] = df["ano"].astype(int)
        df.sort_values(["pais", "indicador_nome", "ano"], ascending=[True, True, False], inplace=True)
        df = df.drop_duplicates(subset=["pais", "indicador_nome"], keep="first")

    print(f"[OK] Indicadores socioeconômicos extraídos: {df.shape[0]} registros.")
    return df


def cruzar_covid_e_indicadores(df_covid, df_indicadores):
    """Combina dados de COVID e indicadores socioeconômicos por país_nome."""

    df_indicadores = df_indicadores[df_indicadores["pais_nome"].notna()]
    df_indicadores = df_indicadores.pivot(index="pais_nome", columns="indicador_nome", values="valor").reset_index()

    df_indicadores.rename(columns={
        "PIB_Total": "pib_total_usd",
        "PIB_per_capita": "pib_per_capita_usd",
        "Desemprego": "taxa_desemprego",
        "Expectativa_vida": "expectativa_vida_anos",
        "Gasto_saude": "gasto_saude_pct_pib",
        "Taxa_escolarizacao": "taxa_escolarizacao_pct",
        "Taxa_alfabetizacao": "taxa_alfabetizacao_pct"
    }, inplace=True)

    df_final = pd.merge(df_indicadores, df_covid, on="pais_nome", how="left")
    print(f"[OK] Dados cruzados: {df_final.shape[0]} países.")
    return df_final


def salvar_csv(df_final, caminho="data/analise_impacto_covid_socioeconomico.csv"):
    """Salva o DataFrame final em CSV (formatado para Excel/Power BI)."""
    colunas = [
        "pais_nome", "cases",
        "pib_total_usd", "pib_per_capita_usd",
        "taxa_desemprego", "expectativa_vida_anos",
        "gasto_saude_pct_pib", "taxa_alfabetizacao_pct", "taxa_escolarizacao_pct"
    ]

    df_final = df_final[[col for col in colunas if col in df_final.columns]]
    
    # Exportação com separador ";" para facilitar leitura no Excel/BI
    df_final.to_csv(caminho, index=False, sep=";", encoding="utf-8", na_rep="-")
    print(f"[💾] CSV salvo com sucesso em: {caminho}")


def etl_analises():
    """Executa o pipeline de análise cruzada entre COVID e indicadores."""
    df_covid = extrair_casos_covid()
    df_indicadores = extrair_indicadores_socioeconomicos()
    df_final = cruzar_covid_e_indicadores(df_covid, df_indicadores)
    salvar_csv(df_final)
    
    print("\n📊 Preview final:")
    print(df_final.head())


if __name__ == "__main__":
    etl_analises()
