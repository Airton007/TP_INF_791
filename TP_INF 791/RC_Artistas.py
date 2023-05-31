
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import random

# Carrega os dados da planilha
planilha = pd.read_excel(r'C:\Users\Airton\Desktop\TRabalho\filmes_100.xlsx')

# Cria o grafo
G = nx.Graph()

# Obtendo os nomes das colunas
colunas = planilha.columns

# Obtem os nomes dos artistas a partir dos cabeçalhos das colunas
artistas = colunas[1:]

# Itera sobre os filmes
for i, row in planilha.iterrows():
    filme = row['Filmes']
    artistas_participantes = row[artistas].dropna().tolist()

    # Adiciona as arestas entre os artistas
    for j, artista1 in enumerate(artistas_participantes):
        for k, artista2 in enumerate(artistas_participantes):
            if j < k and artista1 != artista2:
                if not G.has_edge(artista1, artista2):
                    G.add_edge(artista1, artista2, filmes=[filme])
                else:
                    G[artista1][artista2]['filmes'].append(filme)

# Calcula o grau de cada nó
graus = dict(G.degree())
# print(graus)

 # Calcula o maior e menor grau de conectividade
maior_grau = max(graus.values())
print('Maior grau de conectividade:',maior_grau)

menor_grau = min(graus.values())
print('Menor grau de conectividade:',menor_grau)
      
# Calcula o número total de nós com conectividade máxima
conectividade_maxima = maior_grau
numero_total_de_nos = G.number_of_nodes()
contador = 0

for no, grau in graus.items():
    if grau == conectividade_maxima:
        contador += 1

print("Número de nós com conectividade máxima:", contador)

# Calcula a distribuição do grau
degree_sequence = [d for n, d in G.degree()]

# Calcula a frequência de cada valor de grau
degree_counts = nx.degree_histogram(G)

# Plota o gráfico da distribuição do grau
plt.bar(range(len(degree_counts)), degree_counts)
plt.xlabel('Grau')
plt.ylabel('Frequência')
plt.title('Distribuição do Grau')
plt.show()

# Exibe informações do grafo
print("Número de nós (artistas):", G.number_of_nodes())
print("Número de arestas (filmes):", G.number_of_edges())

# Calcula o grau médio
grau_medio = round(sum(dict(G.degree()).values()) / len(G),3)
print("Grau Médio:",grau_medio)

#Calcula o número de componentes do grafo
print("Número de componentes do grafo:", nx.number_connected_components(G))

# Verifica se o grafo está conectado
if nx.is_connected(G):
    print("Distância média:", nx.average_shortest_path_length(G))
else:
    print("O grafo não está conectado.")

# calcula o Coeficiente de clusterização de cada nó
coeficientes_clusterizacao = nx.clustering(G)
# Obtem os valores dos coeficientes de clusterização
valores_clusterizacao = list(coeficientes_clusterizacao.values())

# Plota o gráfico dos coeficientes de clusterização
plt.hist(valores_clusterizacao, bins=10)
plt.xlabel('Coeficiente de Clusterização')
plt.ylabel('Frequência')
plt.title('Distribuição dos Coeficientes de Clusterização')
plt.show()

# Calcula Coeficiente de clusterização global do grafo
coeficiente_clusterizacao_global = round(nx.average_clustering(G),3)
print('Coeficiente de Cluterização global:', coeficiente_clusterizacao_global)

# Calcula de distribuição dos componentes
componentes = nx.connected_components(G)
tamanhos_componentes = [len(componente) for componente in componentes]

# Plota o gráfico da Distribuição do tamanho dos componentes
plt.hist(tamanhos_componentes, bins='auto')
plt.xlabel('Tamanho dos componentes')
plt.ylabel('Contagem')
plt.title('Distribuição do tamanho dos componentes')
plt.show()

'''distribuicao = {}
for tamanho in tamanhos_componentes:
    if tamanho in distribuicao:
        distribuicao[tamanho] += 1
    else:
        distribuicao[tamanho] = 1

print("Distribuição do tamanho dos componentes:")
for tamanho, count in distribuicao.items():
    print("Tamanho", tamanho, "- Quantidade", count)'''
# Calculando o overlap da vizinhança para cada par de nodo

overlaps = []
for i, nodo1 in enumerate(G.nodes()):
    for j, nodo2 in enumerate(G.nodes()):
        if i < j:
            vizinhos_nodo1 = set(G.neighbors(nodo1))
            vizinhos_nodo2 = set(G.neighbors(nodo2))
            overlap = len(vizinhos_nodo1.intersection(vizinhos_nodo2))
            overlaps.append(overlap)

# Plota o gráfico da distribuição dos valores de overlap
plt.hist(overlaps, bins=20)
plt.xlabel('Overlap')
plt.ylabel('Frequência')
plt.title('Distribuição do Overlap da Vizinhança')
plt.show()

# Personalizar o tamanho dos nós
node_size = [v * 100 for v in graus.values()]  # Ajuste o multiplicador conforme necessário

# Calculando a distância média e a distribuição das distâncias de todos os nodos da rede
distancias = dict(nx.shortest_path_length(G))
distancias_medias = round(sum(sum(distancias[n].values()) for n in G.nodes()) / (G.number_of_nodes() - 1),3)
distancias_valores = [distancia for nodo_distancias in distancias.values() for distancia in nodo_distancias.values()]
print('Distância média:', distancias_medias)

# Distribuição das distâncias
plt.hist(distancias_valores, bins=20)
plt.xlabel('Distância')
plt.ylabel('Frequência')
plt.title('Distribuição das Distâncias')
plt.show()

# Personaliza o tamanho dos nós
node_size = [v * 75 for v in graus.values()]  # Ajuste o multiplicador conforme necessário

# Personaliza a aparência do gráfico
node_labels = {artista: artista for artista in G.nodes()}  # Usar o nome do artista como rótulo
plt.title("Grafo de colaboração entre artistas em filmes", pad = -40, fontsize=14)
plt.axis('off')

# Define as cores para cada nó de acordo com o grau
cores = [graus[n] for n in G.nodes()]
node_color = cores
font_size = 0
edge_color = 'gray'
edge_width = 0.2

# Criação do layout do grafo
layout = nx.spring_layout(G, seed=42, scale=5, k=1) # Layout spring
#layout = nx.random_layout(G, seed=28)  # Layout aleatório
#layout = nx.kamada_kawai_layout(G)  # Layout kamada_kawai

# Personaliza o layout, ajusta o espaçamento entre os elementos do gráfico
plt.tight_layout() 

# Plotagem do grafo
plt.figure(figsize=(20, 25))  
nx.draw_networkx(G, pos=layout, with_labels=True, node_color=node_color, cmap='viridis', node_size=node_size, edge_color=edge_color,
                 width=edge_width, labels=node_labels, font_size=font_size)

# Salva o gráfico em um arquivo de imagem
plt.savefig('grafo_personalizado.png', dpi=600)  # Substitua o nome do arquivo conforme necessário

# Exibe o gráfico
plt.show()