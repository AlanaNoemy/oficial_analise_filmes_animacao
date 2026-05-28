import streamlit as st

# deixa a página com nome ícone e layout largo pro dashboard respirar
st.set_page_config(
    page_title="Demo do Streamlit ECharts",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

# css geral pra deixar bem divo
st.markdown(
    """
    <style>
    :root {
        --app-bg: #F5F6FA;
        --app-surface: #FFFFFF;
        --app-text: #111827;
        --app-muted: #475569;
        --app-sidebar-text: #F8FAFC;
        --app-accent: #6C5CE7;
        --app-sidebar-control: rgba(124, 92, 231, 0.88);
        --app-sidebar-control-hover: rgba(137, 111, 238, 0.98);
    }

    [data-testid="stAppViewContainer"] {
        background-color: var(--app-bg) !important;
        color: var(--app-text) !important;
    }

    [data-testid="stHeader"],
    header[data-testid="stHeader"] {
        background-color: var(--app-bg) !important;
        color: var(--app-text) !important;
    }

    [data-testid="stHeader"]::before,
    header[data-testid="stHeader"]::before {
        background: var(--app-bg) !important;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        background-color: transparent !important;
    }

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] h6,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] div,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMetric"],
    [data-testid="stMetric"] * {
        color: var(--app-text) !important;
    }

    [data-testid="stMetric"] {
        border: 1px solid #C9CED8 !important;
    }

    [data-testid="stMetricChart"],
    [data-testid="stMetricChart"] svg {
        background: var(--app-surface) !important;
    }

    [data-testid="stMetricChart"] .background,
    [data-testid="stMetricChart"] svg > rect:first-child,
    [data-testid="stMetricChart"] svg > g > rect:first-child {
        fill: var(--app-surface) !important;
    }

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: var(--app-muted) !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6C5CE7 0%, #0984E3 100%) !important;
    }

    [data-testid="stSidebar"] .css-1aumxhk {
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: transparent !important;
    }
    .css-1d391kg, .css-12oz5g7, .css-1o4ebv7 {
        background-color: var(--app-surface) !important;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08) !important;
        border-radius: 20px !important;
    }
    .stButton>button {
        border-radius: 999px !important;
    }
    .stButton>button:hover {
        background-color: #FD7E14 !important;
        color: #ffffff !important;
    }
    .css-1q8dd3e.esravye1 {background-color:#F5F6FA !important;}

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    section[aria-label="Sidebar"] a {
        color: var(--app-sidebar-text) !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] svg {
        color: var(--app-sidebar-text) !important;
        fill: var(--app-sidebar-text) !important;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: var(--app-sidebar-text) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: var(--app-sidebar-control) !important;
        border-color: transparent !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
        background: var(--app-sidebar-control-hover) !important;
        border-color: rgba(248, 250, 252, 0.22) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: var(--app-sidebar-text) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] [class*="placeholder"] {
        color: rgba(248, 250, 252, 0.82) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# menu principal onde cada page vira uma tela na sidebar
pg = st.navigation(
    {
        "Menu": [
            st.Page("pages/introducao.py", title="Introdução", icon=":material/book:"),
            st.Page(
                "pages/analise_geral.py",
                title="Analise Geral",
                icon=":material/dashboard:",
                default=True,
            ),
            st.Page("pages/analise_de_mpaa.py", title="Analise de MPAA", icon=":material/code:"),
            st.Page("pages/dashboard.py", title="Dashboard", icon=":material/menu_book:"),
        ]
    }
)
pg.run()
