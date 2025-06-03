import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import time
import random

async def scrape_detail():
    df_listagem = pd.read_csv("C:/Users/vbitu/projects/fake-news-etl-project/data/raw/dados_listagem_aosfatos.csv")
    df_teste = df_listagem.head(2)

    dados_detalhados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for index, row in df_teste.iterrows():
            link = row['link']
            print(f"Processando: {link}")

            try:
                await page.goto(link, timeout=60000)
                await page.wait_for_load_state("networkidle", timeout=20000)

                # Data de publicação
                try:
                    data_element = await page.query_selector("time")
                    data_publicacao = await data_element.get_attribute("datetime")
                except:
                    data_publicacao = "não encontrado"

                # Resumo
                try:
                    resumo_element = await page.query_selector("div.prose p")
                    resumo = await resumo_element.inner_text()
                except:
                    resumo = "não encontrado"

                # Fonte
                try:
                    fonte_element = await page.query_selector("strong:has-text('Fonte')")
                    fonte = await fonte_element.inner_text()
                except:
                    fonte = "não encontrado"

                dados_detalhados.append({
                    'link': link,
                    'data_publicacao': data_publicacao,
                    'resumo': resumo,
                    'fonte': fonte
                })

            except Exception as e:
                print(f"Erro no link {link}: {e}")

            time.sleep(random.uniform(1, 2))

        await browser.close()

    df_detalhes = pd.DataFrame(dados_detalhados)
    print(df_detalhes.head())

if __name__ == "__main__":
    asyncio.run(scrape_detail())



