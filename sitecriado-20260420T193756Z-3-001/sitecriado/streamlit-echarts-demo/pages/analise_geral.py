import os
import streamlit as st
import polars as pl
from streamlit_echarts import JsCode
from echarts_theme import st_echarts


# traduz o csv
GENRE_TRANSLATION = {
    "Action": "Ação",
    "Adventure": "Aventura",
    "Animation": "Animação",
    "Comedy": "Comédia",
    "Crime": "Crime",
    "Documentary": "Documentário",
    "Drama": "Drama",
    "Family": "Família",
    "Fantasy": "Fantasia",
    "History": "História",
    "Horror": "Horror",
    "Music": "Música",
    "Musical": "Musical",
    "Mystery": "Mistério",
    "Romance": "Romance",
    "Science Fiction": "Ficção Científica",
    "TV Movie": "Filme para TV",
    "Thriller": "Suspense",
    "War": "Guerra",
    "Western": "Faroeste",
}

COUNTRY_TRANSLATION = {
    "Afghanistan": "Afeganistão",
    "Albania": "Albânia",
    "Argentina": "Argentina",
    "Armenia": "Armênia",
    "Australia": "Austrália",
    "Austria": "Áustria",
    "Azerbaijan": "Azerbaijão",
    "Bahrain": "Bahrein",
    "Bangladesh": "Bangladesh",
    "Belarus": "Belarus",
    "Belgium": "Bélgica",
    "Belize": "Belize",
    "Bolivia": "Bolívia",
    "Bosnia and Herzegovina": "Bósnia e Herzegovina",
    "Brazil": "Brasil",
    "Bulgaria": "Bulgária",
    "Burkina Faso": "Burkina Faso",
    "Cambodia": "Cambodja",
    "Cameroon": "Camarões",
    "Canada": "Canadá",
    "Chile": "Chile",
    "China": "China",
    "Colombia": "Colômbia",
    "Congo": "Congo",
    "Costa Rica": "Costa Rica",
    "Cote D'Ivoire": "Costa do Marfim",
    "Croatia": "Croácia",
    "Cuba": "Cuba",
    "Cyprus": "Chipre",
    "Czech Republic": "República Tcheca",
    "Czechoslovakia": "Tchecoslováquia",
    "Denmark": "Dinamarca",
    "Dominican Republic": "República Dominicana",
    "East Germany": "Alemanha Oriental",
    "Ecuador": "Equador",
    "Egypt": "Egito",
    "Estonia": "Estônia",
    "Ethiopia": "Etiópia",
    "Faeroe Islands": "Ilhas Faroé",
    "Falkland Islands": "Ilhas Malvinas",
    "Fiji": "Fiji",
    "Finland": "Finlândia",
    "France": "França",
    "Georgia": "Geórgia",
    "Germany": "Alemanha",
    "Greece": "Grécia",
    "Guatemala": "Guatemala",
    "Hong Kong": "Hong Kong",
    "Hungary": "Hungria",
    "Iceland": "Islândia",
    "India": "Índia",
    "Indonesia": "Indonésia",
    "Iran": "Irã",
    "Ireland": "Irlanda",
    "Israel": "Israel",
    "Italy": "Itália",
    "Jamaica": "Jamaica",
    "Japan": "Japão",
    "Jordan": "Jordânia",
    "Kazakhstan": "Cazaquistão",
    "Kenya": "Quênia",
    "Kuwait": "Kuwait",
    "Latvia": "Letônia",
    "Lebanon": "Líbano",
    "Lithuania": "Lituânia",
    "Luxembourg": "Luxemburgo",
    "Macedonia": "Macedônia",
    "Madagascar": "Madagascar",
    "Malaysia": "Malásia",
    "Martinique": "Martinica",
    "Mauritius": "Maurício",
    "Mexico": "México",
    "Moldova": "Moldávia",
    "Montenegro": "Montenegro",
    "Netherlands": "Países Baixos",
    "New Zealand": "Nova Zelândia",
    "Nicaragua": "Nicarágua",
    "Niger": "Níger",
    "Nigeria": "Nigéria",
    "North Korea": "Coreia do Norte",
    "Northern Ireland": "Irlanda do Norte",
    "Norway": "Noruega",
    "Pakistan": "Paquistão",
    "Palestinian Territory": "Territórios Palestinos",
    "Panama": "Panamá",
    "Paraguay": "Paraguai",
    "Peru": "Peru",
    "Philippines": "Filipinas",
    "Poland": "Polônia",
    "Portugal": "Portugal",
    "Puerto Rico": "Porto Rico",
    "Qatar": "Qatar",
    "Romania": "Romênia",
    "Russia": "Rússia",
    "San Marino": "San Marino",
    "Saudi Arabia": "Arábia Saudita",
    "Serbia": "Sérvia",
    "Serbia and Montenegro": "Sérvia e Montenegro",
    "Singapore": "Singapura",
    "Slovakia": "Eslováquia",
    "Slovenia": "Eslovênia",
    "South Africa": "África do Sul",
    "South Korea": "Coreia do Sul",
    "Soviet Union": "União Soviética",
    "Spain": "Espanha",
    "Sri Lanka": "Sri Lanka",
    "Swaziland": "Suazilândia",
    "Sweden": "Suécia",
    "Switzerland": "Suíça",
    "Syrian Arab Republic": "Síria",
    "Taiwan": "Taiwan",
    "Thailand": "Tailândia",
    "Tunisia": "Tunísia",
    "Turkey": "Turquia",
    "Uganda": "Uganda",
    "Ukraine": "Ucrânia",
    "United Arab Emirates": "Emirados Árabes Unidos",
    "United Kingdom": "Reino Unido",
    "United States": "Estados Unidos",
    "United States of America": "Estados Unidos",
    "Uruguay": "Uruguai",
    "Uzbekistan": "Uzbequistão",
    "Venezuela": "Venezuela",
    "Vietnam": "Vietnã",
    "Yugoslavia": "Iugoslávia",
    "Zambia": "Zâmbia",
    "Zimbabwe": "Zimbábue",
}

DECADE_TRANSLATION = {
    "1870s": "1870",
    "1880s": "1880",
    "1890s": "1890",
    "1900s": "1900",
    "1910s": "1910",
    "1920s": "1920",
    "1930s": "1930",
    "1940s": "1940",
    "1950s": "1950",
    "1960s": "1960",
    "1970s": "1970",
    "1980s": "1980",
    "1990s": "1990",
    "2000s": "2000",
    "2010s": "2010",
    "2020s": "2020",
}


# carregamento dos dados
@st.cache_data
def get_dataset():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "animation_movies_enriched_1878_2029.csv")
    df = pl.read_csv(csv_path, null_values=[""])
    df = df.with_columns(
        pl.col("Release_Year").cast(pl.Int32, strict=False),
        pl.col("TMDB_Rating").cast(pl.Float32, strict=False),
        pl.col("Box_Office_Million_USD").cast(pl.Float32, strict=False),
    )
    return df


df = get_dataset()
max_year = df["Release_Year"].max()

# pega os gêneros únicos separando valores que vêm juntos no csv
def extract_genres_from_df(dataframe):
    genres_set = set()
    for genre_str in dataframe['Genre'].drop_nulls().to_list():
        if genre_str:
            # aceita tanto vírgula quanto barra vertical nos gêneros
            genre_str = genre_str.replace("|", ", ")
            genres = [g.strip() for g in genre_str.split(", ")]
            genres_set.update([g for g in genres if g])
    # traduz os gêneros pra português
    translated_genres = [GENRE_TRANSLATION.get(g, g) for g in sorted(list(genres_set))]
    return sorted(translated_genres)

# pega os países únicos separando valores que vêm juntos no csv
def extract_countries_from_df(dataframe):
    countries_set = set()
    for country_str in dataframe['Country_Origin'].drop_nulls().to_list():
        if country_str and country_str.strip():
            # aceita tanto vírgula quanto barra vertical nos países
            country_str = country_str.replace("|", ", ")
            countries = [c.strip() for c in country_str.split(", ")]
            countries_set.update([c for c in countries if c])
    # traduz os países pra português
    translated_countries = [COUNTRY_TRANSLATION.get(c, c) for c in sorted(list(countries_set))]
    return sorted(translated_countries)

# versões invertidas dos dicionários pra filtrar usando os nomes originais
REVERSE_GENRE_TRANSLATION = {v: k for k, v in GENRE_TRANSLATION.items()}
REVERSE_COUNTRY_TRANSLATION = {v: k for k, v in COUNTRY_TRANSLATION.items()}
REVERSE_DECADE_TRANSLATION = {v: k for k, v in DECADE_TRANSLATION.items()}

# pega as décadas válidas do dataset
def extract_decades_from_df(dataframe):
    excluded_decades = {"Unknown", "Unknown Era", "Unknown_Era", "unknown", "unknown era"}
    decades_set = set()
    for decade in dataframe['Decade'].drop_nulls().unique().to_list():
        if decade and str(decade).strip() not in excluded_decades:
            decades_set.add(decade)
    # traduz as décadas pra aparecerem mais limpas
    translated_decades = [DECADE_TRANSLATION.get(d, d) for d in sorted(list(decades_set))]
    return sorted(translated_decades)

unique_genres = extract_genres_from_df(df)
unique_countries = extract_countries_from_df(df)

period_offsets = {
    "10 Anos": 10,
    "20 Anos": 20,
    "50 Anos": 50,
    "100 Anos": 100,
}
period_options = ["10 Anos", "20 Anos", "50 Anos", "100 Anos", "Todo o Período"]


def filter_decade_options_df(_base_df, genres, countries):
    # filtra as décadas antes do select pra não mostrar opção fantasma
    filtered = _base_df
    if genres:
        genres_en = [REVERSE_GENRE_TRANSLATION.get(g, g) for g in genres]

        def has_selected_genre(genre_str):
            if not genre_str:
                return False
            genre_str = genre_str.replace("|", ", ")
            film_genres = [g.strip() for g in genre_str.split(", ")]
            return any(g in genres_en for g in film_genres)

        filtered = filtered.filter(pl.col("Genre").map_elements(has_selected_genre, return_dtype=pl.Boolean))
    if countries:
        countries_en = [REVERSE_COUNTRY_TRANSLATION.get(c, c) for c in countries]

        def has_selected_country(country_str):
            if not country_str or not country_str.strip():
                return False
            country_str = country_str.replace("|", ", ")
            film_countries = [c.strip() for c in country_str.split(", ")]
            return any(c in countries_en for c in film_countries)

        filtered = filtered.filter(pl.col("Country_Origin").map_elements(has_selected_country, return_dtype=pl.Boolean))
    return filtered

st.title(":material/bar_chart: Galeria de Filmes de Animação")
st.markdown(
    f"**Período de análise:** 1976 a {max_year}"
)

# sidebar com os filtros
with st.sidebar:
    # controle geral 
    st.title(":material/filter_alt: Filtros")
    selected_period = st.selectbox(
        "Período de Relatório",
        period_options,
        index=2,
        key="period",
        bind="query-params",
    )
    if selected_period in period_offsets:
        # recorte por período pra focar só no intervalo escolhido
        current_start = max_year - period_offsets[selected_period]
        prev_start = current_start - period_offsets[selected_period]
    else:  # todo o período
        current_start = df["Release_Year"].min()
        prev_start = None

    selected_genres = st.multiselect(
        "Gênero",
        options=unique_genres,
        default=[],
        key="genre",
        bind="query-params",
    )
    selected_countries = st.multiselect(
        "País de Origem",
        options=unique_countries,
        default=[],
        key="country",
        bind="query-params",
    )
    decade_options_df = filter_decade_options_df(
        df.filter(pl.col("Release_Year") >= current_start),
        selected_genres,
        selected_countries,
    )
    # década só aparece se tiver filme de verdade depois dos filtros
    available_decades = extract_decades_from_df(decade_options_df)
    if "decade" in st.session_state:
        # limpa uma década selecionada se ela sumir por causa de outro filtro
        current_decade_state = st.session_state["decade"]
        if isinstance(current_decade_state, str):
            current_decade_state = [current_decade_state]
        valid_decades = [decade for decade in current_decade_state if decade in available_decades]
        if valid_decades != current_decade_state:
            st.session_state["decade"] = valid_decades
    selected_decades = st.multiselect(
        "Década",
        options=available_decades,
        default=[],
        key="decade",
        bind="query-params",
    )
# filtros por categoria
def apply_categorical_filters(_base_df, genres, countries, decades):
    filtered = _base_df
    if genres:
        # volta os gêneros pro inglês se não achar tradução
        genres_en = [REVERSE_GENRE_TRANSLATION.get(g, g) for g in genres]
        # mantém filmes que tenham qualquer gênero selecionado
        def has_selected_genre(genre_str):
            if not genre_str:
                return False
            genre_str = genre_str.replace("|", ", ")
            film_genres = [g.strip() for g in genre_str.split(", ")]
            return any(g in genres_en for g in film_genres)
        
        filtered = filtered.filter(pl.col("Genre").map_elements(has_selected_genre, return_dtype=pl.Boolean))
    if countries:
        # volta os países pro inglês
        countries_en = [REVERSE_COUNTRY_TRANSLATION.get(c, c) for c in countries]
        # verifica se o filme tem pelo menos um dos países do filtro
        def has_selected_country(country_str):
            if not country_str or not country_str.strip():
                return False
            country_str = country_str.replace("|", ", ")
            film_countries = [c.strip() for c in country_str.split(", ")]
            return any(c in countries_en for c in film_countries)
        
        filtered = filtered.filter(pl.col("Country_Origin").map_elements(has_selected_country, return_dtype=pl.Boolean))
    if decades:
        # volta as décadas pro formato original se não achar a tradução também
        decades_en = [REVERSE_DECADE_TRANSLATION.get(d, d) for d in decades]
        filtered = filtered.filter(pl.col("Decade").is_in(decades_en))
    return filtered


current_df = apply_categorical_filters(
    df.filter(pl.col("Release_Year") >= current_start),
    selected_genres,
    selected_countries,
    selected_decades,
)

# ajuda a guardar seleção feita nos gráficos interativos
if "selected_treemap_genre" not in st.session_state:
    st.session_state["selected_treemap_genre"] = None
if "selected_radar_country" not in st.session_state:
    st.session_state["selected_radar_country"] = None


def has_translated_genre(genre_str, genre_en):
    if not genre_str:
        return False
    genre_str = genre_str.replace("|", ", ")
    film_genres = [g.strip() for g in genre_str.split(", ")]
    return genre_en in film_genres


def has_selected_country(country_str, country_en):
    if not country_str or not country_str.strip():
        return False
    country_str = country_str.replace("|", ", ")
    film_countries = [c.strip() for c in country_str.split(", ")]
    return country_en in film_countries


def filter_df_by_selected_genre(dataframe, selected_genre_pt):
    if not selected_genre_pt:
        return dataframe
    genre_en = REVERSE_GENRE_TRANSLATION.get(selected_genre_pt, selected_genre_pt)
    return dataframe.filter(
        pl.col("Genre").map_elements(
            lambda genre_str: has_translated_genre(genre_str, genre_en),
            return_dtype=pl.Boolean,
        )
    )


def filter_df_by_selected_country(dataframe, selected_country_pt):
    if not selected_country_pt:
        return dataframe
    country_en = REVERSE_COUNTRY_TRANSLATION.get(selected_country_pt, selected_country_pt)
    return dataframe.filter(
        pl.col("Country_Origin").map_elements(
            lambda country_str: has_selected_country(country_str, country_en),
            return_dtype=pl.Boolean,
        )
    )


def apply_lower_selections(dataframe):
    df = dataframe
    df = filter_df_by_selected_genre(df, st.session_state.get("selected_treemap_genre"))
    df = filter_df_by_selected_country(df, st.session_state.get("selected_radar_country"))
    return df

if prev_start:
    prev_df = apply_categorical_filters(
        df.filter(
            (pl.col("Release_Year") >= prev_start)
            & (pl.col("Release_Year") < current_start)
        ),
        selected_genres,
        selected_countries,
        selected_decades,
    )
else:
    prev_df = None


# primeira linha com os indicadores principais
def get_kpis(data):
    if data is None or data.is_empty():
        return pl.DataFrame(
            {
                "total_movies": [0],
                "avg_rating": [0.0],
                "total_box_office": [0.0],
                "avg_box_office": [0.0],
            }
        )
    total_movies = data.height
    avg_rating = data["TMDB_Rating"].mean()
    total_box_office = data["Box_Office_Million_USD"].sum()
    avg_box_office = data["Box_Office_Million_USD"].mean()
    return pl.DataFrame(
        {
            "total_movies": [total_movies],
            "avg_rating": [avg_rating],
            "total_box_office": [total_box_office],
            "avg_box_office": [avg_box_office],
        }
    )


current_kpis = get_kpis(current_df)
prev_kpis = get_kpis(prev_df)


def get_delta(curr, prev, is_pct=False):
    if prev is None or prev == 0:
        return None
    if is_pct:
        return f"{curr - prev:+.1f}%"
    return f"{(curr - prev) / prev * 100:+.1f}%"


# dados pequenos dos mini gráficos dentro dos cards
sparkline_df = (
    current_df.group_by("Release_Year")
    .agg(
        pl.len().alias("movies"),
        pl.col("TMDB_Rating").mean().alias("avg_rating"),
        pl.col("Box_Office_Million_USD").sum().alias("total_box_office"),
    )
    .sort("Release_Year")
    .fill_null(0)
)
if sparkline_df.is_empty():
    spark_movies = spark_rating = spark_box_office = None
else:
    spark_movies = sparkline_df["movies"].to_list()
    spark_rating = sparkline_df["avg_rating"].to_list()
    spark_box_office = sparkline_df["total_box_office"].to_list()

col1, col2, col3, col4 = st.columns(4)

with col1:
    val = current_kpis["total_movies"][0] or 0
    delta = (
        get_delta(val, prev_kpis["total_movies"][0]) if prev_kpis is not None else None
    )
    st.metric(
        "Total de Filmes",
        f"{val:,}",
        delta=delta,
        border=True,
        chart_data=spark_movies,
        chart_type="bar",
    )

with col2:
    val = current_kpis["avg_rating"][0] or 0
    delta = (
        get_delta(val, prev_kpis["avg_rating"][0])
        if prev_kpis is not None
        else None
    )
    st.metric(
        "Rating Médio",
        f"{val:.1f}",
        delta=delta,
        border=True,
        chart_data=spark_rating,
        chart_type="line",
    )

with col3:
    val = current_kpis["total_box_office"][0] or 0
    delta = (
        get_delta(val, prev_kpis["total_box_office"][0]) if prev_kpis is not None else None
    )
    st.metric(
        "Bilheteria Total (M USD)",
        f"{val:,.0f}",
        delta=delta,
        border=True,
        chart_data=spark_box_office,
        chart_type="area",
    )

with col4:
    val = current_kpis["avg_box_office"][0] or 0
    delta = (
        get_delta(val, prev_kpis["avg_box_office"][0])
        if prev_kpis is not None
        else None
    )
    st.metric(
        "Bilheteria Média (M USD)",
        f"{val:,.0f}",
        delta=delta,
        border=True,
        chart_data=None,  # esse não usa mini gráfico
        chart_type="line",
    )

# segunda linha mostrando evolução ao longo do tempo
st.subheader(":material/trending_up: Como estamos evoluindo?")
st.caption(
    "Acompanhe o número de filmes e rating médio ao longo do tempo, e identifique mudanças de momentum ano a ano."
)
row2_1, row2_2 = st.columns([3, 2], gap="small")

with row2_1:
    # agrega por ano respeitando seleções feitas nos gráficos de baixo
    trend_df = (
        apply_lower_selections(current_df)
        .group_by("Release_Year")
        .agg(
            pl.len().alias("movies"),
            pl.col("TMDB_Rating").mean().alias("avg_rating"),
        )
        .sort("Release_Year")
        .fill_null(0)
    )

    if trend_df.is_empty():
        st.info("Nenhum dado para os filtros selecionados.")
    else:
        years = trend_df["Release_Year"].to_list()

        trend_opts = {
            "title": {"text": "Tendência de Filmes e Rating", "left": "center", "top": 5},
            "toolbox": {
                "feature": {
                    "saveAsImage": {},
                    "dataView": {"readOnly": True},
                    "restore": {},
                    "magicType": {"type": ["line", "bar"]},
                }
            },
            "tooltip": {
                "trigger": "axis",
                "valueFormatter": JsCode(
                    "function(v){return Math.round(v * 10) / 10}"
                ),
            },
            "legend": {"bottom": "0"},
            "xAxis": {"type": "category", "data": years},
            "yAxis": [
                {"type": "value", "name": "Filmes"},
                {"type": "value", "name": "Rating", "position": "right"}
            ],
            "dataZoom": [
                {"type": "inside", "start": 0, "end": 100},
                {"type": "slider", "start": 0, "end": 100, "height": 20, "bottom": 30},
            ],
            "grid": {"bottom": "18%"},
            "series": [
                {
                    "name": "Filmes",
                    "type": "bar",
                    "data": trend_df["movies"].to_list(),
                },
                {
                    "name": "Rating Médio",
                    "type": "line",
                    "yAxisIndex": 1,
                    "smooth": True,
                    "data": trend_df["avg_rating"].to_list(),
                },
            ],
        }
        st_echarts(options=trend_opts, height="400px", key="trend", theme="streamlit")

with row2_2:
    # total de bilheteria por ano e categoria
    selected_treemap_genre = st.session_state.get("selected_treemap_genre")
    lower_df = apply_lower_selections(current_df)

    if selected_treemap_genre:
        exploded = (
            lower_df
            .filter(pl.col("Genre").is_not_null())
            .with_columns(
                pl.col("Country_Origin")
                .fill_null("")
                .str.replace_all(r"\|", ", ")
                .str.split(", ")
                .alias("Country_list")
            )
            .explode("Country_list")
            .with_columns(pl.col("Country_list").alias("Country_Origin"))
            .filter((pl.col("Country_Origin") != "") & pl.col("Country_Origin").is_not_null())
        )

        revenue_df = (
            exploded
            .group_by("Release_Year", "Country_Origin")
            .agg(pl.col("Box_Office_Million_USD").sum().alias("revenue"))
            .sort(["Release_Year", "Country_Origin"])
        )

        top_countries = (
            revenue_df
            .group_by("Country_Origin")
            .agg(pl.col("revenue").sum().alias("total_revenue"))
            .sort("total_revenue", descending=True)
            .head(5)
            .select("Country_Origin")
            .to_series()
            .to_list()
        )

        revenue_df = revenue_df.filter(pl.col("Country_Origin").is_in(top_countries))
        title = f"Bilheteria Anual por País — {selected_treemap_genre}"
        category_key = "Country_Origin"
        label_map = COUNTRY_TRANSLATION
    else:
        exploded = (
            lower_df
            .filter(pl.col("Genre").is_not_null())
            .with_columns(
                pl.col("Genre")
                .fill_null("")
                .str.replace_all(r"\|", ", ")
                .str.split(", ")
                .alias("Genre_list")
            )
            .explode("Genre_list")
            .with_columns(pl.col("Genre_list").alias("Genre"))
            .filter((pl.col("Genre") != "") & (pl.col("Genre") != "Animation"))
        )

        if selected_genres:
            selected_genres_en = [REVERSE_GENRE_TRANSLATION.get(g, g) for g in selected_genres]
            exploded = exploded.filter(pl.col("Genre").is_in(selected_genres_en))

        revenue_df = (
            exploded
            .group_by("Release_Year", "Genre")
            .agg(pl.col("Box_Office_Million_USD").sum().alias("revenue"))
            .sort(["Release_Year", "Genre"])
        )

        top_genres = (
            revenue_df
            .group_by("Genre")
            .agg(pl.col("revenue").sum().alias("total_revenue"))
            .sort("total_revenue", descending=True)
            .head(5)
            .select("Genre")
            .to_series()
            .to_list()
        )

        revenue_df = revenue_df.filter(pl.col("Genre").is_in(top_genres))
        title = "Bilheteria Anual por Gênero"
        category_key = "Genre"
        label_map = GENRE_TRANSLATION

    if revenue_df.is_empty():
        st.info("Sem dados suficientes para mostrar bilheteria anual.")
    else:
        years = sorted(revenue_df.select("Release_Year").unique().to_series().to_list())
        categories = sorted(revenue_df.select(category_key).unique().to_series().to_list())

        series = []
        for cat in categories:
            y_values = []
            for year in years:
                row = revenue_df.filter(
                    (pl.col("Release_Year") == year) & (pl.col(category_key) == cat)
                )
                y_values.append(round(row["revenue"][0], 2) if row.height else 0)
            series.append(
                {
                    "name": label_map.get(cat, cat),
                    "type": "bar",
                    "stack": "total",
                    "emphasis": {"focus": "series"},
                    "data": y_values,
                }
            )

        total_by_year = (
            revenue_df.group_by("Release_Year")
            .agg(pl.col("revenue").sum().alias("total_revenue"))
            .sort("Release_Year")
        )
        total_values = [
            round(total_by_year.filter(pl.col("Release_Year") == year)["total_revenue"][0], 2)
            if total_by_year.filter(pl.col("Release_Year") == year).height
            else 0
            for year in years
        ]

        series.append(
            {
                "name": "Total Geral",
                "type": "line",
                "smooth": True,
                "showSymbol": False,
                "lineStyle": {"type": "dashed", "width": 2},
                "itemStyle": {"opacity": 0},
                "showInLegend": False,
                "data": total_values,
            }
        )

        yoy_opts = {
            "title": {"text": title, "left": "center", "top": 5},
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "valueFormatter": JsCode(
                    "function(value){return '$' + value.toLocaleString() + 'M';}"
                ),
            },
            "legend": {"bottom": "0", "type": "scroll", "textStyle": {"fontSize": 10}},
            "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
            "xAxis": {"type": "category", "data": years},
            "yAxis": {
                "type": "value",
                "name": "Bilheteria (M USD)",
                "axisLabel": {"formatter": JsCode("function(value){return '$' + value.toLocaleString() + 'M';}")},
            },
            "series": series,
        }
        st_echarts(
            options=yoy_opts, height="400px", key="yoy_revenue", theme="streamlit"
        )

# terceira linha mostrando onde e o que está puxando os resultados
st.subheader(":material/explore: Onde e o quê?")
st.caption(
    "Analise o desempenho por categoria, mercado e produto para identificar onde se concentram as receitas e as margens."
)
st.caption(
    "Estes gráficos usam os filtros da barra lateral 'Filtros' e as seleções interativas dos gráficos abaixo."
)
row3_1, row3_2, row3_3 = st.columns(3)

with row3_1:
    # treemap de gênero com tamanho por bilheteria e cor por rating
    selected_treemap_genre = st.session_state.get("selected_treemap_genre")
    selected_radar_country = st.session_state.get("selected_radar_country")

    if selected_treemap_genre:
        st.markdown(
            f"""
            **Gênero selecionado:** {selected_treemap_genre}  
            """
        )
    if selected_radar_country:
        st.markdown(
            f"""
            **País selecionado:** {selected_radar_country}  
            """
        )

    if selected_treemap_genre or selected_radar_country:
        if st.button("Limpar seleções interativas", key="clear_interactive_selection"):
            st.session_state["selected_treemap_genre"] = None
            st.session_state["selected_radar_country"] = None
            selected_treemap_genre = None
            selected_radar_country = None

    exploded_genres = (
        current_df
        .with_columns(
            pl.col("Genre")
            .fill_null("")
            .str.replace_all(r"\|", ", ")
            .str.split(", ")
            .alias("Genre_list")
        )
        .explode("Genre_list")
        .with_columns(pl.col("Genre_list").alias("Genre"))
        .filter((pl.col("Genre") != "") & (pl.col("Genre") != "Animation"))
    )
    if selected_genres:
        selected_genres_en = [REVERSE_GENRE_TRANSLATION.get(g, g) for g in selected_genres]
        exploded_genres = exploded_genres.filter(pl.col("Genre").is_in(selected_genres_en))
    tree_df = (
        exploded_genres.group_by("Genre")
        .agg(
            pl.col("Box_Office_Million_USD").sum().alias("revenue"),
            pl.col("TMDB_Rating").mean().alias("margin"),
        )
        .drop_nulls()
        .with_columns(
            pl.col("Genre").map_elements(lambda x: GENRE_TRANSLATION.get(x, x), return_dtype=pl.Utf8).alias("Genre_pt")
        )
    )

    if tree_df.is_empty():
        st.info("Sem dados para o treemap.")
    else:
        tree_data = []
        for row in tree_df.to_dicts():
            tree_data.append(
                {
                    "name": row["Genre_pt"],
                    "value": [round(row["revenue"], 2), round(row["margin"], 1)],
                }
            )

        margin_min = tree_df["margin"].min()
        margin_max = tree_df["margin"].max()

        treemap_opts = {
            "backgroundColor": "#ffffff",
            "title": {"text": "Gênero (por Bilheteria)", "left": "center"},
            "tooltip": {
                "formatter": JsCode(
                    "function(p){"
                    "var v=p.value;"
                    "if(!v||v.length<2)return p.name;"
                    "return p.name+'<br/>Bilheteria: $'+v[0].toLocaleString()+'M<br/>Rating: '+v[1].toFixed(1);"
                    "}"
                )
            },
            "visualMap": {
                "type": "continuous",
                "min": round(margin_min, 1) if margin_min is not None else -10,
                "max": round(margin_max, 1) if margin_max is not None else 30,
                "inRange": {"color": ["#aed9ff", "#4e6ef2", "#7c3aed"]},
                "dimension": 1,
                "calculable": True,
                "orient": "horizontal",
                "left": "center",
                "bottom": "0%",
                "text": ["Alto Rating", "Baixo Rating"],
            },
            "series": [
                {
                    "type": "treemap",
                    "data": tree_data,
                    "visibleMin": 300,
                    "roam": False,
                    "visualDimension": 1,
                    "itemStyle": {"borderWidth": 0, "color": "#ffffff"},
                    "label": {
                        "show": True,
                        "color": "#ffffff",
                        "fontSize": 12,
                        "overflow": "truncate",
                        "ellipsis": "...",
                    },
                    "levels": [
                        {
                            "itemStyle": {
                                "borderWidth": 0,
                                "gapWidth": 3,
                                "color": "#ffffff",
                            },
                            "upperLabel": {"show": False},
                            "label": {"color": "#000"},
                        },
                        {
                            "itemStyle": {
                                "borderWidth": 0,
                                "gapWidth": 1,
                            },
                            "label": {
                                "show": True,
                                "color": "#ffffff",
                                "overflow": "truncate",
                                "ellipsis": "...",
                            },
                            "emphasis": {
                                "label": {"color": "#ffffff"},
                                "itemStyle": {"borderColor": "#333"},
                            },
                        },
                    ],
                }
            ],
        }

        treemap_events = {
            "click": "function(params){ return params.name }"
        }
        result = st_echarts(
            options=treemap_opts,
            height="450px",
            key="treemap",
            theme="streamlit",
            events=treemap_events,
        )

        if result:
            clicked_genre = result if isinstance(result, str) else result.get("name")
            if clicked_genre:
                st.session_state["selected_treemap_genre"] = clicked_genre
                selected_treemap_genre = clicked_genre

with row3_2:
    # radar com perfil dos países em escala normalizada
    selected_treemap_genre = st.session_state.get("selected_treemap_genre")
    radar_source = filter_df_by_selected_genre(current_df, selected_treemap_genre)
    radar_df = (
        radar_source.filter(
            (pl.col("Country_Origin").is_not_null())
            & (pl.col("Country_Origin") != "")
        )
        .with_columns(
            pl.col("Country_Origin")
            .str.replace_all(r"\|", ", ")
            .str.split(", ")
            .alias("Country_list")
        )
        .explode("Country_list")
        .with_columns(pl.col("Country_list").alias("Country_Origin"))
        .filter((pl.col("Country_Origin") != "") & pl.col("Country_Origin").is_not_null())
        .group_by("Country_Origin")
        .agg(
            pl.col("Box_Office_Million_USD").sum().alias("revenue"),
            pl.col("TMDB_Rating").mean().alias("rating"),
            pl.len().alias("movies"),
        )
        .drop_nulls()
        .with_columns(
            pl.col("Country_Origin").map_elements(lambda x: COUNTRY_TRANSLATION.get(x, x), return_dtype=pl.Utf8).alias("Country_pt")
        )
    )

    if radar_df.is_empty():
        if selected_treemap_genre:
            st.info(
                f"Sem dados para o gráfico radar do gênero {selected_treemap_genre}."
            )
        else:
            st.info("Sem dados para o gráfico radar.")
    else:
        metrics = ["revenue", "rating", "movies"]
        metric_labels = ["Bilheteria", "Rating", "Filmes"]

        normalized = radar_df.clone()
        for m in metrics:
            col_max = normalized[m].max()
            if col_max and col_max != 0:
                if m == "rating":
                    normalized = normalized.with_columns(
                        (pl.col(m) / 10 * 100).alias(m)
                    )
                else:
                    normalized = normalized.with_columns(
                        (pl.col(m) / col_max * 100).alias(m)
                    )

        indicator = [{"name": label, "max": 100} for label in metric_labels]

        series_data = []
        for row in normalized.to_dicts():
            series_data.append(
                {"name": row["Country_pt"], "value": [round(row[m], 1) for m in metrics]}
            )

        radar_title = "Perfis por País"
        if selected_treemap_genre:
            radar_title = f"Perfis por País — {selected_treemap_genre}"

        radar_opts = {
            "title": {"text": radar_title, "left": "center"},
            "tooltip": {"trigger": "item"},
            "legend": {
                "bottom": "0",
                "type": "scroll",
                "data": [d["name"] for d in series_data],
            },
            "radar": {
                "indicator": indicator,
                "center": ["50%", "50%"],
                "radius": "60%",
            },
            "series": [
                {"type": "radar", "data": series_data, "areaStyle": {"opacity": 0.1}}
            ],
        }
        radar_events = {"click": "function(params){ return params.name }"}
        result = st_echarts(
            options=radar_opts,
            height="450px",
            key="radar",
            theme="streamlit",
            events=radar_events,
        )
        if result:
            clicked_country = result if isinstance(result, str) else result.get("name")
            if clicked_country:
                st.session_state["selected_radar_country"] = clicked_country

with row3_3:
    # top cinco gêneros por bilheteria em barra empilhada
    exploded_top5 = (
        current_df
        .with_columns(
            pl.col("Genre")
            .fill_null("")
            .str.replace_all(r"\|", ", ")
            .str.split(", ")
            .alias("Genre_list"),
            pl.col("Country_Origin")
            .fill_null("")
            .str.replace_all(r"\|", ", ")
            .str.split(", ")
            .alias("Country_list")
        )
        .explode("Genre_list")
        .explode("Country_list")
        .with_columns(
            pl.col("Genre_list").alias("Genre"),
            pl.col("Country_list").alias("Country_Origin"),
        )
        .filter(
            (pl.col("Genre") != "")
            & (pl.col("Genre") != "Animation")
            & (pl.col("Country_Origin") != "")
        )
    )
    selected_treemap_genre = st.session_state.get("selected_treemap_genre")
    exploded_top5 = exploded_top5
    if selected_genres:
        selected_genres_en = [REVERSE_GENRE_TRANSLATION.get(g, g) for g in selected_genres]
        exploded_top5 = exploded_top5.filter(pl.col("Genre").is_in(selected_genres_en))
    if selected_treemap_genre:
        selected_genre_en = REVERSE_GENRE_TRANSLATION.get(
            selected_treemap_genre, selected_treemap_genre
        )
        exploded_top5 = exploded_top5.filter(pl.col("Genre") == selected_genre_en)

    if selected_treemap_genre:
        top5 = (
            exploded_top5.group_by("Country_Origin")
            .agg(pl.col("Box_Office_Million_USD").sum().alias("total"))
            .sort("total", descending=True)
            .head(5)
        )
        top5_names = top5["Country_Origin"].to_list()
        top5_names_pt = [COUNTRY_TRANSLATION.get(g, g) for g in top5_names]
    else:
        top5 = (
            exploded_top5.group_by("Genre")
            .agg(pl.col("Box_Office_Million_USD").sum().alias("total"))
            .sort("total", descending=True)
            .head(5)
        )
        top5_names = top5["Genre"].to_list()
        top5_names_pt = [GENRE_TRANSLATION.get(g, g) for g in top5_names]

    if not top5_names:
        if selected_treemap_genre:
            st.info(f"Sem dados para o gênero {selected_treemap_genre}.")
        else:
            st.info("Sem dados para o gráfico Top 5.")
    else:
        if selected_treemap_genre:
            stacked_df = (
                exploded_top5.group_by("Country_Origin")
                .agg(pl.col("Box_Office_Million_USD").sum().alias("sales"))
            )
            all_countries = sorted(
                [m for m in stacked_df["Country_Origin"].unique().to_list() if m is not None]
            )
            country_sales = []
            for country in all_countries:
                val = stacked_df.filter(pl.col("Country_Origin") == country)["sales"]
                country_sales.append(round(val[0], 2) if not val.is_empty() else 0)
            top5_series = [
                {
                    "name": "Bilheteria",
                    "type": "bar",
                    "emphasis": {"focus": "series"},
                    "data": country_sales[::-1],
                }
            ]
            top5_title = f"Top 5 Países — {selected_treemap_genre}"
            legend_opts = None
        else:
            stacked_df = (
                exploded_top5.filter(pl.col("Genre").is_in(top5_names))
                .group_by("Genre", "Country_Origin")
                .agg(pl.col("Box_Office_Million_USD").sum().alias("sales"))
            )
            all_markets = sorted(
                [m for m in stacked_df["Country_Origin"].unique().to_list() if m is not None]
            )
            all_markets_pt = [COUNTRY_TRANSLATION.get(m, m) for m in all_markets]
            top5_series = []
            for i, mkt in enumerate(all_markets):
                mkt_data = []
                for sc in top5_names:
                    val = stacked_df.filter(
                        (pl.col("Genre") == sc) & (pl.col("Country_Origin") == mkt)
                    )["sales"]
                    mkt_data.append(round(val[0], 2) if not val.is_empty() else 0)
                top5_series.append(
                    {
                        "name": all_markets_pt[i],
                        "type": "bar",
                        "stack": "total",
                        "emphasis": {"focus": "series"},
                        "data": mkt_data[::-1],
                    }
                )
            top5_title = "Top 5: Bilheteria por País"
            legend_opts = {"bottom": "0", "type": "scroll", "textStyle": {"fontSize": 10}}

        top5_tooltip = {"trigger": "axis", "axisPointer": {"type": "shadow"}}
        if not selected_treemap_genre:
            top5_tooltip = {
                "trigger": "axis",
                "axisPointer": {"type": "shadow"},
                "confine": True,
                "extraCssText": "max-width: 280px; white-space: normal;",
                "formatter": JsCode(
                    "function(params){"
                    "var items=params"
                    ".filter(function(p){return Number(p.value)>0;})"
                    ".sort(function(a,b){return Number(b.value)-Number(a.value);})"
                    ".slice(0,5);"
                    "if(!items.length){return params[0].axisValue+'<br/>Sem bilheteria registrada';}"
                    "var html='<strong>'+params[0].axisValue+'</strong><br/><span style=\"color:#667085\">Top 5 países</span>';"
                    "items.forEach(function(p){"
                    "html+='<br/>'+p.marker+p.seriesName+': <strong>$'+Number(p.value).toLocaleString(undefined,{maximumFractionDigits:2})+'M</strong>';"
                    "});"
                    "return html;"
                    "}"
                ),
            }

        top5_opts = {
            "title": {"text": top5_title, "left": "center"},
            "tooltip": top5_tooltip,
            "grid": {
                "left": "3%",
                "right": "4%",
                "bottom": "15%",
                "containLabel": True,
            },
            "xAxis": {"type": "value"},
            "yAxis": {"type": "category", "data": top5_names_pt[::-1]},
            "series": top5_series,
        }
        if legend_opts is not None:
            top5_opts["legend"] = legend_opts
        top5_events = {"click": "function(params){ return params.name }"}
        result = st_echarts(
            options=top5_opts,
            height="450px",
            key="top5_stacked_bar",
            theme="streamlit",
            events=top5_events,
        )
        if result:
            clicked_label = result if isinstance(result, str) else result.get("name")
            if clicked_label:
                if selected_treemap_genre:
                    st.session_state["selected_radar_country"] = clicked_label
                else:
                    st.session_state["selected_treemap_genre"] = clicked_label
                    st.session_state["selected_radar_country"] = None

# quarta linha com análise mais detalhada usando fragment
@st.fragment
def drill_down_section():
    left, right = st.columns(2)

    with left:
        # dispersão pra comparar rating bilheteria e gênero
        sc_df = (
            current_df.filter(pl.col("Genre") != "Animation")
            .group_by("Genre")
            .agg(
                pl.col("TMDB_Rating").mean().alias("avg_rating"),
                pl.col("Box_Office_Million_USD").sum().alias("revenue"),
            )
            .drop_nulls()
            .sort("Genre")
            .with_columns(
                pl.col("Genre").map_elements(lambda x: GENRE_TRANSLATION.get(x, x), return_dtype=pl.Utf8).alias("Genre_pt")
            )
        )

        if sc_df.is_empty():
            result = {"selection": {"point_indices": []}}
            scatter_data = []
            st.info("Sem dados para o gráfico de dispersão.")
        else:
            scatter_data = []
            for row in sc_df.to_dicts():
                scatter_data.append(
                    [
                        round(row["avg_rating"], 1),
                        round(row["revenue"], 0),
                        row["Genre_pt"],
                    ]
                )

            rev_max = sc_df["revenue"].max() or 1

            scatter_opts = {
                "animation": False,
                "title": {"text": "Rating vs Bilheteria por Gênero", "left": "center"},
                "tooltip": {
                    "trigger": "item",
                    "formatter": JsCode(
                        "function(p){"
                        "var v=p.value;"
                        "return v[2]+'<br/>Rating: '+v[0]+'<br/>Bilheteria: $'+v[1].toLocaleString()+'M';"
                        "}"
                    ),
                },
                "xAxis": {"name": "Rating Médio", "type": "value"},
                "yAxis": {"name": "Bilheteria Total (M USD)", "type": "value"},
                "visualMap": {
                    "show": False,
                    "dimension": 1,
                    "min": 0,
                    "max": float(rev_max),
                    "inRange": {"symbolSize": [10, 50]},
                },
                "series": [
                    {
                        "type": "scatter",
                        "data": scatter_data,
                        "itemStyle": {"opacity": 0.7},
                        "emphasis": {
                            "itemStyle": {"borderColor": "#333", "borderWidth": 2}
                        },
                    }
                ],
            }
            result = st_echarts(
                options=scatter_opts,
                height="450px",
                key="drill_scatter",
                theme="streamlit",
                on_select="rerun",
                selection_mode="points",
            )

    with right:
        indices = result["selection"].get("point_indices", [])
        if indices and scatter_data:
            clicked_name = scatter_data[indices[0]][2]
            clicked_name_en = REVERSE_GENRE_TRANSLATION.get(clicked_name, clicked_name)
            st.markdown(f"**Mostrando tendência anual para: {clicked_name}**")

            detail_df = current_df.filter(pl.col("Genre") == clicked_name_en)
            monthly = (
                detail_df.group_by("Release_Year")
                .agg(
                    pl.col("Box_Office_Million_USD").sum().alias("revenue"),
                    pl.col("TMDB_Rating").mean().alias("rating"),
                )
                .sort("Release_Year")
                .fill_null(0)
            )

            if monthly.is_empty():
                st.info("Sem dados para este gênero.")
            else:
                month_labels = monthly["Release_Year"].to_list()
                detail_opts = {
                    "title": {
                        "text": f"{clicked_name} — Tendência Anual",
                        "left": "center",
                    },
                    "tooltip": {
                        "trigger": "axis",
                        "valueFormatter": JsCode(
                            "function(v){return '$'+Math.round(v).toLocaleString()+'M'}"
                        ),
                    },
                    "legend": {"bottom": "0"},
                    "xAxis": {"type": "category", "data": month_labels},
                    "yAxis": [
                        {"type": "value", "name": "Bilheteria (M USD)"},
                        {"type": "value", "name": "Rating"},
                    ],
                    "grid": {"bottom": "15%"},
                    "series": [
                        {
                            "name": "Bilheteria",
                            "type": "bar",
                            "data": monthly["revenue"].to_list(),
                        },
                        {
                            "name": "Rating",
                            "type": "line",
                            "yAxisIndex": 1,
                            "smooth": True,
                            "data": monthly["rating"].to_list(),
                        },
                    ],
                }
                st_echarts(
                    options=detail_opts,
                    height="450px",
                    key="drill_detail",
                    theme="streamlit",
                )
        else:
            st.info(
                "Clique em uma bolha para ver a tendência anual.",
                icon=":material/touch_app:",
            )


with st.container(border=True):
    st.subheader(":material/touch_app: Análise Detalhada — Clique para Explorar")
    st.caption(
        
        "Clicar em uma bolha renderiza novamente apenas esta seção, não a página inteira."
    )
    drill_down_section()

