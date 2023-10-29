import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash_bootstrap_templates import ThemeSwitchAIO
from app import *
import os

FONT_AWESOME= ['https://use.fontawesome.com/releases/v5.10.2/css/all.css']
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server

#Styles 
tab_card = {'height': '100%'}

    #configuração dos gráficos
main_config = {
    'hovermode': 'x unified', #quando passamos o mouse por cima dos dados
    'legend': {'yanchor': 'top',
               'y':0.9,
               'xanchor': 'left',
               'x': 0.1,
               'title': {'text': None}, #retira os titulos
               'font': {'color':'white'}, #fonte sempre branca
               'bgcolor': 'rgba(0, 0, 0, 0.5)'}, #cor do plano de fundo, com 0.5 de opacidade
    'margin': {'l':10, 'r':10, 't':10, 'b':10} #margens
}

config_graph={'displayModeBar': False, 'showTips': False} #tira os 'botõezinhos' que ficam em cima dos gráficos

#templates para serem utilizados para mudar o tema do dashboard
template_theme1 = 'flatly'
template_theme2 = 'darkly'
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# Diretórios de entrada e saída
path_arquivos = 'arquivos'
path_arquivos_tratados = 'arquivos_tratados'

if not os.path.exists(path_arquivos_tratados):
    os.mkdir(path_arquivos_tratados)

# Listar os arquivos CSV na pasta de entrada
arquivos_csv = [f for f in os.listdir(path_arquivos) if f.endswith('.csv')]


if not arquivos_csv:
    pass
else:
# Iterar sobre os arquivos e realizar o processamento
    for arquivo in arquivos_csv:
        caminho_arquivo_entrada = os.path.join(path_arquivos, arquivo)
        caminho_arquivo_saida = os.path.join(path_arquivos_tratados, arquivo)

        # Ler o arquivo CSV original
        df = pd.read_csv(caminho_arquivo_entrada, encoding='Windows-1250', sep=';', skiprows=[0])

        # Remover a primeira linha (cabeçalho)
        df = df.iloc[1:]

        # Salvar o DataFrame tratado em um novo arquivo na pasta de saída
        df.to_csv(caminho_arquivo_saida, index=False)


        os.remove(caminho_arquivo_entrada)

arquivos_csv = [f for f in os.listdir(path_arquivos_tratados) if f.endswith('.csv')]
df = pd.DataFrame()
for arquivo in arquivos_csv:
    caminho_arquivo = os.path.join(path_arquivos_tratados, arquivo)
    dados_arquivo = pd.read_csv(caminho_arquivo, encoding = 'Windows-1250')
    df = pd.concat([df, dados_arquivo])

df = df.loc[df['1'] != 9]
df_cru = df.copy()
df_cru['Data de Emissao'] = pd.to_datetime(df_cru['Data de Emissao'], format='%d/%m/%y')
df['Data de Emissao'] = pd.to_datetime(df['Data de Emissao'], format='%d/%m/%y')
df['Quantidade de Volumes'] = df['Quantidade de Volumes'].astype(int)
df['Peso Real em Kg'] = df['Peso Real em Kg'].str.replace(' ', '')
df['Peso Real em Kg'] = df['Peso Real em Kg'].str.replace(',', '.')
df['Peso Real em Kg'] = df['Peso Real em Kg'].astype(float)
df['Valor da Mercadoria'] = df['Valor da Mercadoria'].str.replace(' ', '')
df['Valor da Mercadoria'] = df['Valor da Mercadoria'].str.replace(',', '.')
df['Valor da Mercadoria'] = df['Valor da Mercadoria'].astype(float)
df['Valor do Frete'] = df['Valor do Frete'].str.replace(' ', '')
df['Valor do Frete'] = df['Valor do Frete'].str.replace(',', '.')
df['Valor do Frete'] = df['Valor do Frete'].astype(float)
df['Valor do Frete sem ICMS'] = df['Valor do Frete sem ICMS'].str.replace(' ', '')
df['Valor do Frete sem ICMS'] = df['Valor do Frete sem ICMS'].str.replace(',', '.')
df['Valor do Frete sem ICMS'] = df['Valor do Frete sem ICMS'].astype(float)
df['Mes'] = df['Data de Emissao'].dt.month
df['Mes'] = df['Mes'].astype(int)
df['Dia'] = df['Data de Emissao'].dt.day
df['Dia'] = df['Dia'].astype(int)
df['Ano'] = df['Data de Emissao'].dt.year
df['Ano'] = df['Ano'].astype(int)
df_cru['Mes'] = df_cru['Data de Emissao'].dt.month

# Transforma os números dos meses em formato "MMM" para usar no filtro
df_cru.loc[ df_cru['Mes'] == 1, 'Mes'] = 'Jan'
df_cru.loc[ df_cru['Mes'] == 2, 'Mes'] = 'Fev'
df_cru.loc[ df_cru['Mes'] == 3, 'Mes'] = 'Mar'
df_cru.loc[ df_cru['Mes'] == 4, 'Mes'] = 'Abr'
df_cru.loc[ df_cru['Mes'] == 5, 'Mes'] = 'Mai'
df_cru.loc[ df_cru['Mes'] == 6, 'Mes'] = 'Jun'
df_cru.loc[ df_cru['Mes'] == 7, 'Mes'] = 'Jul'
df_cru.loc[ df_cru['Mes'] == 8, 'Mes'] = 'Ago'
df_cru.loc[ df_cru['Mes'] == 9, 'Mes'] = 'Set'
df_cru.loc[ df_cru['Mes'] == 10, 'Mes'] = 'Out'
df_cru.loc[ df_cru['Mes'] == 11, 'Mes'] = 'Nov'
df_cru.loc[ df_cru['Mes'] == 12, 'Mes'] = 'Dez'

# # Salvar arquivo .csv em pasta, para conferir
# caminho_arquivo_saida_final = os.path.join(path_arquivos, 'df.csv')
# df.to_csv(caminho_arquivo_saida_final, index=False, encoding='Windows-1250', sep=';')
# print('Arquivo salvo')

# Criando opções pros filtros
options_month = [{'label': 'Todos', 'value': 0}]
for i, j in zip(df_cru['Mes'].unique(), df['Mes'].unique()):
    options_month.append({'label': i, 'value': j})
options_month = sorted(options_month, key=lambda x: x['value']) 

#Funções para os filtros----------------------------------------------------------------------------------------------------------------
def month_filter(month):
    if month == 0:
        mask = df['Mes'].isin(df['Mes'].unique())
    else:
        mask = df['Mes'].isin([month])
    return mask

def convert_to_text(month):
    lista1 = ['Tudo', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    return lista1[month]


# Layout ------------------------------------------------------------------------------------------------------------------------------
app.layout = dbc.Container(children=[

    # Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([  
                            html.Legend("Dashboard 455")
                        ], sm=8),
                        dbc.Col([        
                            html.I(className='fa fa-chart-line', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Legend("SSW"),
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://sistema.ssw.inf.br/bin/ssw0422", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=3)
            ], className='g-2'),
        ], sm=12, lg=8),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Período'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=2)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    #Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    html.Legend('Valor de Frete | Por Dia')
                                )
                            ),
                            dbc.Row(
                                dbc.Col([
                                    dcc.Graph(id='graph5', className='dbc', config=config_graph)
                                ])
                            )
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5)
    ], className='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, style={'height': '200vh'})




#Callbacks

#Converter para milhão
def formato_milhao(value):
    if value > 1000000:
        return f'R$ {value / 1000000:.2f}M'
    elif value > 1000:
        return f'R$ {value / 1000:.2f}K'
    else:
        return f'R$ {value:.2f}'
    
# Graph 1, 2, 3 and 4 (cards)
@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('graph4', 'figure'),
    Output('month-select', 'children'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph1(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_1 = df_2 = df_3 = df_4 = df.loc[mask]


    df_1 = df_1['Valor do Frete sem ICMS'].sum()
    fig1 = go.Figure()
    fig1.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span> Frete Bruto </span>"},
        value = df_1,
        number = {'prefix': "R$"},
    ))

    df_2 = df_2['Valor da Mercadoria'].sum()
    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span> Valor Mercadoria </span>"},
        value = df_2,
        number = {'prefix': "R$"},
    ))
    
    df_3 = df_3['Quantidade de Volumes'].sum()
    fig3 = go.Figure()
    fig3.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span> Qtd Volumes </span>"},
        value = df_3,
        # number = {'prefix': "R$"},
    ))

    df_4 = df_4['Peso Real em Kg'].sum()
    fig4 = go.Figure()
    fig4.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span> Peso Bruto (KG) </span>"},
        value = df_4,
        # number = {'prefix': "R$"},
    ))

    fig1.update_layout(main_config, height=200, template=template)
    fig2.update_layout(main_config, height=200, template=template)
    fig3.update_layout(main_config, height=200, template=template)
    fig4.update_layout(main_config, height=200, template=template)
    fig1.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig2.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig3.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig4.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})

    select = html.H1(convert_to_text(month))

    return fig1, fig2, fig3, fig4, select

#Graph 5
@app.callback(
    Output('graph5', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph5(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_5 = df.loc[mask]

    df_5 = df_5.groupby('Dia')['Valor do Frete'].sum().reset_index()
    fig5 = go.Figure(go.Scatter(
    x=df_5['Dia'], y=df_5['Valor do Frete'], mode='lines', fill='tonexty'))

    fig5.update_layout(main_config, height=180, template=template)
    return fig5

#Rodar o Servidor 
if __name__ == '__main__':
    app.run_server(debug=True, port=8552)