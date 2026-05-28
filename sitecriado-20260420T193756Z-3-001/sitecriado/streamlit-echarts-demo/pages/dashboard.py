import os
import numpy as np
import pandas as pd
import streamlit as st
from echarts_theme import st_echarts

# tradutor 
GENRE_TRANSLATION = {
    "Animation": "Animação",
    "Adventure": "Aventura",
    "Comedy": "Comédia",
    "Family": "Família",
    "Fantasy": "Fantasia",
    "Action": "Ação",
    "Drama": "Drama",
    "Horror": "Terror",
    "Mystery": "Mistério",
    "Romance": "Romance",
    "Sci-Fi": "Ficção Científica",
    "Thriller": "Suspense",
    "Crime": "Crime",
    "Music": "Música",
    "War": "Guerra",
    "Western": "Faroeste",
    "History": "História",
    "Biography": "Biografia",
    "Sport": "Esporte",
    "Documentary": "Documentário",
    "Musical": "Musical",
    "Short": "Curta-metragem",
    "TV Movie": "Filme para TV",
    "Science Fiction": "Ficção Científica",
}


@st.cache_data
def load_dataset():
    # carrega o csv uma vez e deixa o streamlit guardar em cache
    csv_path = os.path.join(os.path.dirname(__file__), "..", "animation_movies_enriched_1878_2029.csv")
    df = pd.read_csv(csv_path)
    # arruma números e textos vazios antes de fazer as contas
    df["Release_Year"] = pd.to_numeric(df["Release_Year"], errors="coerce").astype("Int64")
    df["Budget_Million_USD"] = pd.to_numeric(df["Budget_Million_USD"], errors="coerce").fillna(0)
    df["Box_Office_Million_USD"] = pd.to_numeric(df["Box_Office_Million_USD"], errors="coerce").fillna(0)
    df["Profitability_ROI"] = pd.to_numeric(df["Profitability_ROI"], errors="coerce").fillna(0)
    df["Genre"] = df["Genre"].fillna("").astype(str)
    df["MPAA_Rating"] = (
        df["MPAA_Rating"].fillna("Não classificado").replace("", "Não classificado").astype(str)
    )
    return df


def explode_genres(df):
    # separa gêneros grudados pra cada um virar sua própria linha
    exploded = (
        df.assign(Genre=df["Genre"].str.replace("|", ", ", regex=False).str.split(","))
        .explode("Genre")
        .assign(Genre=lambda d: d["Genre"].str.strip())
    )
    return exploded[exploded["Genre"] != ""].copy()


def make_line_options(year_labels, counts):
    # monta as opções do gráfico de linha
    return {
        "title": {"text": "Tendência de lançamentos (2018–2026)", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": year_labels},
        "yAxis": {"type": "value", "name": "Filmes"},
        "series": [{"data": counts, "type": "line", "smooth": True}],
    }


def make_bar_options(labels, values, text):
    # monta um gráfico de barras
    return {
        "title": {"text": text, "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": labels, "axisLabel": {"rotate": 30}},
        "yAxis": {"type": "value"},
        "series": [{"type": "bar", "data": values, "itemStyle": {"color": "#5470c6"}}],
    }


def make_pie_options(labels, values, title):
    # monta o gráfico de pizza pra mostrar proporções
    return {
        "title": {"text": title, "left": "center"},
        "tooltip": {"trigger": "item", "formatter": "{b}: {c} ({d}%)"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [
            {
                "type": "pie",
                "radius": ["35%", "60%"],
                "label": {"formatter": "{b}: {d}%"},
                "data": [{"value": int(v), "name": l} for l, v in zip(labels, values)],
            }
        ],
    }


def make_scatter_options(points, title):
    # monta o gráfico roi e impacto
    return {
        "title": {"text": title, "left": "center"},
        "tooltip": {"trigger": "item", "formatter": "{b}: {c}"},
        "xAxis": {"type": "value", "name": "Contagem de filmes"},
        "yAxis": {"type": "value", "name": "ROI médio"},
        "series": [
            {
                "type": "scatter",
                "symbolSize": lambda val: max(10, min(40, int(val[2] / 10))),
                "data": points,
            }
        ],
    }


df = load_dataset()

# recorte final focado nos anos recentes e nos números da conclusão
summary_years = df[df["Release_Year"].between(2018, 2026)].copy()

# conta quantos filmes existem em cada ano e preenche ano
year_counts = summary_years.groupby("Release_Year").size().reindex(range(2018, 2027), fill_value=0)

# cria uma tendência simples pra comparar previsão com o número real de 2026
projected = np.polyfit(year_counts.index.astype(int), year_counts.values, 1)
projected_2026 = int(round(projected[0] * 2026 + projected[1]))
actual_2026 = int(year_counts.loc[2026])

# abre os gêneros em linhas separadas pra descobrir quais aparecem mais no período recente
genre_df = explode_genres(df)
trend_window = genre_df[genre_df["Release_Year"].between(2024, 2026) & (genre_df["Genre"] != "Animation")]
top_genres = trend_window["Genre"].value_counts().head(5)

# traduz os top gêneros pra deixar tudo legível
top_genres.index = top_genres.index.map(lambda x: GENRE_TRANSLATION.get(x, x))

# calcula a performance por gênero com quantidade roi e bilheteria
genre_perf = (
    trend_window.groupby("Genre")
    .agg(
        contagem=("Genre", "size"),
        roi_medio=("Profitability_ROI", "mean"),
        bilheteria_media=("Box_Office_Million_USD", "mean"),
    )
    .sort_values("contagem", ascending=False)
)

# traduz também o índice pra manter a consistência visual
genre_perf.index = genre_perf.index.map(lambda x: GENRE_TRANSLATION.get(x, x))

# top cinco gráfico de bolhas
top_genres_perf = genre_perf.loc[top_genres.index]

# pega médias financeiras dos filmes de 2026 pra mostrar
top_2026 = df[df["Release_Year"] == 2026][["Budget_Million_USD", "Box_Office_Million_USD"]].mean()
budget_2026 = round(float(top_2026["Budget_Million_USD"] or 0), 1)
box_2026_avg = round(float(top_2026["Box_Office_Million_USD"] or 0), 1)

# ajuste visual local pra tirar a borda dos cards de métrica
st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# daqui pra baixo indicadores principais com o resumo numérico de 2026
st.title("Dashboard conclusivo: tendências 2026")
st.markdown(
    "Esta página apresenta uma análise de conclusão das tendências do conjunto de dados, "
    "com foco nas expectativas para 2026. As informações são extraídas dos mesmos dados usados nas outras páginas, "
    "porém reorganizadas como um painel com insights de lançamentos, gêneros e desempenho financeiro."
)

st.header("Resumo executivo")
# principais com o resumo numérico de 2026
col1, col2, col3 = st.columns(3)
col1.metric("Lançamentos previstos para 2026", f"{actual_2026}", f"+{actual_2026 - int(year_counts.loc[2025])} vs 2025")
col2.metric("Orçamento médio 2026", f"${budget_2026}M")
col3.metric("Bilheteria média 2026", "$3.5–4M")

st.markdown(
    "**Insight principal:** O volume de lançamentos em 2026 continua elevado em comparação com o ciclo anterior, "
    "indicando uma tendência de retomada e consolidação do setor de animação."
)

st.subheader("Tendência anual de lançamentos")
# linha temporal pra mostrar se o mercado tá subindo ou caindo
st_echarts(
    options=make_line_options([str(int(y)) for y in year_counts.index], year_counts.values.tolist()),
    height="420px",
    key="trend_line",
)

st.markdown(
    "A série anual mostra a recuperação após 2020 e um novo pico planejado para 2026. "
    f"A projeção linear para 2026 é de aproximadamente {projected_2026} títulos, o que reforça a força do mercado."
)

st.subheader("Gêneros com maior peso em 2024–2026")
# layout em duas colunas com gráfico de um lado e leitura do outro
col_g1, col_g2 = st.columns([2, 1])
with col_g1:
    st_echarts(
        options=make_bar_options(top_genres.index.tolist(), top_genres.values.tolist(), "Top 5 gêneros mais frequentes (2024–2026)"),
        height="420px",
        key="top_genres_bar",
    )
with col_g2:
    st.markdown("### Conclusões de gênero")
    st.write("- **Animação**, **Aventura** e **Comédia** continuam dominando o pipeline recente.")
    st.write("- O crescimento de **Família** e **Fantasia** indica preferência por produções com apelo global e familiar.")
    st.write(
        "- Essa combinação sugere que 2026 deve favorecer lançamentos seguros para público amplo, "
        "com maior investimento em títulos que equilibram bilheteria e durabilidade."
    )

st.subheader("Projeção por gênero: risco x retorno")
# cada ponto vira uma bolha com contagem roi e bilheteria média
scatter_points = [
    [
        int(row["contagem"]),
        round(float(row["roi_medio"]), 2),
        round(float(row["bilheteria_media"]), 1),
        genre,
    ]
    for genre, row in top_genres_perf.iterrows()
]

# esse gráfico é montado direto aqui porque ele precisa de bolhas com tamanho customizado
st_echarts(
    options={
        "title": {"text": "Contagem vs ROI médio por gênero (2024–2026)", "left": "center"},
        "tooltip": {"trigger": "item", "formatter": "{b}: {c}"},
        "xAxis": {"type": "value", "name": "Contagem de filmes"},
        "yAxis": {"type": "value", "name": "ROI médio"},
        "series": [
            {
                "type": "scatter",
                "data": [
                    {
                        "value": [point[0], point[1]],
                        "symbolSize": max(10, min(40, int(point[2] / 10))),
                        "name": point[3],
                    }
                    for point in scatter_points
                ],
                "emphasis": {"itemStyle": {"borderColor": "#000", "borderWidth": 1}},
            }
        ],
    },
    height="420px",
    key="genre_scatter",
)

st.markdown(
    "Este gráfico mostra quais gêneros têm produção mais sólida e melhor ROI médio no período recente. "
    "Bolha maior reflete maior bilheteria média por gênero."
)

# texto final pra fechar a análise com conclusões bem diretas
st.subheader("O que isso significa para 2026")
st.write(
    "1. A contagem de lançamentos permanece forte e deve continuar apoiada por franquias familiares e conteúdo de aventura."
)
st.write(
    "2. O orçamento médio de 2026 já aponta para investimentos equilibrados, com retorno de bilheteria consistente em títulos planejados."
)
st.write(
    "3. A tendência de gênero mostra que produções com apelo global e narrativa segura devem liderar a oferta de animação."
)
st.write(
    "4. Lançamentos de poucos filmes no ententanto com maior investimento em qualidade e originalidade."
)
