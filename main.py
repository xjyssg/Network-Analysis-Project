import networkx as nx
import matplotlib.pyplot as plt

def degree_distribution(DiG):
    in_degrees = [DiG.in_degree(node) for node in DiG.nodes()]
    plt.subplot(1, 2, 1)
    plt.hist(in_degrees)
    out_degrees = [DiG.out_degree(node) for node in DiG.nodes()]
    plt.subplot(1, 2, 2)
    plt.hist(out_degrees)
    plt.savefig('./figures/degree_distribution.png')
    plt.show()
    return {"in": in_degrees, "out": out_degrees}

def network_structure(DiG):
    # G = DiG.to_undirected()
    summary = {}
    summary["diameter"] = nx.diameter(DiG)
    summary["radius"] = nx.radius(DiG)
    summary["center"] = nx.center(DiG)
    clustering = nx.clustering(DiG)
    for node in clustering.keys():
        clustering[node] = round(clustering[node], 4)
    summary["clustering"] = clustering
    summary["num_strong"] = nx.number_strongly_connected_components(DiG)
    summary["num_weak"] = nx.number_weakly_connected_components(DiG)

    return summary

def plot_network(G):
    nx.draw(G, node_size=80, node_color='red', with_labels=True)
    plt.show()


if __name__ == "__main__":
    G = nx.read_edgelist("test.edgelist", create_using=nx.DiGraph)
    print(network_structure(G))
    # plot_network(G)
    degree_distribution(G)