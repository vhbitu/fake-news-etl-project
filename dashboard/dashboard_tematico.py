# ===============================
# DASHBOARD FAKE NEWS TEMÁTICAS - MVP FINAL
# ===============================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# Leitura do dataset público final
# ===============================

# Caminho para o dataset gerado na última etapa
df = pd.read_csv(r'C:\Users\vbitu\projects\fake-news-etl-project\data\public\dataset_fake_news_tagueado.csv')

# Garantindo o tipo datetime da data_publicacao
df['data_publicacao'] = pd.to_datetime(df['data_publicacao'], errors='coerce')
df['ano'] = df['data_publicacao'].dt.year

# ===============================
# Configurações de subtemas
# ===============================

subtemas = [
    'boataria_politica', 'pseudociencia', 'negacionismo_climatico',
    'politicas_publicas', 'inteligencia_artificial', 'fraudes_digitais',
    'tecnopolitica', 'autoritarismo', 'discurso_oficial',
    'revisionismo_historico', 'discurso_de_odio', 'exploracao_tragedia'
]

# Narrativas iniciais (podemos ampliar depois)
historias = {
    'inteligencia_artificial': "A partir de 2023 houve um crescimento acelerado de notícias relacionadas à IA, refletindo o avanço dos modelos generativos e sua entrada no cotidiano.",
    'pseudociencia': "Momentos de crise sanitária frequentemente elevam o volume de notícias com curas não comprovadas e tratamentos pseudocientíficos.",
    'fraudes_digitais': "Com a digitalização forçada na pandemia, observou-se um aumento relevante nas fraudes digitais e golpes online.",
    'negacionismo_climatico': "As narrativas de negacionismo climático acompanham debates internacionais e eventos ambientais extremos.",
    'boataria_politica': "A boataria política mantém volume constante, principalmente em ciclos eleitorais e cenários polarizados.",
    # Demais subtemas ainda sem narrativa (podemos adicionar aos poucos)
}

# ===============================
# Interface do Dashboard
# ===============================

st.set_page_config(page_title="Fake News Temáticas", layout="wide")
st.title("📰 Fake News Temáticas - Dashboard Interativo")

# Filtro de seleção
subtema_escolhido = st.selectbox("Selecione um subtema:", subtemas)

# Filtragem temporal (2018+)
df_filtro = df[df['ano'] >= 2018]

# Geração da série temporal do subtema
df_grouped = df_filtro.groupby('ano')[subtema_escolhido].sum()

fig, ax = plt.subplots(figsize=(10, 5))
df_grouped.plot(kind='bar', ax=ax, color='skyblue')
plt.title(f"Evolução Temporal - {subtema_escolhido.replace('_',' ').title()}")
plt.ylabel("Quantidade de Notícias")
plt.xlabel("Ano")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Mostrar a mini história (se existir)
st.subheader("📝 Narrativa do Subtema")
if subtema_escolhido in historias:
    st.write(historias[subtema_escolhido])
else:
    st.write("Narrativa ainda não cadastrada para este subtema.")
