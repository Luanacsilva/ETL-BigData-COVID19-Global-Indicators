# 🌍 ETL-BigData-COVID19-Global-Indicators

> Análise Integrada do Impacto da Pandemia COVID-19 nos Indicadores Socioeconômicos Globais

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-green)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Luanacsilva/ETL-BigData-COVID19-Global-Indicators/pulls)

---

Este projeto visa construir um pipeline ETL (Extract, Transform, Load) que integra dados oficiais da pandemia de COVID-19 com indicadores socioeconômicos globais, permitindo análises comparativas entre países e regiões, e a criação de dashboards interativos para insights estratégicos.

---

## 🎯 Objetivo do Projeto

- Avaliar o impacto da pandemia de COVID-19 em diversos indicadores socioeconômicos globais.
- Construir um pipeline de dados completo, da extração à visualização, usando Big Data.
- Permitir análises dinâmicas e visuais para apoio à tomada de decisão.

---

## 📚 Tecnologias e Ferramentas Utilizadas

- **Python 3**
- **MongoDB**

---

## 🌐 Fontes de Dados

- [COVID-19 API (disease.sh)](https://disease.sh/docs/)
- [World Bank API](https://datahelpdesk.worldbank.org/)

---
# 🏁 Como Iniciar o Projeto

Siga os passos abaixo para rodar o projeto localmente:

---

###  1. Clone o repositório

```bash
git clone https://github.com/Luanacsilva/ETL-BigData-COVID19-Global-Indicators.git
cd ETL-BigData-COVID19-Global-Indicators
```
### 2. Crie e ative um ambiente virtual
```bash 
python -m venv venv
# Ativar no Windows:
venv\Scripts\activate
# Ativar no Mac/Linux:
source venv/bin/activate
```
### 3. Instale as dependências
```bash
pip install -r requirements.txt
pip freeze > requirements.txt
```
### 4. Configure o MongoDB
Certifique-se de ter o MongoDB instalado e rodando localmente ou configure sua conexão com Atlas (MongoDB na nuvem).

Atualize as variáveis de ambiente no arquivo .env com suas credenciais de conexão.

Exemplo de .env:
```bash
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=covid19_indicadores
```
# 5. Execute o projeto
Rodar o menu interativo para escolher os ETLs:
```bash
python src/etl_menu_interativo.py
```
Ou rodar scripts específicos:
```bash
python src/etl_covid.py
python src/etl_worldbank.py
python src/etl_analises.py
python src/etl_tendencias.py
```
---
## 🏗 Estrutura do Projeto

```bash
├── data/
│   └── analise_impacto_covid_sociedade.csv  # Resultado final do cruzamento de dados
│
├── src/
│   ├── etl_analises.py            # Geração do CSV final com análises integradas
│   ├── etl_covid.py               # Extração e transformação de dados da pandemia
│   ├── etl_tendencias.py          # Cálculo de tendências e médias móveis
│   ├── etl_worldbank.py           # Extração de indicadores socioeconômicos do Banco Mundial
│   ├── mongodb_connection.py      # Conexão e manipulação no MongoDB
│   └── etl_menu_interativo.py     # Menu interativo para execução dos ETLs
│
├── .gitignore
├── LICENSE
└── README.md
```
---
## ⚙️ Etapas do Pipeline ETL
Extração de Dados (Extract)

Dados diários da pandemia e indicadores econômicos/sociais.

Transformação de Dados (Transform)

Limpeza, padronização, cálculo de métricas derivadas e integração.

Carga de Dados (Load)

Armazenamento organizado no MongoDB.

Análises e Visualização

Geração de CSVs e construção de dashboards.
---
## 📊 Funcionalidades Principais

Coleta diária de dados da COVID-19.

Cálculo de tendências (médias móveis e taxas de crescimento).

Extração de múltiplos indicadores socioeconômicos.

Análises integradas COVID-19 vs. Indicadores Sociais.

Geração de relatórios e dashboards.

---


# 🛡️ Licença
Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo LICENSE para mais detalhes.
