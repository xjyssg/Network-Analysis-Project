import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns


def degree_distribution(DiG):
    in_degrees = [DiG.in_degree(node) for node in DiG.nodes()]
    plt.subplot(1, 2, 1)
    sns.distplot(in_degrees, rug=True)
    out_degrees = [DiG.out_degree(node) for node in DiG.nodes()]
    plt.xlabel('in-degree')
    plt.ylabel('number')
    plt.subplot(1, 2, 2)
    sns.distplot(out_degrees, rug=True)
    plt.xlabel('out-degree')
    plt.ylabel('number')
    plt.savefig('./figures/degree_distribution.png')
    plt.show()
    return {"in": in_degrees, "out": out_degrees}

def network_structure(DiG):
    G = DiG.to_undirected()
    summary = {}
    # summary["diameter"] = nx.diameter(DiG)
    # summary["radius"] = nx.radius(DiG)
    # summary["center"] = nx.center(DiG)
    clustering = nx.clustering(DiG)
    for node in clustering.keys():
        clustering[node] = round(clustering[node], 4)
    summary["clustering"] = clustering
    summary["num_strong"] = nx.number_strongly_connected_components(DiG)
    summary["num_weak"] = nx.number_weakly_connected_components(DiG)
    summary["triangles"] = nx.triangles(G)
    return summary

def plot_network(DiG):
    nx.draw(DiG, node_size=80, node_color='red', with_labels=True)
    plt.show()
    nx.draw_spectral(DiG)
    plt.show()


if __name__ == "__main__":
    # DiG = nx.read_edgelist("test.edgelist", create_using=nx.DiGraph)
    DiG = nx.read_edgelist("citation.edgelist", create_using=nx.DiGraph)
    # summary = network_structure(DiG)
    # plot_network(DiG)
    # print(summary["num_strong"])
    # print(summary["num_weak"])
    degree_distribution(DiG)