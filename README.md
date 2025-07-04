```markdown
# Fake News ETL Project

Projeto para coleta, processamento, classificação e análise de dados de notícias falsas, utilizando técnicas de web scraping, NLP, e APIs do ChatGPT para classificação temática e de vereditos.

---

## Estrutura do Projeto

```

fake-news-etl-project/
│
├── data/                      # Dados usados no projeto
│   ├── external/              # Dados externos / fontes públicas
│   ├── interim/               # Dados intermediários processados
│   ├── processed/             # Dados finais prontos para análise
│   ├── public/                # Dados públicos para download
│   └── raw/                   # Dados brutos coletados via scraping
│
├── dashboard/                 # Dashboards criados (Power BI)
│   └── dashboard\_fake\_news\_v1.pbix
│
├── docs/                     # Documentação do projeto
│
├── models/                   # Modelos treinados e scripts de ML
│
├── notebooks/                # Notebooks exploratórios e experimentais
│   ├── exploratory/          # Análises exploratórias e pré-processamento
│   ├── experiments/          # Tentativas experimentais não usadas
│   └── public\_dataset/       # Tratamento de datasets públicos
│
├── references/               # Referências e material extra
│
├── reports/                  # Relatórios e figuras geradas
│
├── scripts/                  # Scripts de ETL, classificação e scraping
│
├── src/                      # Código fonte modularizado (features, modelos, visualização)
│
├── .gitignore
├── LICENSE
├── Makefile
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências do projeto
└── setup.py

````

---

## Descrição das principais etapas

- **Coleta de dados:** Web scraping com Selenium e Playwright (`scripts/01_scraping_listagem_selenium.py`, `scripts/02_scraping_detalhes_playwright.py`).
- **Tratamento e merge:** Consolidação dos dados coletados em datasets prontos (`scripts/03_merge_scraping.py`).
- **Classificação:** Uso da API do ChatGPT para classificação temática e de vereditos (`scripts/07_classificacao_fake_news_chatgpt.py`, `scripts/09_classificacao_vereditos_chatgpt.py`).
- **Análise exploratória:** Notebooks para análise dos dados e visualização (`notebooks/exploratory/`, `notebooks/08_analise_classificacao_chatgpt.ipynb`).
- **Dashboard:** Visualização interativa via Power BI (`dashboard/dashboard_fake_news_v1.pbix`).

---

## Como rodar o projeto

1. Configure sua chave API do OpenAI como variável de ambiente:

```bash
export OPENAI_API_KEY='sua-chave-aqui'  # Linux / macOS
setx OPENAI_API_KEY "sua-chave-aqui"    # Windows PowerShell
````

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute os scripts na ordem para coleta, tratamento, classificação e análise.

4. Abra os notebooks para exploração ou visualize o dashboard no Power BI.

---

## Contato

Criado por Victor Hugo Bitu Patricio – [LinkedIn](https://www.linkedin.com/in/vhbitu/)

---

## .gitignore sugerido

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.env
*.env

# Dados
data/raw/
data/interim/
data/processed/

# Dashboards grandes (Power BI)
dashboard/*.pbix

# VS Code
.vscode/

# Outros
.DS_Store
```

---

## requirements.txt básico (baseado no que usou)

```txt
pandas
matplotlib
seaborn
openai
playwright
```

---

## Exemplo simples de Makefile

```makefile
.PHONY: all clean

all: coletar tratar classificar analisar

coletar:
	python scripts/01_scraping_listagem_selenium.py
	python scripts/02_scraping_detalhes_playwright.py
	python scripts/03_merge_scraping.py

tratar:
	python scripts/04_diagnostico_dados.py

classificar:
	python scripts/07_classificacao_fake_news_chatgpt.py
	python scripts/09_classificacao_vereditos_chatgpt.py

analisar:
	jupyter nbconvert --to notebook --execute notebooks/exploratory/08_analise_classificacao_chatgpt.ipynb
```

---

