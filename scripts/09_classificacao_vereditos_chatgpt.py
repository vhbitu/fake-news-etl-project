# Classificação de vereditos ausentes com ChatGPT API

import pandas as pd
import openai
import os
import time

# Configurar sua chave da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Caminho do arquivo de entrada
CAMINHO_DADOS = r"C:\\Users\\vbitu\\projects\\fake-news-etl-project\\data\\interim\\dados_classificados_completos.csv"
df = pd.read_csv(CAMINHO_DADOS)

# Filtrar registros com veredito indisponível
coluna_veredito = 'veredito'

if coluna_veredito not in df.columns:
    raise ValueError("Coluna 'veredito' não encontrada no dataset.")

df_faltantes = df[df[coluna_veredito].str.lower() == 'indisponível'].copy()
print(f"Total de registros a classificar: {len(df_faltantes)}")

# Lista de vereditos possíveis
vereditos_possiveis = [
    "distorcido",
    "exagerado",
    "falso",
    "impreciso",
    "insustentável",
    "não é bem assim"
]

# Função para construir o prompt
def construir_prompt(conteudo):
    return (
        f"Classifique o seguinte conteúdo de notícia no contexto de veredito de checagem:\n"
        f"Conteúdo: {conteudo}\n"
        f"Escolha entre: {', '.join(vereditos_possiveis)}\n"
        f"Responda apenas com um dos termos da lista, sem explicação."
    )

# Função de classificação via API
def classificar_veredito(texto):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": construir_prompt(texto)}],
            temperature=0
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print("Erro:", e)
        return "erro"

# Classificação
vereditos_gerados = []
for i, row in df_faltantes.iterrows():
    print(f"Classificando {i+1}/{len(df_faltantes)}...")
    conteudo = row['conteudo_completo']
    veredito = classificar_veredito(conteudo)
    vereditos_gerados.append(veredito)
    time.sleep(1.5)

# Atualiza os vereditos classificados no DataFrame original
df.loc[df[coluna_veredito].str.lower() == 'indisponível', coluna_veredito] = vereditos_gerados

# Salvar nova versão
CAMINHO_SAIDA = r"C:\\Users\\vbitu\\projects\\fake-news-etl-project\\data\\interim\\dados_classificados_completos_atualizado.csv"
df.to_csv(CAMINHO_SAIDA, index=False)
print("Classificação concluída. Arquivo salvo em:", CAMINHO_SAIDA)
