#######################
# Importando libraries
import streamlit as st
import altair as alt
import json
from urllib.request import urlopen
# import webbrowser
import pandas as pd
import numpy as np
import plotly.express as px
# from streamlit.components.v1 import html


#######################
# Configuração da página
st.set_page_config(
    page_title="Anatel - Reclamações",
    page_icon="😡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

section[data-testid="stSidebar"] {
            width: 200px;
        }            

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
# df_anatel = pd.read_csv('datasets/df_anatel.csv.bz2')

@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/gabrielmprata/Anatel_Reclamacoes/main/datasets/df_anatel.csv.bz2")


df_anatel = load_data()

# Construção dos Datasets
# 1. Histórico indicadores

df_hist = df_anatel.groupby(["ano"])['qtd'].sum().reset_index()

# Variação
df_hist['qtd_ant'] = df_hist.qtd.shift(1)
df_hist['var'] = (((df_hist['qtd']/df_hist['qtd_ant'])*100)-100).round(2)
df_hist['dif'] = (df_hist['qtd']-df_hist['qtd_ant'])
df_hist['qtd'] = (df_hist['qtd'])/1000
df_hist['dif'] = (df_hist['dif'])/1000
df_hist['color'] = np.where(df_hist['dif'] < 0, '#e8816e', '#4c60d6')

df_hist['var'] = df_hist['var'].fillna(0)
df_hist['dif'] = df_hist['dif'].fillna(0)

# 2. Historico da condição da reclamação, 2015 a 2024

df_hist_condicao = (df_anatel[["ano", "condicao", 'qtd']]
                    [(df_anatel['condicao'] != 'Reencaminhada')]
                    ).groupby(["ano", "condicao"])['qtd'].sum().reset_index()

df_hist_condicao['qtd'] = (df_hist_condicao['qtd'])/1000


# 3 Por estado e regiao
# Mapa

df_uf = (df_anatel[["uf", 'qtd']]
         [(df_anatel['ano'] == 2023)]
         ).groupby(["uf"])['qtd'].sum().reset_index()

# Carregando o arquivo Json com o mapa do Brasil
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    Brasil = json.load(response)

state_id_map = {}
for feature in Brasil["features"]:
    feature["id"] = feature["properties"]["sigla"]
    # definindo a informação do gráfico
    state_id_map[feature["properties"]["sigla"]] = feature["id"]

# 3.1 Por regiao

df_total_regiao = (df_anatel[["regiao", 'qtd']]
                   [(df_anatel['ano'] == 2023)]
                   ).groupby(["regiao"])['qtd'].sum().reset_index()


# 3.2 Perguntas qualidade


# 4. Perfil Sociodemográfico
# 4.1 Sexo


# 4.2 Faixa etária


# 4.3 Renda


# 4.4 Escolaridade


#######################
# Construção dos Gráficos

# 1. Histórico indicadores
hist = px.line(df_hist, x='ano', y='qtd',
               height=390, width=1200,  # altura x largura
               labels=dict(ano="Ano",  qtd="Reclamações"), text="qtd",
               line_shape="spline", markers=True, template="plotly_dark")
hist.update_traces(line_color='#fff666', line_width=2,
                   textposition='top center')
hist.update_yaxes(ticksuffix="K", showgrid=True)
hist.update_layout(xaxis=dict(linecolor='rgba(0,0,0,1)', tickmode='array',
                   tickvals=df_hist['ano'], ticktext=df_hist['ano']))

hist2 = px.bar(df_hist, x="ano", y="dif", title="Diferença YxY(K)", template="plotly_dark", text_auto=True,
               height=300, width=1160,  # largura
               labels=dict(ano="Ano",  qtd="Reclamações", dif='Diferença', var='Variação(%)'), hover_data=['ano', 'dif', 'var']
               )
hist2.update_traces(textangle=0, textfont_size=12, textposition='outside',
                    cliponaxis=False, marker_color=df_hist["color"])
hist2.update_yaxes(showticklabels=False, showgrid=False,
                   visible=False, fixedrange=True)
hist2.update_xaxes(showgrid=False, visible=False, fixedrange=True)
hist2.update_layout(xaxis=dict(
    tickmode='array', tickvals=df_hist['ano'], ticktext=df_hist['ano']))

# 2. Historico da condição da reclamação
cond = px.line(df_hist_condicao, x='ano', y='qtd', color='condicao',
               height=390, width=1200,
               color_discrete_sequence=["#fff666", "#a5b409"],
               # color_discrete_sequence=px.colors.sequential.YlOrRd,
               labels=dict(ano="Ano",  qtd="Reclamações", condicao='Condição'), text="qtd",
               line_shape="spline", markers=True, template="plotly_dark")
cond.update_traces(line_width=2, textposition='top center')
cond.update_layout(xaxis=dict(linecolor='rgba(0,0,0,1)', tickmode='array',
                   tickvals=df_hist_condicao['ano'], ticktext=df_hist_condicao['ano']))

# 3 Por estado e regiao
# Criando o mapa
choropleth = px.choropleth_mapbox(
    df_uf,  # database
    locations='uf',  # define os limites no mapa
    geojson=Brasil,  # Coordenadas geograficas dos estados
    color="qtd",  # define a metrica para a cor da escala
    hover_name='uf',  # informação no box do mapa
    hover_data=["uf"],
    # title="Acessos",  # titulo do mapa
    labels=dict(uf="UF", qtd="Reclamações"),
    mapbox_style="carto-darkmatter",  # define o style do mapa
    center={"lat": -14, "lon": -55},  # define os limites para plotar
    zoom=2.5,  # zoom inicial no mapa
    color_continuous_scale="YlOrRd",  # cor dos estados
    # range_color=(0, max(df_UF_flag.Acessos)),  # Intervalo da legenda
    opacity=0.5  # opacidade da cor do mapa, para aparecer o fundo
)

choropleth.update_layout(

    plot_bgcolor='rgba(0, 0, 0, 0)',
    coloraxis_showscale=False,  # Tira a legenda
    margin=dict(l=0, r=0, t=0, b=0),
    height=350
)

# 3.1 Por regiao
reg = px.pie(df_total_regiao, values='qtd', names='regiao', labels=dict(regiao="Região", qtd="Reclamações"),
             height=350, width=350, color_discrete_sequence=px.colors.sequential.YlOrRd, template="plotly_dark"
             )
reg.update_layout(showlegend=False)
reg.update_traces(textposition='outside', textinfo='percent+label')


#######################
# Dashboard Main Panel

st.markdown("# Sistema de Suporte do Atendimento aos usuários ")

st.markdown("## Histórico das Reclamações")

with st.expander("Solicitações, 2015-2024", expanded=True):
    st.plotly_chart(hist, use_container_width=True)
    st.plotly_chart(hist2, use_container_width=True)

with st.expander("Condição da reclamação, 2015-2024", expanded=True):
    st.plotly_chart(cond, use_container_width=True)

st.markdown("## Por Estado e Região")

with st.expander("Mapa do Brasil, 2023", expanded=True):
    col = st.columns((3.6, 2.3), gap='medium')

    with col[0]:
        st.plotly_chart(choropleth, use_container_width=True)

    with col[1]:
        st.plotly_chart(reg, use_container_width=True)
