
import requests
import pandas as pd

#Chamar os melhores filmes, "top filmes'
def get_top_movies(page):
    url = 'https://api.themoviedb.org/3/movie/top_rated'
    params = {
        'api_key': 'efaf998208c473311f88a91abee25763',
        'language': 'en-US',
        'page': page
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        print(f'Erro ao obter os filmes: {response.status_code}')
        return None

#Chamar os detalhes dos filmes
def get_movie_details(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {
        'api_key': 'efaf998208c473311f88a91abee25763',
        'language': 'en-US'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Erro ao obter os detalhes do filme {movie_id}: {response.status_code}')
        return None

# Obter os dados dos melhores filmes
total_pages = 5
movie_data = []

# Iterar sobre as páginas de filmes
for page in range(1, total_pages+1):
    top_movies = get_top_movies(page)
    
    if top_movies:
        # Iterar sobre os filmes da página atual
        for movie in top_movies:
            movie_id = movie['id']
            movie_details = get_movie_details(movie_id)
            
            if movie_details:
                title = movie_details['title']
                release_year = movie_details['release_date'].split('-')[0]
                cast = []
                
                # Obter o elenco do filme
                credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
                credits_params = {
                    'api_key': 'efaf998208c473311f88a91abee25763'
                }
                
                credits_response = requests.get(credits_url, params=credits_params)
                
                if credits_response.status_code == 200:
                    credits_data = credits_response.json()
                    cast_data = credits_data['cast']
                    
                    for actor in cast_data:
                        cast.append(actor['name'])
                
                # Adicionar os dados do filme na lista
                movie_data.append({
                    'Title': title,
                    'Release Year': release_year,
                    'Cast': ', '.join(cast)
                })
            
            # Exibir o progresso
            print(f'Obtendo dados do filme {len(movie_data)}/{total_pages*20}')
    
# Criar um DataFrame a partir dos dados
df = pd.DataFrame(movie_data)

# Salvar os dados em uma planilha
df.to_excel(r'caminho_do_diretorio\filmes_100_2.xlsx', index=False)
print('Dados salvos com sucesso!')
