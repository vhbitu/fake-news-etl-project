import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import time
import random

async def scrape_detail():
    df_listagem = pd.read_csv("C:/Users/vbitu/projects/fake-news-etl-project/data/raw/dados_listagem_aosfatos.csv")

    # Teste ainda com 2 links antes de escalar
    df_teste = df_listagem.head(2)

    dados_detalhados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Deixe headless=False até validarmos tudo
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

                # Resumo (primeiro parágrafo do conteúdo)
                try:
                    resumo_element = await page.locator("div#entry-content p").nth(0).inner_text()
                    resumo = resumo_element.strip()
                except:
                    resumo = "não encontrado"

                dados_detalhados.append({
                    'link': link,
                    'data_publicacao': data_publicacao,
                    'resumo': resumo
                })

            except Exception as e:
                print(f"Erro no link {link}: {e}")

            time.sleep(random.uniform(1, 2))

        await browser.close()

    df_detalhes = pd.DataFrame(dados_detalhados)
    print(df_detalhes.head())

if __name__ == "__main__":
    asyncio.run(scrape_detail())

