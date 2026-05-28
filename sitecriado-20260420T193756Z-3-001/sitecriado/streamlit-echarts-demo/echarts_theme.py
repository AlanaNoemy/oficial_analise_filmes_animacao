from streamlit_echarts import st_echarts as _st_echarts


# paleta oficial do rolê pra deixar todos os gráficos na mesma vibe
LIGHT_ECHARTS_THEME = {
    "color": [
        "#0068C9",
        "#83C9FF",
        "#FF2B2B",
        "#FFABAB",
        "#29B09D",
        "#7DEFA1",
        "#FF8700",
        "#FFD16A",
        "#6D3FC0",
        "#D5B5FF",
    ],
    "backgroundColor": "#FFFFFF",
    "textStyle": {"color": "#31333F"},
    "title": {"textStyle": {"color": "#31333F"}},
    "legend": {"textStyle": {"color": "#31333F"}},
    "tooltip": {
        "backgroundColor": "#FFFFFF",
        "borderColor": "#D7DAE2",
        "textStyle": {"color": "#31333F"},
    },
    "categoryAxis": {
        "axisLabel": {"color": "#31333F"},
        "axisLine": {"lineStyle": {"color": "#D7DAE2"}},
        "axisTick": {"lineStyle": {"color": "#D7DAE2"}},
        "splitLine": {"lineStyle": {"color": "#E6E8F0"}},
    },
    "valueAxis": {
        "axisLabel": {"color": "#31333F"},
        "axisLine": {"lineStyle": {"color": "#D7DAE2"}},
        "axisTick": {"lineStyle": {"color": "#D7DAE2"}},
        "splitLine": {"lineStyle": {"color": "#E6E8F0"}},
    },
    "dataZoom": {"textStyle": {"color": "#31333F"}},
}


def st_echarts(*args, **kwargs):
    # atalho esperto que chama o st_echarts original já com o tema aplicado
    kwargs["theme"] = LIGHT_ECHARTS_THEME
    return _st_echarts(*args, **kwargs)
