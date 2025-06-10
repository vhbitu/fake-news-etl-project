import os
import pandas as pd
import openai
import time

print("Iniciando o script de classificação...")

# Configurar sua API Key via variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("AVISO: OPENAI_API_KEY não está definida. Configure a variável de ambiente.")

# Caminho do arquivo de entrada (ajuste se necessário)
INPUT_PATH = r"C:\\Users\\vbitu\\projects\\fake-news-etl-project\\data\\processed\\dados_unificados_aosfatos.csv"

# Configuração de intervalo para facilitar testes e execuções em lote
INICIO = 2501
FIM = 4419

# Caminho do arquivo de saída baseado no intervalo
OUTPUT_PATH = fr"C:\\Users\\vbitu\\projects\\fake-news-etl-project\\data\\processed\\dados_classificados_chatgpt_{INICIO}_{FIM}.csv"

# Carregar o dataset e selecionar o intervalo desejado
print("Carregando os dados...")
df = pd.read_csv(INPUT_PATH)
df = df.dropna(subset=["titulo"]).reset_index(drop=True)

# Corrigir FIM se for maior que o tamanho do dataset
FIM = min(FIM, len(df))
amostra = df.iloc[INICIO:FIM].copy().reset_index(drop=True)
print(f"Total de títulos a classificar: {len(amostra)}")

# Lista de categorias da taxonomia temática de desinformação
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

# Função para construir o prompt
def construir_prompt(titulo):
    prompt = (
        f"Classifique o seguinte título de notícia em uma das categorias abaixo, considerando que o universo é de fake news:\n"
        f"Título: {titulo}\n"
        f"Categorias possíveis: {', '.join(categorias)}\n"
        f"Responda apenas com o nome exato da categoria."
    )
    return prompt

# Função para chamar a API do ChatGPT usando nova interface da openai>=1.0.0
def classificar_titulo(titulo):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": construir_prompt(titulo)}
            ],
            temperature=0
        )
        categoria = response.choices[0].message.content.strip()
        return categoria
    except Exception as e:
        print(f"Erro ao classificar: {titulo[:60]}... -> {e}")
        return "Erro"

# Classificar todos os títulos do intervalo
resultados = []
for idx, row in amostra.iterrows():
    print(f"Classificando {idx + 1}/{len(amostra)}...")
    categoria = classificar_titulo(row['titulo'])
    resultados.append(categoria)
    time.sleep(1.5)  # pequena pausa para evitar rate limit

# Salvar resultado
amostra['categoria_chatgpt'] = resultados
amostra.to_csv(OUTPUT_PATH, index=False)
print("Classificação concluída e salva em:", OUTPUT_PATH)

