#######################
# Importando libraries
import streamlit as st
# import webbrowser
import pandas as pd
import plotly.express as px
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
# 1. Histórico indicadores
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

# 2. Satisfação Geral por Prestadora
df_isg_prestadora = (df_pesquisa[["prestadora", 'nota']]
                     [(df_pesquisa['grupo'] == 'Indicadores') &
                     (df_pesquisa['calculo'] == 'Média Índices') &
                     (df_pesquisa['indicador'] == 'Satisfação Geral') &
                     (df_pesquisa['ano'] == 2023) &
                     (df_pesquisa['prestadora'] != 'Média Prestadoras') &
                     (df_pesquisa['estado'] != 'Média Brasil')
                      ]
                     ).groupby(["prestadora"])['nota'].mean().round(2).reset_index()

# 2.1 Média Brasil por Prestadora
df_isg_media = (df_pesquisa[["prestadora", 'nota']]
                [(df_pesquisa['grupo'] == 'Indicadores') &
                 (df_pesquisa['calculo'] == 'Média Índices') &
                 (df_pesquisa['indicador'] == 'Satisfação Geral') &
                 (df_pesquisa['ano'] == 2023) &
                 (df_pesquisa['prestadora'] == 'Média Prestadoras') &
                 (df_pesquisa['estado'] == 'Média Brasil')
                 ]
                ).groupby(["prestadora"])['nota'].mean().round(2).reset_index()

# 2.2 Criando texto para a anotação no gráfico
df_isg_media['annot'] = "Média Brasil" + ' ' + df_isg_media['nota'].astype(str)

# 2.3 Por estado

df_isg_media_uf = (df_pesquisa[["estado", 'nota']]
                   [(df_pesquisa['grupo'] == 'Indicadores') &
                    (df_pesquisa['calculo'] == 'Média Índices') &
                    (df_pesquisa['indicador'] == 'Satisfação Geral') &
                    (df_pesquisa['ano'] == 2023) &
                    (df_pesquisa['prestadora'] != 'Média Prestadoras') &
                    (df_pesquisa['estado'] != 'Média Brasil')
                    ]
                   ).groupby(["estado"])['nota'].mean().round(2).reset_index()

# 3. Notas das Perguntas que compõe o Índice de Satisfação Geral e Qualidade
# 3.1 ISG
df_isg_perguntas = (df_pesquisa[["tema", 'nota']]
                    [(df_pesquisa['grupo'] == 'Indicadores') &
                     (df_pesquisa['calculo'] == 'Média Ponderada') &
                     (df_pesquisa['indicador'] == 'Satisfação Geral') &
                     (df_pesquisa['ano'] == 2023) &

                     (df_pesquisa['prestadora'] != 'Média Prestadoras') &
                     (df_pesquisa['estado'] != 'Média Brasil')
                     ]
                    ).groupby(["tema"])['nota'].mean().round(2).reset_index()

# 3.2 Perguntas qualidade
df_isg_qualidade = (df_pesquisa[["indicador", "tema", 'nota']]
                    [(df_pesquisa['grupo'] == 'Indicadores') &
                     (df_pesquisa['calculo'] == 'Média Ponderada') &
                     (df_pesquisa['indicador'] != 'Satisfação Geral') &
                     (df_pesquisa['ano'] == 2023) &

                     (df_pesquisa['prestadora'] != 'Média Prestadoras') &
                     (df_pesquisa['estado'] != 'Média Brasil')
                     ]
                    ).groupby(["indicador", "tema"])['nota'].mean().round(2).reset_index()

# 4. Perfil Sociodemográfico
# 4.1 Sexo
df_sexo = df_pesquisa[(df_pesquisa['grupo'] == 'Perfil') &
                      (df_pesquisa['calculo'] == 'Percentual') &
                      (df_pesquisa['tema'] == 'Sexo') &
                      (df_pesquisa['ano'] == 2023) &
                      (df_pesquisa['prestadora'] == 'Média Prestadoras') &
                      (df_pesquisa['estado'] == 'Média Brasil')
                      ].copy()

# 4.2 Faixa etária
df_idade = df_pesquisa[(df_pesquisa['grupo'] == 'Perfil') &
                       (df_pesquisa['calculo'] == 'Percentual') &
                       (df_pesquisa['tema'] == 'Faixa etária') &
                       (df_pesquisa['ano'] == 2023) &
                       (df_pesquisa['prestadora'] == 'Média Prestadoras') &
                       (df_pesquisa['estado'] == 'Média Brasil')
                       ].copy()

#######################
# Construção dos Gráficos

# 1. Histórico indicadores
hist = px.histogram(df_historico_ind, x="indicador", y="nota", color='ano', barmode='group',
                    labels=dict(indicador="Indicador",
                                ano="Ano", nota="Nota"),
                    color_discrete_sequence=px.colors.sequential.YlOrRd, text_auto='.3s',
                    template="plotly_dark"
                    )
hist.update_traces(textfont_size=12, textangle=0,
                   textposition="outside", cliponaxis=False)
hist.update_layout(yaxis_title="Nota")

# 2. Satisfação por operadora
oper = px.bar(df_isg_prestadora.sort_values(by='nota', ascending=False), x='nota', y='prestadora', color='prestadora', orientation='h',
              labels=dict(prestadora="Prestadora", nota="Nota"),

              color_discrete_sequence=["#fff666"],
              template="plotly_dark",  text_auto='.2s'

              )
oper.update_layout(showlegend=False)
oper.add_vline(x=df_isg_media.nota.values[0], line_width=3, annotation_text=df_isg_media.annot.values[0],
               annotation_position="top",
               line_dash="dot", line_color="green")

# 2.1 Por estado
estado = px.bar(df_isg_media_uf.sort_values(by='estado', ascending=True), x="estado", y="nota",
                labels=dict(estado="Estado", regiao="Região", nota="Nota"),
                color_discrete_sequence=["#fff666"], template="plotly_dark"
                )
estado.add_hline(y=df_isg_media.nota.values[0], line_width=3, annotation_text=df_isg_media.annot.values[0],
                 annotation_position="top right", annotation_font_size=16,
                 line_dash="dot", line_color="green")

# 3 Perguntas ISG
isg = px.bar(df_isg_perguntas.sort_values(by='tema', ascending=False), x='nota', y='tema', color='tema', orientation='h',
             labels=dict(tema="Tema", nota="Nota"),
             color_discrete_sequence=["#fff666"],
             template="plotly_dark",  text_auto='.3s'
             )
isg.update_layout(showlegend=False)

# 3.1 Perguntas qualidade (1 gráfico por pergunta, total de 5)
qual1 = px.bar(df_isg_qualidade.query('indicador == "Qualidade da Cobrança ou Recarga"'), x='nota', y='tema', color='tema', orientation='h',
               labels=dict(ind_tema="Tema", nota="Nota"),
               color_discrete_sequence=["#fff666"],
               height=300,  # altura
               title="Qualidade da Cobrança ou Recarga",
               template="plotly_dark",  text_auto='.3s'
               )
qual1.update_layout(showlegend=False)
qual1.update_yaxes(showticklabels=True, showgrid=False, title_text='')
qual1.update_xaxes(visible=False, fixedrange=True, showgrid=False)

qual2 = px.bar(df_isg_qualidade.query('indicador == "Qualidade da Informação ao Consumidor"'), x='nota', y='tema', color='tema', orientation='h',
               labels=dict(ind_tema="Tema", nota="Nota"),
               color_discrete_sequence=["#fff666"],
               height=300,  # altura
               title="Qualidade da Informação ao Consumidor",
               template="plotly_dark",  text_auto='.3s'
               )
qual2.update_layout(showlegend=False)
qual2.update_yaxes(showticklabels=True, showgrid=False, title_text='')
qual2.update_xaxes(visible=False, fixedrange=True, showgrid=False)

qual3 = px.bar(df_isg_qualidade.query('indicador == "Qualidade do Atendimento Digital"'), x='nota', y='tema', color='tema', orientation='h',
               labels=dict(ind_tema="Tema", nota="Nota"),
               color_discrete_sequence=["#fff666"],
               height=350,  # altura
               title="Qualidade do Atendimento Digital",
               template="plotly_dark",  text_auto='.3s'
               )
qual3.update_layout(showlegend=False)
qual3.update_yaxes(showticklabels=True, showgrid=False, title_text='')
qual3.update_xaxes(visible=False, fixedrange=True, showgrid=False)

qual4 = px.bar(df_isg_qualidade.query('indicador == "Qualidade do Atendimento Telefônico"'), x='nota', y='tema', color='tema', orientation='h',
               labels=dict(ind_tema="Tema", nota="Nota"),
               color_discrete_sequence=["#fff666"],
               height=350,  # altura
               title="Qualidade do Atendimento Telefônico",
               template="plotly_dark",  text_auto='.3s'
               )
qual4.update_layout(showlegend=False)
qual4.update_yaxes(showticklabels=True, showgrid=False, title_text='')
qual4.update_xaxes(visible=False, fixedrange=True, showgrid=False)

qual5 = px.bar(df_isg_qualidade.query('indicador == "Qualidade do Funcionamento"'), x='nota', y='tema', color='tema', orientation='h',
               labels=dict(ind_tema="Tema", nota="Nota"),
               color_discrete_sequence=["#fff666"],
               height=500,  # altura
               title="Qualidade do Funcionamento",
               template="plotly_dark",  text_auto='.3s'
               )
qual5.update_layout(showlegend=False)
qual5.update_yaxes(showticklabels=True, showgrid=False, title_text='')
qual5.update_xaxes(visible=False, fixedrange=True, showgrid=False)

# 4. Perfil Sociodemográfico
# 4.1 Sexo
sexo = px.pie(df_sexo, values='nota', names='alternativas',
              labels=dict(nota="Percentual", alternativas="Sexo"),
              template="plotly_dark",
              title="Sexo",
              height=350, width=350, color_discrete_sequence=px.colors.sequential.YlOrRd
              )
sexo.update_layout(showlegend=False)
sexo.update_traces(textposition='outside', textinfo='percent+label')

# 4.2 Faixa etária
idade = px.pie(df_idade, values='nota', names='alternativas',
               labels=dict(nota="Percentual", alternativas="Faixa Etária"),
               template="plotly_dark",
               title="Faixa etária",
               height=350, width=350, color_discrete_sequence=px.colors.sequential.YlOrRd
               )
idade.update_layout(showlegend=False)
idade.update_traces(textposition='outside', textinfo='percent+label')

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

with st.expander("Histórico", expanded=True):
    st.plotly_chart(hist, use_container_width=True)

st.markdown("# Índice de Satisfação Geral por Prestadora e por Estado, 2023")

with st.expander("Prestadora", expanded=True):
    st.plotly_chart(oper, use_container_width=True)

with st.expander("Estado", expanded=False):
    st.plotly_chart(estado, use_container_width=True)

st.markdown(
    "# Notas das Perguntas que compõe o Índice de Satisfação Geral e Qualidade, 2023")

with st.expander("Satisfação Geral", expanded=True):
    st.plotly_chart(isg, use_container_width=True)

with st.expander("Qualidade", expanded=False):

    col = st.columns((2.6, 2.9), gap='medium')

    with col[0]:
        st.plotly_chart(qual1, use_container_width=True)

    with col[1]:
        st.plotly_chart(qual2, use_container_width=True)

    with col[0]:
        st.plotly_chart(qual3, use_container_width=True)

    with col[1]:
        st.plotly_chart(qual4, use_container_width=True)

    col2 = st.columns((5.6, 0.6), gap='medium')
    with col2[0]:
        st.plotly_chart(qual5, use_container_width=True)

st.markdown("# Perfil Sociodemográfico dos Consumidores, 2023")

with st.expander("Perfil", expanded=True):

    col = st.columns((2.6, 2.9), gap='medium')

    with col[0]:
        st.plotly_chart(sexo, use_container_width=True)

    with col[1]:
        st.plotly_chart(idade, use_container_width=True)
