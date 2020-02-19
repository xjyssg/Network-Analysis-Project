import networkx as nx
import matplotlib.pyplot as plt


def network_structure(G):
    summary = {}
    summary["diameter"] = nx.diameter(G)
    summary["radius"] = nx.radius(G)
    summary["center"] = nx.center(G)
    return summary

def plot_network(G):
    nx.draw(G, node_size=80, node_color='red', with_labels=True)
    plt.show()


if __name__ == "__main__":
    G = nx.read_edgelist("test.edgelist", create_using=nx.DiGraph)
    print(network_structure(G))