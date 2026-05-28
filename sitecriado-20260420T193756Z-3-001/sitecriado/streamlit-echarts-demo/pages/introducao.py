import streamlit as st

# telinha de boas vindas pra explicar o projeto antes dos gráficos
st.title('Introdução')

# resuminho 
st.markdown(
    'Este site apresenta uma análise de filmes de animação usando visualizações interativas. '
    'Aqui você encontra insights sobre classificações, bilheteria e outras métricas relevantes do conjunto de dados.'
)

# créditos do trabalho com aluno professor e instituição
st.markdown('**Aluno:** Alana Noemy do Nascimento')
st.markdown('**Professor:** Rômulo Maia')
st.caption('Fatec Sebrae')
