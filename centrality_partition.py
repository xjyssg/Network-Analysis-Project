#!/usr/bin/env python
# coding: utf-8

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice

G = nx.read_edgelist(path = "test.edgelist")

# compute centrality (degree, betweenness, closeness) of nodes
def centrality(G, k = None, normalized = True, weight=None, endpoints=False, distance=None, seed=None):
    centrality = {}
    centrality["degree"] = nx.degree_centrality(G)
    centrality["betweeness"] = nx.betweenness_centrality(G, k=k, normalized=normalized, weight=weight, endpoints=endpoints, seed=seed)
    centrality["closeness"] = nx.closeness_centrality(G, distance=distance)
    return centrality

centrality = centrality(G, seed = 123)


def getModularity(gn_tuple, max_iter = 100):
    # set the max_iter to the length of gn_generator        
    max_iter = len(gn_tuple)
    modularity = []
    k = 1
    while k < max_iter: 
        gn_communities = gn_tuple[k]
        mod = nx.algorithms.community.modularity(G, gn_communities)
        modularity.append(mod)
        k = k + 1
    return(modularity)            


# Graph partition
gn_generator = nx.algorithms.community.centrality.girvan_newman(G)
gn_tuple = tuple(gn_generator)
modularity = getModularity(gn_tuple)
mod_best = max(modularity) 
gn_communities_best = gn_tuple[modularity.index(mod_best)]
    
gn_dict_communities = {}
for i, c in enumerate(gn_communities_best):
    print ("Community {}".format(i))
    for node in c:
        gn_dict_communities[node] = i + 1
        
for node in G:
    if node not in gn_dict_communities.keys():
        gn_dict_communities[node] = -1
        
# gn_pos = community_layout(G, gn_dict_communities) # Manually creating layout
gn_pos = nx.spectral_layout(G)

from matplotlib import cm
gn_colors = []
for node in G.nodes:
    gn_colors.append(cm.Set1(gn_dict_communities[node]))
    
plt.figure(figsize=(10,10))
nx.draw_networkx_nodes(G, gn_pos, node_color=gn_colors, node_size=500)
nx.draw_networkx_edges(G, gn_pos, alpha=0.2)
plt.axis('off')
plt.show()

