import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash_bootstrap_templates import ThemeSwitchAIO
from app import *

FONT_AWESOME= ['https://use.fontawesome.com/releases/v5.10.2/css/all.css']
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server


#Styles -------------------------------------------------------------------------------------------------------------------------------
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


#Lendo e manipulando o arquivo .xlsx (TROCAR PARA .CSV DEPOIS) ----------------------------------------------------------------------------
df = pd.read_excel('SSW.xlsx')
df_cru = df.copy()
df['Mes'] = df['Data de Emissao'].dt.month
df['Quantidade de Volumes'] = df['Quantidade de Volumes'].astype(int)
df['Mes'] = df['Mes'].astype(int)
df['Dia'] = df['Data de Emissao'].dt.day
df['Dia'] = df['Dia'].astype(int)
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

# Criando opções pros filtros ---------------------------------------------------------------------------------------------------------
options_month = [{'label': 'Todos', 'value': 0}]
for i, j in zip(df_cru['Mes'].unique(), df['Mes'].unique()):
    options_month.append({'label': i, 'value': j})
options_month = sorted(options_month, key=lambda x: x['value']) 

options_team = [{'label': 'Todos', 'value': 0}]
for i in df['Tipo de Baixa'].unique():
    options_team.append({'label': i, 'value': i})


#Funções para os filtros----------------------------------------------------------------------------------------------------------------
def month_filter(month):
    if month == 0:
        mask = df['Mes'].isin(df['Mes'].unique())
    else:
        mask = df['Mes'].isin([month])
    return mask

def team_filter(team):
    if team == 0:
        mask = df['Tipo de Baixa'].isin(df['Tipo de Baixa'].unique())
    else:
        mask = df['Tipo de Baixa'].isin([team])
    return mask

def convert_to_text(month):
    lista1 = ['Ano Todo', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    return lista1[month]

# Layout ------------------------------------------------------------------------------------------------------------------------------
app.layout = dbc.Container(children=[
    # Armazenamento de dataset
    # dcc.Store(id='dataset', data=df_store),

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
                            # html.I(className='fa fa-balance-scale', style={'font-size': '200%'})
                            html.I(className='fa fa-chart-line', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("SSW")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://sistema.ssw.inf.br/bin/ssw0422", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Valor do Frete | Por Tipo de Baixa')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, md=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
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
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', className='dbc', config=config_graph)
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
                            dcc.Graph(id='graph5', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id='graph7', className='dbc', config=config_graph)
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph8', className='dbc', config=config_graph)
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
    
    # Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Distribuição de Propaganda'),
                    dcc.Graph(id='graph9', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Valores de Propaganda convertidos por mês"),
                    dcc.Graph(id='graph10', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph11', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Tipo de Baixa'),
                    dbc.RadioItems(
                        id="radio-team",
                        options=options_team,
                        value=0,
                        inline=True,
                        labelCheckedClassName="text-warning",
                        inputCheckedClassName="border border-warning bg-warning",
                    ),
                    html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
    ], className='g-2 my-auto', style={'margin-top': '7px'})
#  fluid=True (ocupa todo a largura da tela), 100vh = altura do visor (se fosse vw seria largura)
], fluid=True, style={'height': '200vh'})

#Callbacks ----------------------------------------------------------------------------------------------------------------------------

#Converter para milhão
def formato_milhao(value):
    if value > 1000000:
        return f'R$ {value / 1000000:.2f}M'
    elif value > 1000:
        return f'R$ {value / 1000:.2f}K'
    else:
        return f'R$ {value:.2f}'
    
# Graph 1 and 2
@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('month-select', 'children'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph1(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_1 = df.loc[mask]

    df_1 = df_1.groupby(['Tipo de Baixa', 'Modalidade'])['Valor do Frete'].sum()
    df_1 = df_1.sort_values(ascending=False)
    df_1 = df_1.groupby('Tipo de Baixa').head(1).reset_index()

    # Crie uma coluna formatada para o DataFrame para uso nos rótulos dos gráficos
    df_1['Valor do Frete Formatado'] = df_1['Valor do Frete'].apply(formato_milhao)

    fig2 = go.Figure(go.Pie(labels=df_1['Tipo de Baixa'], values=df_1['Valor do Frete'], hole=.6))
    fig1 = go.Figure(go.Bar(x=df_1['Tipo de Baixa'], y=df_1['Valor do Frete'], textposition='auto', text=df_1['Valor do Frete Formatado']))
    fig1.update_layout(main_config, height=200, template=template)
    fig2.update_layout(main_config, height=200, template=template, showlegend=False)

    select = html.H1(convert_to_text(month))

    return fig1, fig2, select

# Graph 3
@app.callback(
    Output('graph3', 'figure'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph3(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_3 = df.loc[mask]

    mask = team_filter(team)
    df_3 = df_3.loc[mask]

    # mask = team_filter(team)
    # df_3 = df.loc[mask]

    df_3 = df_3.groupby('Dia')['Valor do Frete'].sum().reset_index()
    fig3 = go.Figure(go.Scatter(
    x=df_3['Dia'], y=df_3['Valor do Frete'], mode='lines', fill='tonexty'))
    fig3.add_annotation(text='Faturamento Médio | Por dia',
        xref="paper", yref="paper",
        font=dict(
            size=17,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
    fig3.add_annotation(text=f"Média : {round(df_3['Valor do Frete'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=16,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)

    fig3.update_layout(main_config, height=180, template=template)
    return fig3

# Graph 4
@app.callback(
    Output('graph4', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph4(team, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = team_filter(team)
    df_4 = df.loc[mask]

    df_4 = df_4.groupby('Mes')['Valor do Frete'].sum().reset_index()
    fig4 = go.Figure(go.Scatter(x=df_4['Mes'], y=df_4['Valor do Frete'], mode='lines', fill='tonexty'))

    fig4.add_annotation(text='Faturamento Médio | Por mês',
        xref="paper", yref="paper",
        font=dict(
            size=15,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
    fig4.add_annotation(text=f"Média : {round(df_4['Valor do Frete'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=16,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)

    fig4.update_layout(main_config, height=180, template=template)
    return fig4

# Indicators 1 and 2 ------ Graph 5 and 6
@app.callback(
    Output('graph5', 'figure'),
    Output('graph6', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph5(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_5 = df_6 = df.loc[mask]
    
    df_5 = df_5.groupby(['Tipo de Baixa'])['Valor do Frete'].sum()
    df_5.sort_values(ascending=False, inplace=True)
    df_5 = df_5.reset_index()
    fig5 = go.Figure()
    fig5.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span>{df_5['Tipo de Baixa'].iloc[0]} - Top Consultant</span><br><span style='font-size:70%'>Em vendas - em relação a média</span><br>"},
        value = df_5['Valor do Frete'].iloc[0],
        number = {'prefix': "R$"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_5['Valor do Frete'].mean()}
    ))

    df_6 = df_6.groupby('Unidade Fiscal')['Valor do Frete'].sum()
    df_6.sort_values(ascending=False, inplace=True)
    df_6 = df_6.reset_index()
    fig6 = go.Figure()
    fig6.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span>{df_6['Unidade Fiscal'].iloc[0]} - Top Team</span><br><span style='font-size:70%'>Em vendas - em relação a média</span><br>"},
        value = df_6['Valor do Frete'].iloc[0],
        number = {'prefix': "R$"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_6['Valor do Frete'].mean()}
    ))

    fig5.update_layout(main_config, height=200, template=template)
    fig6.update_layout(main_config, height=200, template=template)
    fig5.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig6.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    return fig5, fig6

# Graph 7
@app.callback(
    Output('graph7', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph7(toggle):
    template = template_theme1 if toggle else template_theme2

    df_7 = df.groupby(['Mês', 'Equipe'])['Valor do Frete'].sum().reset_index()
    df_7_group = df.groupby('Mês')['Valor do Frete'].sum().reset_index()
    
    fig7 = px.line(df_7, y="Valor do Frete", x="Mês", color="Equipe")
    fig7.add_trace(go.Scatter(y=df_7_group["Valor do Frete"], x=df_7_group["Mês"], mode='lines+markers', fill='tonexty', name='Total de Vendas'))

    fig7.update_layout(main_config, yaxis={'title': None}, xaxis={'title': None}, height=190, template=template)
    fig7.update_layout({"legend": {"yanchor": "top", "y":0.99, "font" : {"color":"white", 'size': 10}}})
    return fig7

# Graph 8
@app.callback(
    Output('graph8', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph8(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_8 = df.loc[mask]

    df_8 = df_8.groupby('Equipe')['Valor do Frete'].sum().reset_index()
    fig8 = go.Figure(go.Bar(
        x=df_8['Valor do Frete'],
        y=df_8['Equipe'],
        orientation='h',
        textposition='auto',
        text=df_8['Valor do Frete'],
        insidetextfont=dict(family='Times', size=12)))

    fig8.update_layout(main_config, height=360, template=template)
    return fig8

# Graph 9
@app.callback(
    Output('graph9', 'figure'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph9(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_9 = df.loc[mask]

    mask = team_filter(team)
    df_9 = df_9.loc[mask]

    df_9 = df_9.groupby('Tipo de Baixa')['Valor do Frete'].sum().reset_index()

    fig9 = go.Figure()
    fig9.add_trace(go.Pie(labels=df_9['Tipo de Baixa'], values=df_9['Valor do Frete'], hole=.7))

    fig9.update_layout(main_config, height=150, template=template, showlegend=False)
    return fig9

# Graph 10
@app.callback(
    Output('graph10', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph10(team, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = team_filter(team)
    df_10 = df.loc[mask]

    df10 = df_10.groupby(['Meio de Propaganda', 'Mês'])['Valor do Frete'].sum().reset_index()
    fig10 = px.line(df10, y="Valor do Frete", x="Mês", color="Meio de Propaganda")

    fig10.update_layout(main_config, height=200, template=template, showlegend=False)
    return fig10

# Graph 11
@app.callback(
    Output('graph11', 'figure'),
    Output('team-select', 'children'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph11(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_11 = df.loc[mask]

    mask = team_filter(team)
    df_11 = df_11.loc[mask]

    fig11 = go.Figure()
    fig11.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span style='font-size:150%'>Valor Total</span><br><span style='font-size:70%'>Em Reais</span><br>"},
        value = df_11['Valor do Frete'].sum(),
        number = {'prefix': "R$"}
    ))

    fig11.update_layout(main_config, height=300, template=template)
    select = html.H1("Todas Equipes") if team == 0 else html.H1(team)

    return fig11, select

#Rodar o Servidor ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8551)






# df1 = df.groupby('Unidade Fiscal')['Valor do Frete'].sum().reset_index()
# fig1 = go.Figure(go.Bar(
#         x=df1['Valor do Frete'],
#         y=df1['Unidade Fiscal'],
#         orientation='h',
#         textposition='auto',
#         text=df1['Valor do Frete'],
#         insidetextfont=dict(family="Times", size=12)))

# df2 = df.groupby('Mes')['Valor do Frete'].sum().reset_index()
# fig2 = go.Figure(go.Scatter(
#         x=df2['Mes'],
#         y=df2['Valor do Frete'],
#         mode='lines',
#         fill='tonexty'))