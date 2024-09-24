#######################
# Importando libraries
import streamlit as st
# import webbrowser
import pandas as pd
# from streamlit.components.v1 import html

#######################
# Configuração da página
st.set_page_config(
    page_title="Anatel - Reclamações",
    page_icon="😡",
    layout="wide"
)

# alt.themes.enable("dark")


#######################
# CSS styling
st.markdown("""
<style>
            
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

#######################
# Carregando dataset
df_pesquisa = pd.read_csv('datasets/df_pesquisa.csv.bz2')

# Construção dos Datasets

df_historico_ind = (df_pesquisa[['ano', "indicador", 'nota']]
                    [(df_pesquisa['grupo'] == 'Indicadores') &
                     (df_pesquisa['calculo'] == 'Média Índices') &
                     (df_pesquisa['estado'] != 'Média Brasil') &
                     (df_pesquisa['prestadora'] != 'Média Prestadoras')
                     ]
                    ).groupby(['ano', "indicador"])['nota'].mean().round(2).reset_index()

var_isg = (df_historico_ind.nota.values[17] -
           df_historico_ind.nota.values[11]).round(2)
var_qdf = (df_historico_ind.nota.values[16] -
           df_historico_ind.nota.values[10]).round(2)
var_info = (df_historico_ind.nota.values[13] -
            df_historico_ind.nota.values[7]).round(2)
var_aten = (df_historico_ind.nota.values[15] -
            df_historico_ind.nota.values[9]).round(2)
var_dig = (df_historico_ind.nota.values[14] -
           df_historico_ind.nota.values[8]).round(2)
var_cob = (df_historico_ind.nota.values[12] -
           df_historico_ind.nota.values[6]).round(2)
#######################
# Dashboard Main Panel

st.markdown("# Notas Indicadores - Internet Fixa, 2023")

with st.expander("Notas Indicadores", expanded=True):

    col = st.columns((1.6, 1.3, 1.3), gap='medium')

    with col[0]:
        #######################
        # Quadro com o total e a variação
        st.markdown('### Satisfação Geral do cliente')
        st.metric(label="", value=str(
            (df_historico_ind.nota.values[17]).round(2)), delta=str(var_isg))

    with col[1]:
        st.markdown('### Qualidade do Funcionamento')
        st.metric(label="", value=str(
            (df_historico_ind.nota.values[16]).round(2)), delta=str(var_qdf))

    with col[2]:
        st.markdown('### Informação ao Consumidor')
        st.metric(label="", value=str(
            (df_historico_ind.nota.values[13]).round(2)), delta=str(var_info))

    col2 = st.columns((1.6, 1.3, 1.3), gap='medium')

    with col2[0]:
        st.markdown('### Atendimento Telefônico')
        st.metric(label="", value=str(
            (df_historico_ind.nota.values[15]).round(2)), delta=str(var_aten))

    with col2[1]:
        st.markdown('### Atendimento Digital')
        st.metric(label="", value=str(
            (df_historico_ind.nota.values[14]).round(2)), delta=str(var_dig))

    with col2[2]:
        st.markdown('### Cobrança')
        st.metric(label="", value=str(
            (df_historico_ind.nota.values[12]).round(2)), delta=str(var_aten))

st.markdown("# Histórico Indicadores, 2021-2023")
