import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração geral do Streamlit
st.set_page_config(page_title="Fake News Temáticas", layout="centered")
st.title("Fake News Temáticas - Dashboard Interativo (V2 PRO)")

# Caminho relativo seguro
base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, '..', 'data', 'public', 'dataset_fake_news_tagueado.csv')

# Leitura do dataset público final
df = pd.read_csv(csv_path)

# Garantindo o tipo datetime da data_publicacao
df['data_publicacao'] = pd.to_datetime(df['data_publicacao'], errors='coerce')
df['ano'] = df['data_publicacao'].dt.year

# Aplicando o filtro temporal de 2018+
df = df[df['ano'] >= 2018]

# Subtemas e Narrativas
subtemas = [
    'boataria_politica', 'pseudociencia', 'negacionismo_climatico',
    'politicas_publicas', 'inteligencia_artificial', 'fraudes_digitais',
    'tecnopolitica', 'autoritarismo', 'discurso_oficial',
    'revisionismo_historico', 'discurso_de_odio', 'exploracao_tragedia'
]

historias = {
    'inteligencia_artificial': "A partir de 2023 houve um crescimento acelerado de notícias relacionadas à IA, refletindo o avanço dos modelos generativos e sua entrada no cotidiano.",
    'pseudociencia': "Momentos de crise sanitária frequentemente elevam o volume de notícias com curas não comprovadas e tratamentos pseudocientíficos.",
    'fraudes_digitais': "Com a digitalização forçada na pandemia, observou-se um aumento relevante nas fraudes digitais e golpes online.",
    'negacionismo_climatico': "As narrativas de negacionismo climático acompanham debates internacionais e eventos ambientais extremos.",
    'boataria_politica': "A boataria política mantém volume constante, principalmente em ciclos eleitorais e cenários polarizados.",
}

# Interface interativa - Multiselect
subtemas_selecionados = st.multiselect(
    "Selecione um ou mais subtemas:", 
    subtemas, 
    default=['inteligencia_artificial']
)

if not subtemas_selecionados:
    st.warning("Por favor, selecione pelo menos um subtema para visualizar o gráfico.")
    st.stop()

# Geração do gráfico
df_grouped = df.groupby('ano')[subtemas_selecionados].sum()

plt.figure(figsize=(8, 5))
sns.set_palette("tab10")

for subtema in subtemas_selecionados:
    plt.plot(df_grouped.index, df_grouped[subtema], marker='o', label=subtema.replace('_',' ').title())

plt.title("Evolução Temporal dos Subtemas Selecionados")
plt.ylabel("Quantidade de Notícias")
plt.xlabel("Ano")
plt.xticks(df_grouped.index)
plt.legend()
plt.grid(visible=True, linestyle='--', alpha=0.5)
plt.tight_layout()

st.pyplot(plt.gcf())

# Narrativa (se houver apenas 1 subtema selecionado)
if len(subtemas_selecionados) == 1:
    st.subheader("Narrativa do Subtema")
    tema = subtemas_selecionados[0]
    if tema in historias:
        st.write(historias[tema])
    else:
        st.write("Narrativa ainda não cadastrada para este subtema.")


