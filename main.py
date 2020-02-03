import networkx as nx

G = nx.read_edgelist("citation.edgelist")
# nx.draw(G, node_size=80, node_color='red', with_labels=True)
# plt.show()
print(G.nodes())