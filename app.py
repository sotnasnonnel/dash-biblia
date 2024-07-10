from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Inicializa a aplicação Dash
app = Dash(__name__, suppress_callback_exceptions=True)

# Função para carregar dados
def load_data():
    return pd.read_excel('milagres_biblia_simplificado.xlsx')

data = load_data()

# Layout da aplicação com estilos e scripts
app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
    ),
    html.Div(className='header', children='Análise dos Milagres da Bíblia'),
    dcc.Tabs(id='tabs', value='main', children=[
        dcc.Tab(label='Página Principal', value='main'),
        dcc.Tab(label='Tabela Completa', value='table'),
    ]),
    html.Div(id='tabs-content', className='tab-content'),
    html.Div(className='footer', children='by: Lennon')
])

# Callback para atualizar o conteúdo da aba
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'main':
        return render_main_page()
    elif tab == 'table':
        return render_table_page()

# Função para renderizar a página principal com gráficos
def render_main_page():
    return html.Div(className='content', children=[
        html.H1("Análise dos Milagres da Bíblia"),
        html.Div(className='filters', children=[
            html.Div([
                dcc.Dropdown(
                    id='livro-filter',
                    options=[{'label': i, 'value': i} for i in data['Livro'].unique()],
                    multi=True,
                    placeholder='Filtrar por Livro'
                )
            ]),
            html.Div([
                dcc.Dropdown(
                    id='autor-filter',
                    options=[{'label': i, 'value': i} for i in data['Autor do Milagre'].unique()],
                    multi=True,
                    placeholder='Filtrar por Autor'
                )
            ]),
            html.Div([
                dcc.Dropdown(
                    id='tipo-filter',
                    options=[{'label': i, 'value': i} for i in data['Classificação Simplificada'].unique()],
                    multi=True,
                    placeholder='Filtrar por Tipo de Milagre'
                )
            ])
        ]),
        dcc.Graph(id='graph-livro'),
        dcc.Graph(id='graph-autor'),
        dcc.Graph(id='graph-tipo')
    ])

# Função para renderizar a página de tabela completa
def render_table_page():
    return html.Div(className='content', children=[
        html.H1("Tabela Completa dos Milagres da Bíblia"),
        html.Div([
            dcc.Dropdown(
                id='colunas-filter',
                options=[{'label': col, 'value': col} for col in data.columns],
                multi=True,
                value=data.columns.tolist(),
                placeholder='Selecionar Colunas'
            )
        ]),
        html.Div(className='data-table', children=[
            dash_table.DataTable(
                id='data-table',
                columns=[{'name': col, 'id': col} for col in data.columns],
                data=data.to_dict('records'),
                filter_action='native',
                sort_action='native',
                page_size=10
            )
        ])
    ])

# Callbacks para atualizar os gráficos
@app.callback(
    [Output('graph-livro', 'figure'),
     Output('graph-autor', 'figure'),
     Output('graph-tipo', 'figure')],
    [Input('livro-filter', 'value'),
     Input('autor-filter', 'value'),
     Input('tipo-filter', 'value')]
)
def update_charts(livro, autor, tipo):
    filtered_data = data.copy()
    if livro:
        filtered_data = filtered_data[filtered_data['Livro'].isin(livro)]
    if autor:
        filtered_data = filtered_data[filtered_data['Autor do Milagre'].isin(autor)]
    if tipo:
        filtered_data = filtered_data[filtered_data['Classificação Simplificada'].isin(tipo)]

    # Gráfico: Distribuição dos Milagres por Livro
    milagres_por_livro = filtered_data['Livro'].value_counts().reset_index()
    milagres_por_livro.columns = ['Livro', 'count']
    fig1 = px.bar(milagres_por_livro, x='Livro', y='count', title='Distribuição dos Milagres por Livro da Bíblia',
                  labels={'Livro': 'Livro', 'count': 'Número de Milagres'})

    # Gráfico: Distribuição dos Milagres por Autor
    milagres_por_autor = filtered_data['Autor do Milagre'].value_counts().reset_index()
    milagres_por_autor.columns = ['Autor', 'count']
    fig2 = px.pie(milagres_por_autor, values='count', names='Autor', title='Distribuição dos Milagres por Autor')

    # Gráfico: Tipos de Milagres Mais Frequentes
    tipos_de_milagres = filtered_data['Classificação Simplificada'].value_counts().reset_index()
    tipos_de_milagres.columns = ['Tipo', 'count']
    fig3 = px.bar(tipos_de_milagres, x='Tipo', y='count', title='Tipos de Milagres Simplificados Mais Frequentes',
                  labels={'Tipo': 'Tipo de Milagre Simplificado', 'count': 'Número de Ocorrências'})

    return fig1, fig2, fig3

# Callback para atualizar a tabela
@app.callback(
    Output('data-table', 'data'),
    [Input('colunas-filter', 'value')]
)
def update_table(columns):
    return data[columns].to_dict('records')

# Executa a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
