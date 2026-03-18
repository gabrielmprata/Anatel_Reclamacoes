# :bar_chart: Anatel - Reclamações 😡 :chart_with_upwards_trend:
# :bar_chart: Pesquisa de Satisfação e Qualidade 🙂☹️😡 :chart_with_upwards_trend:

<p align="left">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=RED&style=for-the-badge" #vitrinedev/>  

<img src="http://img.shields.io/static/v1?label=vers%C3%A3o%20do%20projeto&message=v1.2.0&color=red&style=for-the-badge&logo=github"/>
</p>

## 🖥️ Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dash-anatel-reclamacoes-qualidade.streamlit.app/)

<img src="https://github.com/user-attachments/assets/9a79bb15-556e-4942-a2cf-fc1aa3f9cc47" alt="Dashboard"  height="350">


<br>

# :radio_button: Objetivo 
Criar um simples Dashboard em **Python** e **Streamlit**, para a visualização das informações de reclamações dos usuários de banda larga fixa no Brasil.
>
E apresentar as informações da **Pesquisa de Satisfação e Qualidade** feita pela Anatel, com os usuários.
<br><br>
# Ferramentas utilizadas
<img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="40" height="40"/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg" width="40" height="40"/>   <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/plotly/plotly-original-wordmark.svg" width="40" height="40"/>  <img loading="lazy" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-original-wordmark.svg" width="40" height="40"/>


<br></br>
# Introdução

Os dados apresentados nesse estudo acadêmico, referem-se ao registro de reclamções dos usuários contra as operadoras de Banda Larga Fixa (**SCM** - Serviço de Comunicação Multimídia), coletados no Sistema de Suporte do Atendimento aos Usuários da Anatel.
>
Demonstramos também nesse estudo, a **pesquisa de satisfação e qualidade** realizada pela Anatel.


<br><br>
# **<font color=#85d338> 1. Definição do problema**
>
O mercado de banda larga fixa vem crescendo cada vez mais no Brasil, gerando uma grande concorrência entre empresas de telecomunicações.
<br><br>

# **<font color=#85d338> 2. Coleta de Dados**
>
Os dados das **Reclamações**, foram coletados do sítio da Agência Nacional de Telecomunicações.<img align="left" width="45" height="45" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Anatel_Logo.svg/180px-Anatel_Logo.svg.png">
>
Link: https://dados.gov.br/dados/conjuntos-dados/solicitacoesregistradasnaanatel
>
As informações da **Pesquisa de satisfção e qualidade**, estão no sítio de dados abertos da Anatel, no link abaixo:
>
Link: https://dados.gov.br/dados/conjuntos-dados/pesquisas-de-satisfacao-e-qualidade-percebida
<br><br>

# **<font color=#85d338> 3. Pré-processamento**
>
Esta é a etapa mais demorada e trabalhosa do projeto de ciência de dados, e estima-se que consuma pelo menos 70% do tempo total do projeto.
>
Após coletar e analisar os dados na etapa anterior, é necessário limpar, transformar e apresentar melhor os seus dados, a fim de obter, na próxima etapa, os melhores resultados possíveis nos algoritmos de machine learning ou simplesmente apresentar dados mais confiáveis para os clientes em soluções de
business intelligence.
>
Como o nosso objetivo é criar um Dashboard com **Python** e **Streamlit**, iremos minimizar ao máximo o tamanho e a granularidade dos Datasets disponibilizados, a fim de termos um ambiente mais "leve" para a leitura dos dados.
>
Principais técnicas utilizadas:
>
**Limpeza:** Consiste na verificação da consistência das informações, correção de possíveis erros de preenchimento ou eliminação de valores desconhecidos, redundantes ou não pertencentes ao domínio.
>
**Agregação:** Também pode ser considerada uma técnica de redução de dimensionalidade, pois reduz o número de linhas e colunas de um dataset.
>
### 3.1 Dataset Reclamações
>
No link da etapa anterior, é disponibilizado um arquivo compactado *consumidor_reclamacoes.zip*, com ceraga de 520 mega bytes.
>
Ao descompactar, usamos nesse projeto o arquivo, *reclamacoes_contexto.csv*, com cerca de 3,8 Gigabytes.
>
É um arquivo muito grande para manipular no Colab, sendo assim desenvolvi um código Python no VsCode, usando os recursos da minha máquina, para importar o arquivo, e gerar um arquivo compactado para poder utilizar com mais facilidade e agilidade no Google Colab.
>
Link para o arquivo .py
>
[<img loading="lazy" src="https://github.com/gabrielmprata/Anatel_Reclamacoes/blob/6c5b82301d75a3a8b5026bf703a41cb7c5080140/images/githubcodespaces-original.svg" width="40" height="40"/>](https://github.com/gabrielmprata/Anatel_Reclamacoes/blob/main/Pre_etl.py)

[![Colab Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1HcN6QvrPrgMSWPA8P6NH2x6r4OqUEvev#)
>
### 3.2 Dataset Pesquisa de Satisfação e Qualidade
>
[![Colab Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XcwVd8iIzISfIDcQupraeRMJ3vjZaIO5)
>
# **<font color=#85d338> 4. Apresentação dos resultados**
>
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dash-anatel-reclamacoes-qualidade.streamlit.app/)
