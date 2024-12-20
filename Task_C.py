import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_excel('collaboration_network.xlsx', 'Paper list')
df1.head()
df2 = pd.read_excel('collaboration_network.xlsx', 'People list')
df2.head()

get_surname = lambda s: s.split(',')[0]
df2['author surname'] = df2['author name'].apply(get_surname)

G = nx.DiGraph()

for authors in df1['author(s)']:
    authors_list = authors.split(' et al.')[0].split(' & ')
    if len(authors_list) == 1:
        continue
    author1 = authors_list[0]
    for author in authors_list[1:]:
        G.add_edge(author1, author)  

colors = []
for node in G.nodes():
    gender = df2[df2['author surname'] == node]['gender']
    if len(gender) == 0:
        colors.append(1)
        continue

    if gender.values[0] == 'W':
        colors.append(0)
    else:
        colors.append(1)
        
pos = nx.spring_layout(G, k=0.45,iterations=50)

plt.figure(figsize=(10,10))
nx.draw(G, pos=pos, node_size=2500, with_labels=True, node_color=colors, font_color='r')
plt.show()

communiti = nx.community.louvain_communities(G)
print(communiti)

nx.density(G)

plt.figure(figsize=(5,8))
pagerank_scores = nx.pagerank(G)
plt.barh(list(pagerank_scores.keys()), pagerank_scores.values())
plt.show()

number_authors_per_paper = df1['author(s)'].apply(lambda x: len(x.split(' & ')))
plt.hist(number_authors_per_paper)
plt.xlabel('Authors per Paper')
plt.ylabel('Frequency')
plt.title('Distribution of Authors')
plt.show()

indegree_centrality = nx.centrality.in_degree_centrality(G)
plt.hist(indegree_centrality.values())
plt.title('In degree')
plt.show()

outdegree_centrality = nx.centrality.out_degree_centrality(G)
plt.hist(outdegree_centrality.values())
plt.title('Out degree')
plt.show()

