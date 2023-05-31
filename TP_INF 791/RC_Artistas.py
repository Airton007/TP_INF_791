
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import random

# Carregar os dados da planilha
planilha = pd.read_excel(r'C:\Users\Airton\Desktop\TRabalho\filmes_100.xlsx')

# Criar o grafo
G = nx.Graph()

# Obtendo os nomes das colunas
colunas = planilha.columns

# Obter os nomes dos artistas a partir dos cabeçalhos das colunas
artistas = colunas[1:]

# Iterar sobre os filmes
for i, row in planilha.iterrows():
    filme = row['Filmes']
    artistas_participantes = row[artistas].dropna().tolist()

    # Adicionar as arestas entre os artistas
    for j, artista1 in enumerate(artistas_participantes):
        for k, artista2 in enumerate(artistas_participantes):
            if j < k and artista1 != artista2:
                if not G.has_edge(artista1, artista2):
                    G.add_edge(artista1, artista2, filmes=[filme])
                else:
                    G[artista1][artista2]['filmes'].append(filme)

# Calcular o grau de cada nó
graus = dict(G.degree())

# Coeficiente de clusterização de cada nodo
coeficientes_clusterizacao = nx.clustering(G)

# Coeficiente de clusterização global do grafo
coeficiente_clusterizacao_global = nx.average_clustering(G)

# Calculando o overlap da vizinhança para cada par de nodo
overlaps = []
for i, nodo1 in enumerate(G.nodes()):
    for j, nodo2 in enumerate(G.nodes()):
        if i < j:
            vizinhos_nodo1 = set(G.neighbors(nodo1))
            vizinhos_nodo2 = set(G.neighbors(nodo2))
            overlap = len(vizinhos_nodo1.intersection(vizinhos_nodo2))
            overlaps.append(overlap)

# Distribuição dos valores de overlap
plt.hist(overlaps, bins=20)
plt.xlabel('Overlap')
plt.ylabel('Frequência')
plt.title('Distribuição do Overlap da Vizinhança')
plt.show()

# Calcular o grau de cada nó
graus = dict(G.degree())

# Personalizar o tamanho dos nós
node_size = [v * 100 for v in graus.values()]  # Ajuste o multiplicador conforme necessário

# Calculando a distância média e a distribuição das distâncias de todos os nodos da rede
distancias = dict(nx.shortest_path_length(G))
distancias_medias = sum(sum(distancias[n].values()) for n in G.nodes()) / (G.number_of_nodes() - 1)
distancias_valores = [distancia for nodo_distancias in distancias.values() for distancia in nodo_distancias.values()]

# Distribuição das distâncias
plt.hist(distancias_valores, bins=20)
plt.xlabel('Distância')
plt.ylabel('Frequência')
plt.title('Distribuição das Distâncias')
plt.show()

# Personalizar o tamanho dos nós
node_size = [v * 50 for v in graus.values()]  # Ajuste o multiplicador conforme necessário

# Personalizar a aparência do gráfico
node_labels = {artista: artista for artista in G.nodes()}  # Usar o nome do artista como rótulo
node_color = 'skyblue'  # Cor do nó
font_size = 8  # Tamanho da fonte
edge_color = 'gray'  # Cor das arestas
edge_width = 0.2  # Espessura das arestas
layout = nx.random_layout(G, seed=28)  # Layout aleatório
#layout = nx.kamada_kawai_layout(G)  # Layout kamada_kawai
#layout = nx.spring_layout(G, seed=42)  # Layout spring

# Exibir informações do grafo
print("Número de nós (artistas):", G.number_of_nodes())
print("Número de arestas (filmes):", G.number_of_edges())
print("Grau médio do grafo:", nx.average_degree_connectivity(G))
print("Número de componentes do grafo:", nx.number_connected_components(G))
print("Coeficiente de clusterização de cada nó:", nx.clustering(G))

# Verificar se o grafo está conectado
if nx.is_connected(G):
    print("Distância média:", nx.average_shortest_path_length(G))
else:
    print("O grafo não está conectado.")


# Plotar o grafo
plt.figure(figsize=(20, 30))  # Tamanho da figura
nx.draw_networkx(G, pos=layout, node_color=node_color, node_size=node_size, edge_color=edge_color,
                 width=edge_width, labels=node_labels, font_size=font_size)

# Personalizar o estilo do grafo
plt.title("Grafo de colaboração entre artistas e filmes", fontsize=16)
plt.axis('off')  # Desabilitar os eixos

# Personalizar o layout
plt.tight_layout()  # Ajustar o espaçamento entre os elementos do gráfico

# Salvar o gráfico em um arquivo de imagem
plt.savefig('grafo_personalizado.png', dpi=300)  # Substitua o nome do arquivo conforme necessário

# Exibir o gráfico
plt.show()