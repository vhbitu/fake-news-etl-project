import os
import time
import pandas as pd
import openai

print("Iniciando preenchimento de vereditos ausentes com ChatGPT...")

# Configurar a chave da OpenAI via variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise EnvironmentError("A variável de ambiente OPENAI_API_KEY não está definida.")

# Caminho do arquivo de entrada
CAMINHO_DADOS = "data/interim/dados_classificados_completos.csv"
df = pd.read_csv(CAMINHO_DADOS)

# Verificar se a coluna de veredito existe
coluna_veredito = "veredito"
if coluna_veredito not in df.columns:
    raise ValueError(f"Coluna '{coluna_veredito}' não encontrada no dataset.")

# Filtrar registros com veredito 'indisponível'
df_faltantes = df[df[coluna_veredito].str.lower() == "indisponível"].copy()
print(f"Total de registros com veredito ausente: {len(df_faltantes)}")

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
        "Classifique o seguinte conteúdo de notícia no contexto de veredito de checagem:\n"
        f"Conteúdo: {conteudo}\n"
        f"Escolha entre: {', '.join(vereditos_possiveis)}\n"
        "Responda apenas com um dos termos da lista, sem explicação."
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
        print(f"Erro na classificação: {e}")
        return "erro"

# Classificação dos vereditos ausentes
vereditos_gerados = []
for i, row in df_faltantes.iterrows():
    print(f"Classificando {i + 1}/{len(df_faltantes)}...")
    veredito = classificar_veredito(row.get("conteudo_completo", ""))
    vereditos_gerados.append(veredito)
    time.sleep(1.5)  # evitar rate limiting da API

# Atualizar os vereditos classificados no DataFrame original
df.loc[df[coluna_veredito].str.lower() == "indisponível", coluna_veredito] = vereditos_gerados

# Salvar nova versão atualizada
CAMINHO_SAIDA = "data/interim/dados_classificados_completos_atualizado.csv"
df.to_csv(CAMINHO_SAIDA, index=False)
print("Classificação concluída. Arquivo salvo em:", CAMINHO_SAIDA)
