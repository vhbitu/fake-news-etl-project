
````markdown
# Fake News ETL Project

Projeto para coleta, processamento e análise de notícias falsas, usando scraping, NLP e ChatGPT para classificação.

---

## Estrutura do Projeto

- **data/**: dados brutos, processados, externos e públicos  
- **dashboard/**: dashboards em Power BI  
- **docs/**: documentação  
- **models/**: modelos e scripts ML  
- **notebooks/**: análises exploratórias e experimentos  
- **reports/**: relatórios e figuras  
- **scripts/**: scripts de scraping, ETL e classificação  
- **src/**: código modular (features, modelos, visualização)  
- Arquivos raiz: `.gitignore`, `LICENSE`, `Makefile`, `README.md`, `requirements.txt`, `setup.py`

---

## Etapas principais

1. **Coleta de dados:** Selenium e Playwright (scripts `01` e `02`)  
2. **Tratamento:** merge e limpeza (`03`)  
3. **Classificação:** ChatGPT para temas e vereditos (`07` e `09`)  
4. **Análise:** notebooks exploratórios (`08`)  
5. **Dashboard:** Power BI (`dashboard_fake_news_v1.pbix`)

---

## Como rodar

1. Configure a chave da API OpenAI:

```bash
# Linux/macOS
export OPENAI_API_KEY='sua-chave'

# Windows PowerShell
setx OPENAI_API_KEY "sua-chave"
````

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute os scripts na ordem indicada para coletar, tratar, classificar e analisar.

4. Explore os notebooks e visualize o dashboard no Power BI.

---

## Contato

Victor Hugo Bitu Patricio – [LinkedIn](https://www.linkedin.com/in/vhbitu/)

---

## .gitignore sugerido

```
__pycache__/
*.py[cod]
.env
data/raw/
data/interim/
data/processed/
dashboard/*.pbix
.vscode/
.DS_Store
```

---

## requirements.txt básico

```
pandas
matplotlib
seaborn
openai
playwright
```

---

## Makefile simples

```makefile
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


