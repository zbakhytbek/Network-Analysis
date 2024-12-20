import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

df0 = pd.read_excel('collaboration_network.xlsx', 'Co-author matrix', index_col=0)
df0.head()
df1 = pd.read_excel('collaboration_network.xlsx', 'Paper list')
df1.head()
df2 = pd.read_excel('collaboration_network.xlsx', 'People list')
df2.head()

getcountry = lambda s: s.split(', ')[-1]
df2['Country'] = df2['Location of Institutional affiliation in Column E [City (State), Country]'].apply(getcountry)
countries = df2['Country'].unique().tolist()

A_country = np.zeros((len(countries), len(countries)))

for a, row in df0.iterrows():
    country1 = df2[df2['ID'] == a]['Country'].values[0]
    for a1 in row.index[row==1].tolist():
        country2 = df2[df2['ID'] == a1]['Country'].values[0]
        
        if not country1 == country2:
            i1 = countries.index(country1)
            i2 = countries.index(country2)
            A_country[i1,i2] = A_country[i1,i2] + 1

plt.imshow(A_country)
plt.xticks(np.arange(0,18), countries, rotation='vertical')
plt.yticks(np.arange(0,18), countries)
plt.show()

for i in range(A_country.shape[0]):
    for j in range(A_country.shape[1]):
        print(A_country[i, j], end=' ')
    print()

G = nx.Graph(A_country, )
hist = nx.degree_histogram(G)
plt.bar(range(len(hist)), hist)
plt.xlabel('Degree')
plt.ylabel('Node Number')
plt.show()

for degree, count in enumerate(hist):
    print(f'Degree {degree}: {count} nodes')

degree_centrality = nx.centrality.degree_centrality(G)
plt.plot(degree_centrality.keys(), degree_centrality.values(), '-o')
plt.xticks(np.arange(0,18), countries, rotation='vertical')
plt.title('degree')
plt.show()

betweenness_centrality = nx.centrality.betweenness_centrality(G)
plt.plot(betweenness_centrality.keys(), betweenness_centrality.values(), '-o')
plt.xticks(np.arange(0,18), countries, rotation='vertical')
plt.title('betweenness')
plt.show()

closeness_centrality = nx.centrality.closeness_centrality(G)
plt.plot(closeness_centrality.keys(), closeness_centrality.values(), '-o')
plt.xticks(np.arange(0,18), countries, rotation='vertical')
plt.title('closeness')
plt.show()



labeldict = {}
for i, cont in enumerate(countries):
    labeldict.update({i: cont})
    
communitie = nx.community.louvain_communities(G)
colors = np.zeros((18,))
for node in range(18):
    for i, part in enumerate(communitie):
        if node in part:
            colors[node] = i
            
sizes = np.array(G.degree())[:, 1]*200 + 200
edge_weights = nx.get_edge_attributes(G, 'weight')
edge_widths = [edge_weights.get(edge, 1) for edge in G.edges()]
pos = nx.spring_layout(G,k=0.7,iterations=50)
nx.draw(G, labels=labeldict, node_color=colors, node_size=sizes, pos=pos, font_size=8, font_color='r', width=edge_widths, edge_cmap=plt.cm.Blues)
plt.show()


get_author1 = lambda s: s.split(' & ')[0].split(' et al.')[0]
def get_author2(s):
    l = s.split(' & ')
    if len(l) == 1:
        return None
    s = l[1].split(' et al.')[0]
    return s

df1['author1'] = df1['author(s)'].apply(get_author1)
df1['author2'] = df1['author(s)'].apply(get_author2)

get_surname = lambda s: s.split(',')[0]
df2['author surname'] = df2['author name'].apply(get_surname)

df2 = df2[df2['gender'].notna()]

genders1 = []
for surname in df1['author1']:
    gender = df2[df2['author surname'] == surname]['gender']
    if len(gender) > 0:
        genders1.append(gender.values[0])
        
plt.pie([genders1.count('M'), genders1.count('W')], labels=['M', 'W'], autopct='%1.1f%%')
plt.title('author 1 gender')
plt.show()

genders2 = []
for surname in df1['author2']:
    gender = df2[df2['author surname'] == surname]['gender']
    if len(gender) > 0:
        genders2.append(gender.values[0])

plt.pie([genders2.count('M'), genders2.count('W')], labels=['M', 'W'], autopct='%1.1f%%')
plt.title('author 2 gender')
plt.show()