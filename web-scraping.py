import requests
from bs4 import BeautifulSoup
import pandas as pd

# Listas para criar dataset
Titulo = []
Autor = []
Editora = []
Score = []
Ano = []
Genero = []

generos = {
    "Ficção": "9",
    "Não Ficção": "13",
    "Autoajuda": "5",
    "Infantojuvenil": "11",
    "Negócios": "8"
}

for genNome, x in generos.items():
    for i in range(10, 24):
        ano = 2000 + i

        url = f'https://www.publishnews.com.br/ranking/anual/{x}/20{i}/0/0'

        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            titulos = soup.find_all('div', class_='pn-ranking-livro-nome')
            autor = soup.find_all('div', class_='pn-ranking-livro-autor')
            editora = soup.find_all('div', class_='pn-ranking-livro-editora')
            score = soup.find_all('div', class_='pn-ranking-livros-posicao-volume')

            for titulo in range(len(titulos)):
                if titulo < len(autor) and titulo < len(editora) and titulo < len(score):
                    # print(f'Ano: {ano} - Gênero: {genNome} - '
                    #     f'Título: {titulos[titulo].text} - '
                    #     f'Autor: {autor[titulo].text} - '
                    #     f'Editora: {editora[titulo].text} - '
                    #     f'Score: {score[titulo].text}\n')

                    # Atribuindo os valores para dentro das listas
                    Titulo.append(titulos[titulo].text)
                    Autor.append(autor[titulo].text)
                    Editora.append(editora[titulo].text)
                    Score.append(score[titulo].text)
                    Ano.append(ano)
                    Genero.append(genNome)

                    
                else:
                    print(f'Erro: Dados faltando para o título {titulos[titulo].text}')
        else:
            print(f'Falha, status {response.status_code} - Ano: {ano} - Gênero: {genNome}')

dados = pd.DataFrame({
    'Genero': Genero,
    'Ano': Ano,
    'Score': Score,
    'Titulo': Titulo,
    'Autor': Autor,
    'Editora': Editora,
    
})

print(dados.head())

# Comando para criar dataset (Execute-o somente uma vez e depois comente a linha novamente)
# dados.to_csv('librarySales.csv', index=False) 