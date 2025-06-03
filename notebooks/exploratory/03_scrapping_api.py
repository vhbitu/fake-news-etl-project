import requests
import pandas as pd
import time

# Configurações iniciais
BASE_URL = "https://api.aosfatos.org/posts"
PARAMS = {
    "format": "checagem",
    "per_page": 12,  # Padrão de paginação da API
    "page": 1
}

# Lista onde armazenaremos os dados coletados
dados_coletados = []

# Descobrimos que o site possui 372 páginas (ajuste aqui se necessário)
TOTAL_PAGINAS = 372

for pagina in range(1, TOTAL_PAGINAS + 1):
    print(f"Processando página {pagina} de {TOTAL_PAGINAS}...")

    # Atualiza o número da página nos parâmetros
    PARAMS["page"] = pagina

    # Faz a requisição para a API
    resposta = requests.get(BASE_URL, params=PARAMS)

    # Verifica se a requisição foi bem sucedida
    if resposta.status_code == 200:
        dados_json = resposta.json()

        for item in dados_json['results']:
            dados = {
                "id": item.get("id"),
                "titulo": item.get("title"),
                "slug": item.get("slug"),
                "veredito": item.get("verdict_label"),
                "data_publicacao": item.get("published_at"),
                "tags": [tag.get("name") for tag in item.get("tags", [])],
                "resumo": item.get("summary"),
                "fonte": item.get("source"),
                "conteudo": item.get("content")
            }
            dados_coletados.append(dados)

    else:
        print(f"Erro na página {pagina}: Status {resposta.status_code}")

    # Pequena pausa para não sobrecarregar o servidor
    time.sleep(0.5)

# Converte a lista em DataFrame
df = pd.DataFrame(dados_coletados)

# Salva o resultado final
df.to_csv("C:/Users/vbitu/projects/fake-news-etl-project/data/processed/dados_detalhados_aosfatos.csv", index=False, encoding="utf-8-sig")

print("Coleta finalizada com sucesso!")

