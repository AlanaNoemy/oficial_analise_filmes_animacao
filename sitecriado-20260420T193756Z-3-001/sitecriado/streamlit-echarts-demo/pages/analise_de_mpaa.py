import streamlit as st
import pandas as pd
from pathlib import Path
from echarts_theme import st_echarts


DATA_FILE = Path(__file__).resolve().parents[1] / 'animation_movies_enriched_1878_2029.csv'

# carrega os dados que vão alimentar os gráficos de mpaa
df = pd.read_csv(DATA_FILE)

def render_mpaa_analysis():
    # monta a página de análise da classificação indicativa
    st.header('Análise de Classificação MPAA')
    st.markdown('Explore a distribuição de filmes por classificação MPAA e compare métricas financeiras médias por rating.')

    free_rating_label = 'Livre/Todos os públicos'
    free_ratings = {'G', 'TP', 'L', 'AL', 'ALL', '0', 'V'}
    equivalent_ratings = {
        '6': '6/6+',
        '6+': '6/6+',
        '12': '12/12+/PG12',
        '12+': '12/12+/PG12',
        'PG12': '12/12+/PG12',
        '+13': '13+/PG-13',
        'PG-13': '13+/PG-13',
        'U/A 13+': '13+/PG-13',
        '14': '14/14+',
        '14+': '14/14+',
        '15': '15/MA 15+',
        'MA 15+': '15/MA 15+',
        '18': '18/R 18+',
        'R 18+': '18/R 18+',
        'A': '18/R 18+',
    }
    rating_meanings = {
        free_rating_label: 'Livre para todos os públicos',
        'PG': 'Orientação dos pais sugerida; pode conter material leve não ideal para crianças pequenas',
        '6/6+': 'Recomendado para maiores de 6 anos',
        '12/12+/PG12': 'Recomendado para maiores de 12 anos; em alguns sistemas exige orientação dos pais',
        '13+/PG-13': 'Pode ser inadequado para menores de 13 anos; orientação dos pais recomendada',
        '14/14+': 'Recomendado para maiores de 14 anos',
        '15/MA 15+': 'Recomendado para maiores de 15 anos; em alguns sistemas exige adulto acompanhante',
        '18/R 18+': 'Restrito ou recomendado para adultos/maiores de 18 anos',
        '19': 'Restrito para maiores de 19 anos',
        'IIA': 'Não recomendado para crianças; orientação dos pais sugerida',
        'M': 'Público maduro; recomendado para adolescentes mais velhos/adultos',
        'M/3': 'Portugal: permitido para maiores de 3 anos',
        'R': 'Restrito; menores precisam de adulto ou pode indicar conteúdo adulto, conforme o país',
        'TE+7': 'Todo espectador, mas não recomendado para menores de 7 anos',
    }

    def normalize_2026_rating(rating):
        rating = str(rating).strip()
        if rating in free_ratings:
            return free_rating_label
        if rating in equivalent_ratings:
            return equivalent_ratings[rating]
        return rating
    known_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17', 'Não classificado']

    # pega quem está sem mpaa e coloca como não classificado pra não perder o dado e tals
    df['MPAA_Rating'] = (
        df['MPAA_Rating']
        .fillna('Não classificado')
        .replace('', 'Não classificado')
    )

    df_filtered = df[df['MPAA_Rating'].isin(known_ratings)].copy()

    # conta quantos filmes existem em cada classificação
    mpaa_counts = (
        df_filtered['MPAA_Rating']
        .value_counts()
        .rename_axis('rating')
        .reset_index(name='count')
        .sort_values('count', ascending=False)
    )

    mpaa_distribution = [
        {"value": int(row['count']), "name": row['rating']}
        for _, row in mpaa_counts.iterrows()
    ]

    # calcula médias de orçamento e bilheteria por rating
    chart_data = (
        df_filtered.groupby('MPAA_Rating', dropna=False)
        [['Budget_Million_USD', 'Box_Office_Million_USD']]
        .mean()
        .reset_index()
        .replace({pd.NA: 0})
    )
    chart_data['Budget_Million_USD'] = pd.to_numeric(chart_data['Budget_Million_USD'], errors='coerce').fillna(0)
    chart_data['Box_Office_Million_USD'] = pd.to_numeric(chart_data['Box_Office_Million_USD'], errors='coerce').fillna(0)

    ratings = chart_data['MPAA_Rating'].astype(str).tolist()
    avg_budget = chart_data['Budget_Million_USD'].round(2).tolist()
    avg_box_office = chart_data['Box_Office_Million_USD'].round(2).tolist()

    col1, col2 = st.columns(2)
    with col1:
        # gráfico de pizza mostrando a distribuição das classificações
        legend_selected = {item['name']: False for item in mpaa_distribution}
        pie_opts = {
            'title': {'text': 'Distribuição MPAA', 'left': 'center'},
            'tooltip': {'trigger': 'item', 'formatter': '{b}: {c} filmes ({d}%)'},
            'legend': {
                'orient': 'horizontal',
                'left': 'center',
                'bottom': '0%',
                'selected': legend_selected,
                'selectedMode': 'multiple',
            },
            'series': [
                {
                    'type': 'pie',
                    'radius': ['35%', '60%'],
                    'avoidLabelOverlap': True,
                    'label': {
                        'show': True,
                        'position': 'outside',
                        'formatter': '{b}: {d}%',
                    },
                    'labelLine': {'length': 15, 'length2': 10},
                    'data': mpaa_distribution,
                    'itemStyle': {
                        'borderColor': '#fff',
                        'borderWidth': 2,
                    },
                    'emphasis': {
                        'itemStyle': {
                            'shadowBlur': 15,
                            'shadowOffsetX': 0,
                            'shadowColor': 'rgba(0, 0, 0, 0.4)',
                        }
                    },
                }
            ],
        }
        st_echarts(options=pie_opts, height='420px', key='mpaa_pie')

        st.markdown(
            """
            **O que cada setor representa:**  
            - **G:** filmes adequados para todos os públicos.  
            - **PG:** orientação dos pais recomendada; algumas cenas podem não ser apropriadas para crianças.  
            - **PG-13:** alguns conteúdos podem ser inapropriados para menores de 13 anos.  
            - **R:** restrito; menores de 17 anos devem estar acompanhados de um adulto.  
            - **NC-17:** proibido para menores de 17 anos.  
            - **Não classificado:** filmes sem classificação MPAA disponível.
            """
        )

    with col2:
        # barras comparando orçamento médio e bilheteria média
        bar_opts = {
            'title': {'text': 'Média de Orçamento e Bilheteria por MPAA', 'left': 'center'},
            'tooltip': {'trigger': 'axis', 'axisPointer': {'type': 'shadow'}},
            'legend': {'data': ['Orçamento Médio', 'Bilheteria Média'], 'bottom': 0},
            'xAxis': {'type': 'category', 'data': ratings, 'axisLabel': {'rotate': 30, 'interval': 0}},
            'yAxis': {'type': 'value', 'name': 'Milhões USD'},
            'series': [
                {'name': 'Orçamento Médio', 'type': 'bar', 'data': avg_budget, 'itemStyle': {'color': '#5470c6'}},
                {'name': 'Bilheteria Média', 'type': 'bar', 'data': avg_box_office, 'itemStyle': {'color': '#91cc75'}},
            ],
            'grid': {'left': '10%', 'right': '10%', 'bottom': '15%'},
        }
        st_echarts(options=bar_opts, height='380px', key='mpaa_bar')

    st.markdown('### Classificação MPAA em 2026')

    mpaa_2026 = df[(df['Release_Year'] == 2026) & (df['MPAA_Rating'] != 'NR')].copy()
    mpaa_2026['Classificação'] = mpaa_2026['MPAA_Rating'].map(normalize_2026_rating)
    mpaa_2026_counts = (
        mpaa_2026
        .groupby('Classificação', as_index=False)
        .agg(
            Quantidade=('MPAA_Rating', 'size'),
            Siglas=('MPAA_Rating', lambda values: ', '.join(sorted(set(values.astype(str))))),
        )
        .sort_values('Quantidade', ascending=False)
    )
    mpaa_2026_counts['Significado'] = (
        mpaa_2026_counts['Classificação']
        .map(rating_meanings)
        .fillna('Classificação sem legenda definida')
    )
    total_2026 = mpaa_2026_counts['Quantidade'].sum() or 1
    mpaa_2026_counts['Percentual'] = (
        (mpaa_2026_counts['Quantidade'] / total_2026 * 100)
        .round(1)
        .astype(str)
        + '%'
    )

    st_echarts(
        options={
            'title': {'text': 'Distribuição MPAA em 2026', 'left': 'center'},
            'tooltip': {'trigger': 'item', 'formatter': '{b}: {c} filmes ({d}%)'},
            'legend': {'bottom': '0', 'type': 'scroll'},
            'series': [
                {
                    'type': 'pie',
                    'radius': ['35%', '60%'],
                    'data': [
                        {'value': int(row['Quantidade']), 'name': row['Classificação']}
                        for _, row in mpaa_2026_counts.iterrows()
                    ],
                }
            ],
        },
        height='420px',
        key='mpaa_pie_2026_analysis',
    )

    st.markdown(
        """
        **Legenda:**
        """
    )

    st.dataframe(
        mpaa_2026_counts[['Classificação', 'Siglas', 'Significado', 'Quantidade', 'Percentual']],
        hide_index=True,
        use_container_width=True,
    )


render_mpaa_analysis()

