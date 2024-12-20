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

def get_institution(s):
    s = s.split(' (')[0]
    if s[-1] == ' ':
        return s[:-1]
    return s

institutions = df2['Published affiliation - one affiliation only (Paper IDs comma separated)'].apply(get_institution).unique().tolist()

A_reg = np.zeros((len(institutions), len(institutions)))
A_nat = np.zeros((len(institutions), len(institutions)))
A_int = np.zeros((len(institutions), len(institutions)))

for a1, row in df0.iterrows():
    institution1 = df2[df2['ID'] == a1]['Published affiliation - one affiliation only (Paper IDs comma separated)'].apply(get_institution).values[0]
    place1 = df2[df2['ID'] == a1]['Location of Institutional affiliation in Column E [City (State), Country]'].values[0]
    for a2 in row.index[row==1].tolist():
        institution2 = df2[df2['ID'] == a2]['Published affiliation - one affiliation only (Paper IDs comma separated)'].apply(get_institution).values[0]
        place2 = df2[df2['ID'] == a2]['Location of Institutional affiliation in Column E [City (State), Country]'].values[0]

        
        if pd.isna(institution1) or pd.isna(institution2):
            continue
        if not institution1 == institution2:
            i1 = institutions.index(institution1)
            i2 = institutions.index(institution2)
            if place1 == place2:
                A_reg[i1,i2] = A_reg[i1,i2] + 1
            elif place1.split(', ')[-1] == place2.split(', ')[-1]:
                A_nat[i1,i2] = A_nat[i1,i2] + 1
            else:
                A_int[i1,i2] = A_int[i1,i2] + 1                

plt.subplot(1,3,1)
plt.imshow(A_reg)
plt.title('reg')
plt.subplot(1,3,2)
plt.imshow(A_nat)
plt.title('nat')
plt.subplot(1,3,3)
plt.imshow(A_int)
plt.title('int')
plt.show()

G_reg = nx.Graph(A_reg)
G_nat = nx.Graph(A_nat)
G_int = nx.Graph(A_int)

for G in [G_reg, G_nat, G_int]:
    degree_centrality = nx.centrality.degree_centrality(G)
    plt.plot(degree_centrality.keys(), degree_centrality.values(), '-o')
    plt.title('degree')
    plt.show()
    
for G in [G_reg, G_nat, G_int]:
    betweenness_centrality = nx.centrality.betweenness_centrality(G)
    plt.plot(betweenness_centrality.keys(), betweenness_centrality.values(), '-o')
    plt.title('betweenness')
    plt.show()
    
for G in [G_reg, G_nat, G_int]:
    closeness_centrality = nx.centrality.closeness_centrality(G)
    plt.plot(closeness_centrality.keys(), closeness_centrality.values(), '-o')
    plt.title('closeness')
    plt.show()
    
labeldict = {}
for i, cont in enumerate(institutions):
    labeldict.update({i: cont})
G = nx.Graph(A_reg + A_nat + A_int)
sizes = np.array(G.degree())[:, 1]*200 + 200
communiti = nx.community.louvain_communities(G)
colors = np.zeros((len(institutions),))
for node in range(len(institutions)):
    for i, part in enumerate(communiti):
        if node in part:
            colors[node] = i
pos = nx.spring_layout(G,k=0.9,iterations=50)
plt.figure(figsize=(10,10))
nx.draw(G_reg, edge_color='r', labels=labeldict, node_color=colors, node_size=sizes, pos=pos, font_size=6)
nx.draw(G_nat, edge_color='g', labels=labeldict, node_color=colors, node_size=sizes, pos=pos, font_size=6)
nx.draw(G_int, edge_color='b', labels=labeldict, node_color=colors, node_size=sizes, pos=pos, font_size=6)
plt.show()

max_community_size = 0
max_community = {}
for community in communiti:
    if max_community_size < len(community):
        max_community_size = len(community)
        max_community = community

max_community = list(max_community)

max_community_labeldict = dict()
for node in max_community:
    max_community_labeldict.update({node: labeldict[node]})
list(max_community_labeldict.items())
print(list(max_community_labeldict.items()))