import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import time
import random

async def scrape_detail():
    # Carrega o CSV de listagem
    df_listagem = pd.read_csv("C:/Users/vbitu/projects/fake-news-etl-project/data/raw/dados_listagem_aosfatos.csv")

    # Teste com 2 registros apenas
    df_teste = df_listagem.head(2)

    dados_detalhados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Deixa headless=False só para conferirmos o carregamento
        context = await browser.new_context()
        page = await context.new_page()

        for index, row in df_teste.iterrows():
            link = row['link']
            print(f"Processando: {link}")

            try:
                await page.goto(link, timeout=60000)
                await page.wait_for_load_state("networkidle", timeout=60000)
                await asyncio.sleep(2)

                # Data de publicação
                try:
                    data_element = await page.locator("aside.text-sm.text-center.mb-5").inner_text()
                    data_publicacao = data_element.strip()
                except:
                    data_publicacao = "não encontrado"

                # Conteúdo completo (todos os parágrafos)
                try:
                    parags = await page.locator("div#entry-content p").all_inner_texts()
                    conteudo_completo = " ".join([p.strip() for p in parags])
                except:
                    conteudo_completo = "não encontrado"

                dados_detalhados.append({
                    'link': link,
                    'data_publicacao': data_publicacao,
                    'conteudo_completo': conteudo_completo
                })

            except Exception as e:
                print(f"Erro no link {link}: {e}")

            time.sleep(random.uniform(1, 2))

        await browser.close()

    # Salva o resultado no processed
    df_detalhes = pd.DataFrame(dados_detalhados)
    df_detalhes.to_csv("C:/Users/vbitu/projects/fake-news-etl-project/data/processed/dados_detalhados_aosfatos_parcial.csv", index=False, encoding="utf-8-sig")

    print("Coleta parcial finalizada com sucesso!")
    print(df_detalhes.head())

if __name__ == "__main__":
    asyncio.run(scrape_detail())

