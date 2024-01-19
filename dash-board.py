import pandas as pd
from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.graph_objs as go
import plotly.express as px

external_stylesheets = ['./assets/styles.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./librarySales.csv')

top10 = (
    df.groupby('Ano')
    .apply(lambda x: x.nlargest(10, 'Score'))
    .reset_index(drop=True)
)

opcoesAno = [{'label': str(ano), 'value': ano} for ano in top10['Ano'].unique()]

# Criando as opções para Dropdown dos gêneros dos livros
opcoesGenero = [{'label': 'Todos os gêneros', 'value': 'All'}] + [{'label': genero, 'value': genero} for genero in df['Genero'].unique()]

totalVendas = df.groupby('Ano')['Score'].sum().reset_index(name='totalV')

paletaCores = px.colors.sequential.Rainbow

melhorLiv = (
    df.groupby(['Ano', 'Titulo', 'Genero', 'Autor', 'Editora'], as_index=False)
    .agg({'Score': 'mean'})
    .sort_values(by=['Ano', 'Score'], ascending=[True, False])
    .groupby('Ano')
    .first()
    .reset_index()
)

app.layout = html.Div([
    html.Div(
        className="cabecalho",
        children=[
            html.H1(children='Analisando os livros mais vendidos entre 2010 a 2023')
        ],
    ),
    
    html.Div(
        className="resumo",
        children=[
            dcc.Markdown('''
                >
                > Os livros nunca deixaram de ser a opção principal de se obter conhecimento,
                  dito isso, decidimos analisar os livros mais vendidos desde 2010 a 2023 utilizando
                  dados coletados da página [publishnews.com.br](https://www.publishnews.com.br/ranking/anual/0/2023/0/0)
                >
                > Coletamos os *20 livros* mais vendidos de **cada ano** e de **cada gênero** informado pelo site.       
                >
            ''')
        ]
    ),

    html.Div(
        className="dataSet",
        children=[
            html.H3(f"Clique no botão para visualizar o Dataset"),
            dcc.Dropdown(
            id='dropdownDataset',
            options=[
                {'label': 'Esconder Dataset', 'value': 'esconder'},
                {'label': 'Mostrar Dataset', 'value': 'mostrar'}
            ],
            value='esconder',
            clearable=False
            ),
            html.Div(id='dataset', style={'display': 'none'}, children=[
            dash_table.DataTable(data=df.to_dict('records'), page_size=20),
            ]),
        
    ]),

    html.Div(
        className="enunciado",
        children=[
            html.H2(f'Análise 1')
        ],
    ),

    html.Div(
        className="botoes",
        children=[
            dcc.Dropdown(
                id='anos',
                options=opcoesAno,
                value=top10['Ano'].min(),
                
            ),
            dcc.Dropdown(
                id='generos',
                options=opcoesGenero,
                value='All', 
                
            ),
        ]
    ),
    
    html.Div(
        children=[
            dcc.Graph(id='graficoPizza'),
        ]
    ),

    html.Div(
        className="analise",
        children=[
            html.H3(f"Observações"),
            html.Div(
                className="paragrafos",
                children=[
                    dcc.Markdown('''
                        Os livros do gênero ** 'Negócios' ** só passaram a aparecer no rank a ** partir de 2018 **;

                        ** Box Harry Potter **  de *J. K. Rowling*, é o Box de livros ** mais vendido em 2020 **;

                        O livro ** 'Como eu era antes de você' ** de *Jojo Moyes*, ficou em primeiro lugar no rank de 2016, ** mesmo ano ** em que o ** filme ** baseado no mesmo foi lançado;
                    '''),
                    dcc.Markdown('''
                        Os livros do gênero ** 'Ficção' ** são os que estão em mais quantidade no rank, contando desde 2010 a 2023;

                        No período da pandemia do covid-19, os livros mais vendidos foram os dos gêneros ** Negócios **(2020-2021) e ** Ficção ** (2022-2023);

                        ** Steve Jobs ** de *Walter Isaacson*, é a primeira biografia a aparecer em rank.
                    ''')
                ]),
        ]),
    
    html.Div(
        className="enunciado",
        children=[
            html.H2(f'Análise 2')
        ],
    ),

    html.Div(
        className="vendas",
        children=[
            html.Div([
                html.H2(f"Top 1 Livro mais vendido por ano"),
                html.Table(
                    className='tabela', 
                    children=[
                        html.Tr([html.Th(col) for col in ['Ano', 'Título', 'Gênero', 'Autor', 'Editora', 'Score']])
                    ] +
                    [html.Tr([
                        html.Td(f"{ano}"),
                        html.Td(f"{titulo}"),
                        html.Td(f"{genero}"),
                        html.Td(f"{autor}"),
                        html.Td(f"{editora}"),
                        html.Td(f"{score}")
                    ]) for ano, titulo, genero, autor, editora, score in zip(melhorLiv['Ano'], melhorLiv['Titulo'], melhorLiv['Genero'], melhorLiv['Autor'], melhorLiv['Editora'], melhorLiv['Score'])]
                )
            ])
        ]
    ),

    html.Div(
        className="analise",
        children=[
            html.H3(f"Observações"),
            html.Div(
                className="paragrafos",
                children=[
                    dcc.Markdown('''
                        O ** gênero ** de livros que ficaram em *1º lugar* ao decorrer dos anos foram os de ** Autoajuda **;
            
                        ** 2023 ** tem o ** menor Score ** registrado dentre os anos de 2010 a 2023 com ** Café com Deus pai ** de *Junior Rostirola*;
                    '''),
                    dcc.Markdown('''
                        ** 2014 ** é o ano com o livro de ** maior Score ** entre o período de 2010 a 2023 com o livro ** Nada a perder 3 ** de *Edir Macedo*;
                    
                        ** Ágape ** de *Padre Marcelo Rossi*; ** A sutil arte de ligar o foda-se ** de *Mark Manson*; ** Mais esperto que o diabo ** de *Napoleon Hill* foram Títulos que lideraram o ranking por ** dois anos ** seguidos;
                    ''')
            ]),        
        ]
    ),    

    html.Div(
        className="enunciado",
        children=[
            html.H2(f'Análise 3')
        ],
    ),

        html.Div(
            className="vendas",
            children=[
                dcc.Graph(
                    id='vendasT',
                    figure=px.scatter(totalVendas, x='Ano', y='totalV', color='totalV', size='totalV', 
                                    labels={'totalV': 'Score total'},
                                    title='Total de Vendas por Ano',
                                    color_continuous_scale=paletaCores),
                                   
                )
            ]
        ),

            html.Div(
        className="analise",
        children=[
            html.H3(f"Observações"),
            html.Div(
                className="paragrafos",
                children=[
                    dcc.Markdown('''
                        Podemos notar uma **crescente na média de Vendas** entre o **período de 2010 a 2014**;                          
                
                        **2014 é o ano com a maior média de vendas registrada**, com uma média de Score total de 6700.04;
                        
                        O período de *2020 a 2023* (pandemia covid-19), possuem as **menores médias** de Score total registrada dentre todos os demais anos.

                    '''),
                
                ]),
        ]),

    ])

@app.callback(
    Output('graficoPizza', 'figure'),
    [Input('anos', 'value'),
     Input('generos', 'value')]
)
def pizza(selecionarAno, selecionarGenero):
    filtroAno = top10
    if selecionarGenero != 'All':
        filtroAno = filtroAno[filtroAno['Genero'] == selecionarGenero]
    filtroAno = filtroAno[filtroAno['Ano'] == selecionarAno]

    labels = filtroAno['Titulo']
    values = filtroAno['Score']
    textInfo = [
        f'Título: {titulo}<br>Autor: {autor}<br>Editora: {editora}<br>Score: {score}'
        for titulo, autor, editora, score in zip(filtroAno['Titulo'], filtroAno['Autor'], filtroAno['Editora'], filtroAno['Score'])
    ]

    trace = go.Pie(
        labels=labels,
        values=values,
        
        hoverinfo='text+percent',  # Mostra as informações dentro da fatia e seu percentual ao passar o mouse por cima
        text=textInfo,
        textinfo='none',  # Não mostrar o texto fora da fatia
        marker=dict(line=dict(color='white', width=2)),
    )

    layout = go.Layout(
        title=f'Top 10 Livros Mais Vendidos em {selecionarAno}',
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig

# Callback para atualizar a visibilidade da tabela
@app.callback(
    Output('dataset', 'style'),
    [Input('dropdownDataset', 'value')]
)
def visualizador(visibilidade):
    if visibilidade == 'mostrar':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)
