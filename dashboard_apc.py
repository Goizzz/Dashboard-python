# -*- coding: utf-8 -*-
"""Dashboard APC

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nR9FV5k4isILPDpoec_vYbj0rQZVW63G

##Grupo F - Netflix

##Membros

|Matrícula|Nome Completo|
|:---|:---|
|222025914|Marllon Fausto Cardoso|
|190056711|Beatriz Alves Freire|
|222021933|William Bernardo da Silva|
|222026386|Pedro Gois Marques Monteiro|
|222014877|João Vitor da Costa Monteiro|
|222006561|Arthur Rabelo Casagrande|
|222006991|Mateus Cavalcante de Sousa|
|222025950|Mateus Henrique Queiroz Magalhães Sousa|

##Objetivo

Mostrar dados econômicos e sobre produções audio-visuais da empresa Netflix.

##Base de dados

|Nome|Descrição|Colunas| Amostras|
|:---|:---|--:|--:|
|[Base 1](https://drive.google.com/file/d/15ATX-NDTQJv2GfQyhXbIhXDL_lGZm3n1/view)|Dados sobre a frequência em que certas produções apareceram no top 10 mais populares.|6|584|
|[Base 2](https://drive.google.com/file/d/1DIzGhh_hqi-IqAZr8mWcahSPL7J2FsYC/view?usp=sharing)|Dados referentes a renovação trimestral da Netflix de 2018 e 2019.|7|1160|
|[Base 3](https://drive.google.com/file/d/1V4KeRN35SYZwnk0uftth2uZvpOjo6QFx/view?usp=sharing)|Dados referentes ao preço da NFLX34 (ação da Netflix) nos últimos 5 anos.|2|1024|
|[Base 4](https://drive.google.com/file/d/1NH6BW0vuhqL0MYezftuwV_YT85wYHs2Y/view?usp=sharing)|Dados referentes às produções originais da Netflix.|3|40|

##Bibliotecas plotly e pandas
"""

!pip install -qqq jupyter_dash

pip install Dash

from jupyter_dash import JupyterDash
import plotly.express as px
import plotly.graph_objects as go
from _plotly_utils import colors
from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly.io as pio
import numpy as np
pio.templates.default = "plotly_dark"

"""### Base 1"""

url3 = 'https://drive.google.com/file/d/15ATX-NDTQJv2GfQyhXbIhXDL_lGZm3n1/view?usp=sharing'
path3 = 'https://drive.google.com/uc?export=download&id='+url3.split('/')[-2]
dataframe = pd.read_csv(path3, sep=',')
dataframe = dataframe.values.tolist()

"""### Base 2"""

url4 = 'https://drive.google.com/file/d/1DIzGhh_hqi-IqAZr8mWcahSPL7J2FsYC/view?usp=sharing'
path4 = 'https://drive.google.com/uc?export=download&id='+url4.split('/')[-2]
df4 = pd.read_csv(path4, sep=',')
df4 = df4.values.tolist()

"""### Base 3"""

urlm = 'https://drive.google.com/file/d/1V4KeRN35SYZwnk0uftth2uZvpOjo6QFx/view?usp=sharing'
pathm = 'https://drive.google.com/uc?export=download&id='+urlm.split('/')[-2]
dfm = pd.read_csv(pathm, sep='.')
dfm = dfm.values.tolist()

"""### Base 4"""

url1 = 'https://drive.google.com/file/d/1NH6BW0vuhqL0MYezftuwV_YT85wYHs2Y/view?usp=sharing'
path1 = 'https://drive.google.com/uc?export=download&id='+url1.split('/')[-2]
df2 = pd.read_csv(path1)
df2=df2.values.tolist()

"""## ##Gráficos

1. Diferentes preços da Netflix no mundo
2. Programas da Netflix no TOP 10 Global
3. Preço das ações da Netflix nos ultimos 5 anos
4. Quantidade de Programas por gênero

## Programas da Netflix no TOP 10 Global

#### O objetivo do gráfico é mapear as séries e filmes de sucesso ao redor do mundo, desde Julho de 2021 a Janeiro de 2022, comparando a quantidade de semanas que o mesmo, permaneceu no top 10 global. Com isso, conseguimos analisar o sucesso de cada série ou filme durante esse período.
"""

def sortKeyNamesAndFrequencies(x):
  return x[1]
#Declaração de constante
SHOW_TITLE_COLUMN = 3
SHOW_WEEKS_ON_TOP10_COLUMN = 6

#Atribuição de listas
names = []
frequencies = []

for i in range(len(dataframe)):
  names.append(dataframe[i][SHOW_TITLE_COLUMN])
  frequencies.append(dataframe[i][SHOW_WEEKS_ON_TOP10_COLUMN])


Repeted_Titles = []
Names_and_Frequencies = []

#Para cada nome esta associando a frequencia de vezes no TOP 10
for i in range(len(names)):
  if names[i] in Repeted_Titles:
    continue
  Repeted_Titles.append(names[i])
  FrequencyOfNamesI = 0

  for j in range(len(dataframe)):
    if (names[i] == dataframe[j][3]):
        FrequencyOfNamesI += dataframe[j][6]
  Names_and_Frequencies.append([names[i], FrequencyOfNamesI])

Names_and_Frequencies.sort(key = sortKeyNamesAndFrequencies, reverse = True)

#Criando os eixos a partir do nome e frequecia respectiva
NameAxis = []
FrequencyAxis = []
for i in range(len(Names_and_Frequencies)):
  NameAxis.append(Names_and_Frequencies[i][0])
  FrequencyAxis.append(Names_and_Frequencies[i][1])

#Criacao do grafico de barras
graphic_TOP10 = px.bar(x= NameAxis, y= FrequencyAxis, labels= {
    'x': 'Títulos dos Filmes',
    'y': 'Semanas no TOP 10',
}, title= 'Programas da Netflix no TOP 10 Global:', template='plotly_dark', color_discrete_sequence=['#e50914'])
graphic_TOP10.update_xaxes(showgrid= False, linecolor= 'white')
graphic_TOP10.update_yaxes(showgrid= False, linecolor= 'white')
graphic_TOP10.update_layout(font={'family':'Normal', 'size': 15})

"""##Renovações das inscrições da Netflix por Trimestre (2018 - 2019)

#### Objetivo: Demonstrar o aumento de renovações durante o período de 2018 e 2019.
"""

# Criando listas por continente
eua_canada = []
euro_om_africa = []
america_latina = []
asia_pacifico = []

# Guardando os valores de renovação apenas de 2018 e 2019
# OBS: Os valores ja ficam em ordem temporal
for c in df4:
    if '2018' in c[1] or '2019' in c[1]:
        if 'United States' in c[0]:
            eua_canada.append(c[2])
        elif 'Europe' in c[0]:
            euro_om_africa.append(c[2])
        elif 'Latin' in c[0]:
            america_latina.append(c[2])
        else:
            asia_pacifico.append(c[2])
# Criando a lista media e calculando a media entre os continentes por trimestre.
media = []
for c in range(8):
    media.append((eua_canada[c] + euro_om_africa[c] + america_latina[c] + asia_pacifico[c])// 4)

# Organizando uma lista para ser o eixo X, desconsiderando o ano de 2020
eixoX = []
for c in df4:
    if c[1] not in eixoX and '2020' not in c[1]:
        eixoX.append(c[1])

# Gerando o gráfico com plotly
fig4 = go.Figure(data=[
    go.Scatter(
        x= eixoX,
        y= eua_canada,
        name= 'EUA e Canadá',
        line=dict(color='blue')
    ),
    go.Scatter(
        x= eixoX,
        y = euro_om_africa,
        name= 'Europa, Oriente Médio e África',
        line=dict(color='red'),
    ),
        go.Scatter(
        x= eixoX,
        y= america_latina,
        name= 'América Latina',
        line=dict(color='green')
    ),
    go.Scatter(
        x= eixoX,
        y= asia_pacifico,
        name= 'Ásia Pacífico',
        line=dict(color='yellow')
    ),
    go.Scatter(
        x= eixoX,
        y= media,
        name= 'Média',
        line=dict(color='gray', dash= 'dash', width=1),
    )
    ])
# Personalização do gráfico
fig4.update_layout(title='Renovações das assinaturas da Netflix por trimestre (2018-2019)', title_font_color = 'white', template='plotly_dark', legend_font_color='white')
fig4.update_xaxes(color= 'white', showgrid= False, linecolor= 'white', title =  'Trimestre')
fig4.update_yaxes(color= 'white', showgrid= False, linecolor= 'white', title = 'Renovações')
fig4.show()

"""## Preço das ações da Netflix nos ultimos 5 anos

#### O gráfico referente ao preço das ações da Netflix (NFLX34), durante o período de 2 de janeiro de 2018 a 10 de janeiro de 2023, tem por objetivo compreender a situação da empresa, utilizando esse dado econômico como referência, e entender o posicionamento da corporação em relação ao contexto social e político no ano de 2022, já que, dentre vários motivos, os conflitos entre Rússia e Ucrânia contribuíram para a desvalorização no preço das ações, uma vez que a Netflix cessou o fornecimento de seus serviços à Rússia.
"""

# Manipulando as listas com os preços das ações e com as datas:
preco = []
data = []
for i in dfm:
  i[1] = i[1].replace(',','.') # Trocando a vírgula por ponto.
  i[1] = float(i[1])
  preco.append(i[1])
  data.append(i[0])

# Plotando o gráfico de barras:
figm = px.bar(x= data, y= preco, labels= {
    'x': 'Data',
    'y': 'Preço (R$)',
}, title= 'Preço da NFLX34 nos ultimos 5 anos:', template='plotly_dark', color_discrete_sequence=['#e50914'])
figm.update_xaxes(showgrid= False, linecolor= 'white')
figm.update_yaxes(showgrid= False, linecolor= 'white')
figm.update_layout(font={'family':'Normal', 'size': 15})

"""## Categorias mais adicionadas desde 2021

####O gráfico em questão tem como objetivo fazer uma análise dos gêneros de séries mais produzidas em um cenário pós pandêmico, buscando a compreensão dos genêros mais populares neste período.
"""

def sortKeyNamesAndFrequencies(x):
  return x[1]

def remove_repetidos(x):#simplificação da matriz
    l = []
    generos = []
    for i in x:
        generos.append(i[1])
        if i[1] not in l and '-' not in i[1] and '/' not in i[1] and ' ' not in i[1]:
            l.append(i[1])
    l.sort()
    return l, generos

listac, generos = remove_repetidos(df2)
listac.append('Anime')

quantidade = []
conta = 0
for i in listac:
    contador = 0
    for filme in generos:
        if i[:5] == filme[:5]:
            contador+=1
    quantidade.append([i])
    quantidade[conta].append(contador)
    conta += 1
quantidade.sort(key = sortKeyNamesAndFrequencies, reverse = True)
genders1 = []
FrequencyAxis1 = []
for i in range(len(quantidade)):
  genders1.append(quantidade[i][0])
  FrequencyAxis1.append(quantidade[i][1])

graphic_gender = px.bar(y= genders1, x= FrequencyAxis1, labels= {
    'y': 'Gêneros',
    'x': 'Quantidade de Filmes',
}, title= 'Categorias mais adicionadas desde 2021:', template='plotly_dark', color_discrete_sequence=['#e50914'])
graphic_gender.update_xaxes(showgrid= False, linecolor= 'white')
graphic_gender.update_yaxes(showgrid= False, linecolor= 'white')
graphic_gender.update_layout(font={'family':'Normal', 'size': 15})

"""##Dashboard:"""

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

# Configuração para remover display dos gráficos
config_graph={'displayModeBar': False, 'showTips': False}

# Lista para gerar os componentes
anos = ['2018', '2019', '2020', '2021', '2022', 'Todos os períodos']

num_de_vzs_no_semanal=['Top 10 dos que mais aparecem','Top 20 dos que mais aparecem','Top 30 dos que mais aparecem'
,'Top 40 dos que mais aparecem','Top 50 dos que mais aparecem','Gráfico todo']

# Criando site
app.layout = html.Div([

    # Criando um conjunto de abas/tabs
    dcc.Tabs([

    # Gráfico da Beatriz
    dcc.Tab(label='TOP 10 Global', children=[
    html.H2('Programas da Netflix no TOP 10 Global', style={'margin-top': '25px', 'color': '#E6020D', 'font-family': 'Bebas Neue',
                                                            'font-weight': 'bold', 'margin-left': '10px'}),
    html.P('O objetivo do gráfico é mapear as séries e filmes de sucesso ao redor do mundo, desde Julho de 2021 a Janeiro de 2022, comparando a quantidade de semanas que o mesmo, permaneceu no top 10 global. Com isso, conseguimos analisar o sucesso de cada série ou filme durante esse período.',
           style={'margin-top': '25px', 'color': 'white', 'font-family': 'Bebas Neue', 'font-weight': 'bold', 'margin-left': '10px'}),
    html.Br(),
    dcc.Dropdown(num_de_vzs_no_semanal, value = 'Gráfico todo', id='grafico_top_10', style={'background-color': 'black', 'color': 'red',
                                                                                            'border-color': 'red', 'border-width': '2px',
                                                                                            'font-color': 'black'}),
    html.Br(),
    dcc.Graph(
        id='grafico_inteiro',
        figure=graphic_TOP10, config=config_graph),

    html.Br(),
      ]),

    # Gráfico Will
    dcc.Tab(label='Renovações das inscrições', children=[
    html.H2('Renovações das inscrições da Netflix por Trimestre (2018 - 2019)', style={'margin-top': '50px', 'color': '#E6020D', 'font-family': 'Bebas Neue',
                                                                                       'font-weight': 'bold', 'margin-left': '10px'}),
    html.P('O objetivo do gráfico é demonstrar o aumento de renovações durante o período de 2018 e 2019.',
           style={'margin-top': '25px', 'color': 'white', 'font-family': 'Bebas Neue', 'font-weight': 'bold', 'margin-left': '10px'}),
    html.Br(),

    dcc.RangeSlider(
    min=0, max=7, step=1, marks={
        0: 'Q1 - 2018',
        1: 'Q2 - 2018',
        2: 'Q3 - 2018',
        3: 'Q4 - 2018',
        4: 'Q1 - 2019',
        5: 'Q2 - 2019',
        6: 'Q3 - 2019',
        7: 'Q4 - 2019'
    }, value=[0, 7], id='buttonwill'),

    html.Br(),

    dcc.Graph(id='figwill', figure=fig4, config=config_graph),]),

    # Gráfico Marllon
    dcc.Tab(label='Preço da NFLX34', children=[

    html.Br(),
    html.H2('Preço da NFLX34 nos últimos 5 anos', style={'margin-top': '25px', 'color': '#E6020D', 'font-family': 'Bebas Neue', 'font-weight': 'bold'}),
    html.P('O gráfico referente ao preço das ações da Netflix (NFLX34), durante o período de 2 de janeiro de 2018 a 10 de janeiro de 2023, tem por objetivo compreender a situação da empresa, utilizando esse dado econômico como referência, e entender o posicionamento da corporação em relação ao contexto social e político no ano de 2022, já que, dentre vários motivos, os conflitos entre Rússia e Ucrânia contribuíram para a desvalorização no preço das ações, uma vez que a Netflix cessou o fornecimento de seus serviços à Rússia.',
           style={'margin-top': '25px', 'color': 'rgb(255, 255, 255)', 'font-family': 'Bebas Neue', 'font-weight': 'bold'}),

    html.Br(),
    dcc.Dropdown(anos, value = 'Todos os períodos', id='grafico_acoes', style={'background-color': 'black', 'color': 'red',
                                                                                'border-color': 'red', 'border-width': '2px', 'font-color': 'black'}),
    html.Br(),
    dcc.Graph(
        id= 'graficom',
        figure=figm, config=config_graph),

    ]),

    # Gráfico Cavati
    dcc.Tab(label='Gêneros mais adicionados', children=[

    html.Br(),

    html.H2('Gêneros mais adicionados desde 2021', style={'margin-top': '25px', 'color': '#E6020D', 'font-family': 'Bebas Neue', 'font-weight': 'bold'}),

    html.P('O gráfico em questão tem como objetivo fazer uma análise dos gêneros de séries mais produzidas em um cenário pós pandêmico, buscando a compreensão dos genêros mais populares neste período.',
           style={'margin-top': '25px', 'color': 'white', 'font-family': 'Bebas Neue', 'font-weight': 'bold', 'margin-bottom': '15px'}),
    dcc.Slider(5, 20, 5, value = 15, id = 'cavaslider'),

    dcc.Graph(id='cavasgraph', figure=graphic_gender, config = config_graph)
    ]),

], style={'margin-top': '140px', 'border': 'solid', 'border-color': '#E6020D', 'font-weight': 'bold', 'font-size': '20px', 'height': '65px'}),

],style={'background-color': 'black', 'background-image': 'url("https://docs.google.com/uc?id=1nFI-b84b6qYoCDMBrF8FT8NjUE_9owKx")',
          'background-repeat': 'no-repeat', 'background-position': 'top center', 'position': 'top left', 'margin-top': '-1.3vh',
          'margin-left': '-0.6vw', 'margin-right': '-0.7vw'})


# Callback componente do cavati
@app.callback(
    Output('cavasgraph', 'figure'),
    Input('cavaslider', 'value'))


def update_output(value):

    graphic_gender = px.bar(y= genders1[:value], x= FrequencyAxis1[:value], labels= {
        'y': 'Gêneros',
        'x': 'Quantidade de Filmes',
    }, title= 'Categorias mais adicionadas desde 2021:', template='plotly_dark', color_discrete_sequence=['#e50914'])
    graphic_gender.update_xaxes(showgrid= False, linecolor= 'white')
    graphic_gender.update_yaxes(showgrid= False, linecolor= 'white')
    graphic_gender.update_layout(font={'family':'Normal', 'size': 15})
    graphic_TOP10.update_traces(textposition='inside')
    return graphic_gender


# Callback componente da bea
@app.callback(
    Output('grafico_inteiro', 'figure'),
    Input('grafico_top_10', 'value'))

def update_output(value):
    if value == 'Top 10 dos que mais aparecem':
        bia_indice = 10
    elif value == 'Top 20 dos que mais aparecem':
        bia_indice = 20
    elif value == 'Top 30 dos que mais aparecem':
        bia_indice = 30
    elif value == 'Top 40 dos que mais aparecem':
        bia_indice = 40
    elif value == 'Top 50 dos que mais aparecem':
        bia_indice = 50
    else:
        bia_indice = 401

    graphic_TOP10 = px.bar(x= NameAxis[:bia_indice], y= FrequencyAxis[:bia_indice], labels= {
        'x': 'Títulos dos Filmes',
        'y': 'Semanas no TOP 10',
    }, title= 'Programas da Netflix no TOP 10 Global:', template='plotly_dark', color_discrete_sequence=['#e50914'])
    graphic_TOP10.update_xaxes(showgrid= False, linecolor= 'white')
    graphic_TOP10.update_yaxes(showgrid= False, linecolor= 'white')
    graphic_TOP10.update_layout(font={'family':'Normal', 'size': 15})
    graphic_TOP10.update_traces(textposition='inside')
    return graphic_TOP10


# Callback componente Will
@app.callback(
    Output('figwill', 'figure'),
    Input('buttonwill', 'value'))

def willgraph(value):
    fig4 = go.Figure(data=[
    go.Scatter(
        x= eixoX[value[0]:value[1]+1],
        y= eua_canada[value[0]:value[1]+1],
        name= 'EUA e Canadá',
        line=dict(color='blue')
    ),
    go.Scatter(
        x= eixoX[value[0]:value[1]+1],
        y = euro_om_africa[value[0]:value[1]+1],
        name= 'Europa, Oriente Médio e África',
        line=dict(color='red'),
    ),
        go.Scatter(
        x= eixoX[value[0]:value[1]+1],
        y= america_latina[value[0]:value[1]+1],
        name= 'América Latina',
        line=dict(color='green')
    ),
    go.Scatter(
        x= eixoX[value[0]:value[1]+1],
        y= asia_pacifico[value[0]:value[1]+1],
        name= 'Ásia Pacífico',
        line=dict(color='yellow')
    ),
    go.Scatter(
        x= eixoX[value[0]:value[1]+1],
        y= media[value[0]:value[1]+1],
        name= 'Média',
        line=dict(color='gray', dash= 'dash', width=1),
    )
    ])

    fig4.update_layout(title='Renovações das assinaturas da Netflix por trimestre (2018-2019)', title_font_color = 'white', template='plotly_dark', legend_font_color='white')
    fig4.update_xaxes(color= 'white', showgrid= False, linecolor= 'white', title =  'Trimestre')
    fig4.update_yaxes(color= 'white', showgrid= False, linecolor= 'white', title = 'Renovações')
    return fig4

# Callback componente do Marllon
@app.callback(
    Output('graficom', 'figure'),
    Input('grafico_acoes', 'value'))

def marllon_graphic(value):
  precoX = []
  dataX =[]
  anox = value[-1]
  preco_indice = 0
  if value == 'Todos os períodos':
    dataX = data[:]
    precoX = preco[:]
  else:
    for i in range(len(data)):
      if anox == str(data[i][-1]):
        dataX.append(data[i])
        precoX.append(preco[i])
  figm = px.bar(x= dataX, y= precoX, labels= {
          'x': 'Data',
          'y': 'Preço da Ação (R$)',
  }, title= 'Preço da NFLX34', template='plotly_dark', color_discrete_sequence=['#e50914'])
  figm.update_xaxes(showgrid= False, linecolor= 'white')
  figm.update_yaxes(showgrid= False, linecolor= 'white')
  figm.update_layout(font={'family':'Normal', 'size': 15})
  figm.update_traces(textposition='inside')
  return figm


if __name__ == '__main__':
    app.run_server(mode = 'external')