from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

# external_stylesheets = [
#     'https://unpkg.com/terminal.css@0.7.2/dist/terminal.min.css',
# ]

app = Dash(__name__)
           
#external_stylesheets=external_stylesheets

from random import randint

N = 20

database = {
    'index': list(range(N)),
    'maiores': [randint(1, 1000) for _ in range(N)]
}

df = pd.read_excel('Vendas.xlsx')

fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
opcoes = list(df['ID Loja'].unique())
opcoes.append('Todas as lojas')

ssw = pd.read_excel('SSW.xlsx', decimal='.')
fig2 = px.bar(ssw, x='Valor do Frete', y='Modalidade', color='Modalidade'),

app.layout = html.Div(children=[
    html.H1(children='Dashboard Python'),
    html.H2(children='Quantidade de produtos | Por loja'),
    html.Div(children='''
        Obs: este gráfico, mostra a quantidade de produtos vendidos, não o faturamento
    '''),

    dcc.Dropdown(opcoes, value='Todas as lojas', id='lista_lojas'),

    dcc.Graph(
        config={'displayModeBar': False},
        id='qtd_x_prod',
        figure=fig
    ),
    
    dcc.Graph(
        config={'displayModeBar': False},
        figure={
            'data': [
                {
                    'y': database['maiores'],
                    'x': database['index'],
                    'name': 'Maiores'
                }
            ]
        }
    )
])

# call back
@app.callback(
    Output('qtd_x_prod', 'figure'),
    Input('lista_lojas', 'value')
)
def update_output(value):
    if value == 'Todas as lojas':
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja']==value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)