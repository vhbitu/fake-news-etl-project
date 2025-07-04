"""
Script de classificação temática de títulos de fake news usando API do ChatGPT.

Este script foi desenvolvido para processar o dataset por lotes, evitando sobrecarga na API.
Os intervalos são definidos pelas variáveis INICIO e FIM.
Cada execução gera um arquivo separado com as classificações, que posteriormente serão unificadas.

Exemplo de arquivos gerados:
- dados_classificados_chatgpt_0_100.csv
- dados_classificados_chatgpt_101_2500.csv
- dados_classificados_chatgpt_2501_4419.csv

Autor: Victor Hugo Bitu
"""
# scripts/07_classificacao_fake_news_chatgpt.py

import os
import pandas as pd
import openai
import time

print("Iniciando o script de classificação...")

# Configurar sua API Key via variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("AVISO: OPENAI_API_KEY não está definida. Configure a variável de ambiente.")

# Caminho do arquivo de entrada (relativo ao projeto)
INPUT_PATH = os.path.join("data", "processed", "dados_unificados_aosfatos.csv")

# Configuração do intervalo para execuções em lote
INICIO = 2501
FIM = 4419

# Caminho de saída baseado no intervalo
OUTPUT_PATH = os.path.join("data", "processed", f"dados_classificados_chatgpt_{INICIO}_{FIM}.csv")

# Carregar o dataset
print("Carregando os dados...")
df = pd.read_csv(INPUT_PATH)
df = df.dropna(subset=["titulo"]).reset_index(drop=True)

# Corrigir FIM se exceder o número de linhas
FIM = min(FIM, len(df))
amostra = df.iloc[INICIO:FIM].copy().reset_index(drop=True)
print(f"Total de títulos a classificar: {len(amostra)}")

# Categorias da taxonomia temática de fake news
categorias = [
    "Política e Eleições",
    "Saúde e Pandemias",
    "Economia e Crise Financeira",
    "Conspirações Globais",
    "Segurança Pública e Violência",
    "Meio Ambiente e Catástrofes",
    "Tecnologia e Redes Sociais",
    "Grupos Sociais, Ideologia e Moral",
    "Religião e Profecias",
    "Ciência e Pseudociência",
    "Personagens Públicos e Celebridades",
    "Outros / Não Classificado"
]

# Construção do prompt para a API
def construir_prompt(titulo):
    return (
        f"Classifique o seguinte título de notícia em uma das categorias abaixo, considerando que o universo é de fake news:\n"
        f"Título: {titulo}\n"
        f"Categorias possíveis: {', '.join(categorias)}\n"
        f"Responda apenas com o nome exato da categoria."
    )

# Função para chamar a API da OpenAI
def classificar_titulo(titulo):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": construir_prompt(titulo)}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao classificar: {titulo[:60]}... -> {e}")
        return "Erro"

# Classificação dos títulos
resultados = []
for idx, row in amostra.iterrows():
    print(f"Classificando {idx + 1}/{len(amostra)}...")
    categoria = classificar_titulo(row['titulo'])
    resultados.append(categoria)
    time.sleep(1.5)  # evitar rate limit

# Salvar os resultados
amostra['categoria_chatgpt'] = resultados
amostra.to_csv(OUTPUT_PATH, index=False)
print("Classificação concluída e salva em:", OUTPUT_PATH)
