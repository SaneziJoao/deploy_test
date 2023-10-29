import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash_bootstrap_templates import ThemeSwitchAIO
from app import *
import os
import re
from dash import dash_table as dt

# FONT_AWESOME= ['https://use.fontawesome.com/releases/v5.10.2/css/all.css']
app = dash.Dash(__name__)#, external_stylesheets=FONT_AWESOME)
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

#Tratando arquivo .csv
path_arquivos = 'arquivos'

df = pd.read_csv('C:/Users/106104/SSW/arquivos/CTRC_ATRASADOS_ENTREGA.csv', encoding='Windows-1250', sep=';')
df['EMISSAO'] = pd.to_datetime(df['EMISSAO'], format='%d/%m/%Y')
df_cru = df.copy()
df = df.loc[df['0'] != 9]
df['MES'] = df['EMISSAO'].dt.month
df['MES'] = df['MES'].astype(int)
df_cru = df_cru.loc[df_cru['0'] != 9]
df_cru['MES'] = df_cru['EMISSAO'].dt.month
df_cru['MES'] = df_cru['MES'].astype(int)
df['QTD'] = 1
df['DIA'] = df['EMISSAO'].dt.day
df['DIA'] = df['DIA'].astype(int)
df['KG_CALCULADO'] = df['KG_CALCULADO'].str.replace('.', '')
df['KG_CALCULADO'] = df['KG_CALCULADO'].str.replace(',', '.')
df['KG_CALCULADO'] = df['KG_CALCULADO'].astype(float)
df['VALOR_MERCADORIA'] = df['VALOR_MERCADORIA'].str.replace('.', '')
df['VALOR_MERCADORIA'] = df['VALOR_MERCADORIA'].str.replace(',', '.')
df['VALOR_MERCADORIA'] = df['VALOR_MERCADORIA'].astype(float)
df['FRETE'] = df['FRETE'].str.replace('.', '')
df['FRETE'] = df['FRETE'].str.replace(',', '.')
df['FRETE'] = df['FRETE'].astype(float)
df['DIAS_ATRASO'] = df['DIAS_ATRASO'].astype(int)


# Transforma os números dos meses em formato "MMM" para usar no filtro
df_cru.loc[ df_cru['MES'] == 1, 'MES'] = 'JAN'
df_cru.loc[ df_cru['MES'] == 2, 'MES'] = 'FEV'
df_cru.loc[ df_cru['MES'] == 3, 'MES'] = 'MAR'
df_cru.loc[ df_cru['MES'] == 4, 'MES'] = 'ABR'
df_cru.loc[ df_cru['MES'] == 5, 'MES'] = 'MAI'
df_cru.loc[ df_cru['MES'] == 6, 'MES'] = 'JUN'
df_cru.loc[ df_cru['MES'] == 7, 'MES'] = 'JUL'
df_cru.loc[ df_cru['MES'] == 8, 'MES'] = 'AGO'
df_cru.loc[ df_cru['MES'] == 9, 'MES'] = 'SET'
df_cru.loc[ df_cru['MES'] == 10, 'MES'] = 'OUT'
df_cru.loc[ df_cru['MES'] == 11, 'MES'] = 'NOV'
df_cru.loc[ df_cru['MES'] == 12, 'MES'] = 'DEZ'

def aging(dias):
    if dias <= 5:
        return 'ATÉ 5 DIAS'
    elif dias <=10:
        return 'ATÉ 10 DIAS'
    elif dias <=30:
        return 'ATÉ 30 DIAS'
    else:
        return '+30 DIAS'
    
def id_aging_atraso(texto):
    if texto == 'ATÉ 5 DIAS':
        return 1
    elif texto == 'ATÉ 10 DIAS':
        return 2
    elif texto == 'ATÉ 30 DIAS':
        return 3
    else:
        return 4
    
def tipo_ocorrencia(ocorrencia):
    return 'Tipo Ocorrência'
    
df['AGING'] = df['DIAS_ATRASO'].apply(aging)
df['ID_AGING'] = df['AGING'].apply(id_aging_atraso)
df['ID_AGING'] = df['ID_AGING'].astype(int)
df['TIPO_OCORRENCIA'] = df['DESCR_OCORRENCIA'].apply(tipo_ocorrencia)

df_dim = pd.read_csv('C:/Users/106104/SSW/arquivos/dOcorrencias.csv', encoding='UTF-8', sep=';')
df = df.merge(df_dim, left_on='COD_OCORRENCIA', right_on='CODIGO', how='left')

# # Salvar arquivo .csv em pasta, para conferir
# caminho_arquivo_saida_final = os.path.join(path_arquivos, 'df.csv')
# df.to_csv(caminho_arquivo_saida_final, index=False, encoding='Windows-1250', sep=';')
# print('Arquivo salvo')

# Criando opções pros filtros
options_month = [{'label': 'Todos', 'value': 0}]
for i, j in zip(df_cru['MES'].unique(), df['MES'].unique()):
    options_month.append({'label': i, 'value': j})
options_month = sorted(options_month, key=lambda x: x['value']) 

#Funções para os filtros----------------------------------------------------------------------------------------------------------------
def month_filter(month):
    if month == 0:
        mask = df['MES'].isin(df['MES'].unique())
    else:
        mask = df['MES'].isin([month])
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
                            html.Label('Período'),
                            dcc.Dropdown(
                                id="radio-month",
                                options=options_month,
                                value=0
                            ),
                            # dbc.RadioItems(
                            #     id="radio-month",
                            #     options=options_month,
                            #     value=0,
                            #     inline=True,
                            #     labelCheckedClassName="text-success",
                            #     inputCheckedClassName="border border-success bg-success",
                            # ),
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
                                    html.Legend('Qtd CTRCS | Por dias de atraso')
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
            ], className='g-0 my-auto', style={'margin-top': '7px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    html.Legend('Qtd CTRCS | Por Tipo de Ocorrência')
                                )
                            ),
                            dbc.Row(
                                dbc.Col([
                                    dcc.Graph(id='graph6', className='dbc', config=config_graph)
                                ])
                            )
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    html.Legend('Qtd CTRCS | Por Ocorrência')
                                )
                            ),
                            dbc.Row(
                                dbc.Col([
                                    dcc.Graph(id='graph7', className='dbc', config=config_graph)
                                ])
                            )
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(
                                dbc.Col(
                                    html.Legend('Qtd CTRCS | Por Unidade')
                                )
                            ),
                            dbc.Row(
                                dbc.Col([
                                    dt.DataTable(
                                        id='table',
                                        columns=[
                                            {'name': 'UNID_ENTREGA', 'id': 'UNID_ENTREGA'},
                                            {'name': 'QTD Total', 'id': 'QTD_TOTAL'},
                                            {'name': 'FRETE Total', 'id': 'FRETE_TOTAL'}
                                        ],
                                        style_table={'height': '400px', 'overflowY': 'auto'},
                                    )
                                    # dcc.Graph(id='graph8', className='dbc', config=config_graph)
                                ])
                            )
                        ])
                    ], style=tab_card)
                ])
            ], className='g-0 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=7)
    ], className='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, style={'height': '200vh'})


#CALLBACKS

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


    df_1 = df_1['QTD'].sum()
    fig1 = go.Figure()
    fig1.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span> Qtd CTRCS Pendentes </span>"},
        value = df_1,
        # number = {'prefix': "R$"},
    ))

    df_2 = df_2['VALOR_MERCADORIA'].sum()
    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span> Valor Mercadoria </span>"},
        value = df_2,
        number = {'prefix': "R$"},
    ))
    
    df_3 = df_3['FRETE'].sum()
    fig3 = go.Figure()
    fig3.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span> Total Frete </span>"},
        value = df_3,
        number = {'prefix': "R$"},
    ))

    df_4 = df_4['KG_CALCULADO'].sum()
    fig4 = go.Figure()
    fig4.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span> KG Calculado </span>"},
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

    df_5 = df_5.groupby('AGING')['QTD'].sum().reset_index()
    # df_5 = df_5.sort_values(by='ID_AGING', ascending=False)
    fig5 = go.Figure(
        go.Bar(
            x=df_5['AGING'],
            y=df_5['QTD'],
            textposition='auto',
            text=df_5['QTD']
        ))

    fig5.update_layout(main_config, height=180, template=template)
    return fig5

#Graph 6
@app.callback(
    Output('graph6', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph6(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_6 = df.loc[mask]

    df_6 = df_6.groupby('TIPO')['QTD'].sum().reset_index()
    df_6 = df_6.sort_values(by='QTD', ascending = False)
    fig6 = go.Figure(
        go.Bar(
            x=df_6['TIPO'],
            y=df_6['QTD'],
            textposition='auto',
            text=df_6['QTD']
        ))

    fig6.update_layout(main_config, height=180, template=template)
    return fig6

#Graph 7
@app.callback(
    Output('graph7', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph7(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_7 = df.loc[mask]

    df_7 = df_7.groupby('DESCR_OCORRENCIA')['QTD'].sum().reset_index()
    df_7 = df_7.sort_values(by='QTD', ascending=True)
    fig7 = go.Figure(
        go.Bar(
            y=df_7['DESCR_OCORRENCIA'],
            x=df_7['QTD'],
            textposition='auto',
            text=df_7['QTD'],
            orientation='h'
        ))

    fig7.update_layout(main_config, height=180, template=template)
    return fig7

#Graph 8

def calculate_aggregated_data(selected_month):
    if selected_month == 0:
        mask = df['MES'].isin(df['MES'].unique())
    else:
        mask = df['MES'] == selected_month
    filtered_df = df[mask]
    grouped_df = filtered_df.groupby('UNID_ENTREGA').agg({'QTD': 'sum', 'FRETE': 'sum'}).reset_index()
    return grouped_df

@app.callback(
    Output('table', 'data'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def update_table(month, toggle):
    template = template_theme1 if toggle else template_theme2

    def update_table(selected_month):
        grouped_df = calculate_aggregated_data(month)
        data = grouped_df.to_dict('records')
        return data


#Rodar o Servidor 
if __name__ == '__main__':
    app.run_server(debug=True, port=8552)