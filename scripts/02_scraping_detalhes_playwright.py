import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import time
import random
import os

# Caminhos padronizados
CAMINHO_ENTRADA = "data/raw/dados_listagem_aosfatos.csv"
CAMINHO_SAIDA = "data/processed/dados_detalhados_aosfatos.csv"

async def scrape_detail():
    print("Iniciando coleta de dados detalhados com Playwright...")

    # Carrega o CSV com os links das checagens
    if not os.path.exists(CAMINHO_ENTRADA):
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {CAMINHO_ENTRADA}")
    
    df_listagem = pd.read_csv(CAMINHO_ENTRADA)
    dados_detalhados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for index, row in df_listagem.iterrows():
            link = row['link']
            print(f"Processando: {link}")

            try:
                await page.goto(link, timeout=60000)
                await page.wait_for_load_state("networkidle", timeout=60000)
                await asyncio.sleep(2)

                # Extração da data de publicação
                try:
                    data_element = await page.locator("aside.text-sm.text-center.mb-5").inner_text()
                    data_publicacao = data_element.strip()
                except:
                    data_publicacao = "não encontrado"

                # Extração do conteúdo completo da checagem
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

            # Pausa aleatória para evitar bloqueios
            time.sleep(random.uniform(1, 2))

        await browser.close()

    # Salvar arquivo final com os dados detalhados
    df_detalhes = pd.DataFrame(dados_detalhados)
    df_detalhes.to_csv(CAMINHO_SAIDA, index=False, encoding="utf-8-sig")

    print("✅ Coleta finalizada com sucesso!")
    print(df_detalhes.head())

if __name__ == "__main__":
    asyncio.run(scrape_detail())

