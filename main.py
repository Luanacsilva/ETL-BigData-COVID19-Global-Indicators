import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.etl_analises import etl_analises
from src.etl_covid import etl_covid_global
from src.etl_worldbank import etl_worldbank
from src.etl_tendencias import etl_tendencias, montar_temporal, salvar_csv

def menu():
    while True:
        print("\n=== MENU DE EXECUÇÃO DE ETLs ===")
        print("1. Executar ETL de Análise Cruzada (COVID + Indicadores)")
        print("2. Executar ETL de Dados Históricos de COVID (Global)")
        print("3. Executar ETL de Indicadores Socioeconômicos (World Bank)")
        print("4. Gerar Série Temporal por País")
        print("5. Executar ETL de Tendências Temporais")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        match escolha:
            case "1":
                etl_analises()
            case "2":
                etl_covid_global()
            case "3":
                etl_worldbank()
            case "4":
                pais_nome = input("Nome do país (ex: Brazil): ")
                pais_iso3 = input("Código ISO3 (ex: BRA): ")
                df = montar_temporal(pais_nome, pais_iso3)
                salvar_csv(df, pais_nome)
            case "5":
                etl_tendencias()
            case "0":
                print("Saindo...")
                sys.exit()
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
