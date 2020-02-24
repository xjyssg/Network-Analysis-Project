import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import comb


def degree_distribution(DiG):
    in_degrees = [DiG.in_degree(node) for node in DiG.nodes()]
    plt.subplot(1, 2, 1)
    sns.distplot(in_degrees, rug=True)
    out_degrees = [DiG.out_degree(node) for node in DiG.nodes()]
    plt.xlabel('in-degree')
    plt.ylabel('number')
    plt.title('in-degree distribution')
    plt.subplot(1, 2, 2)
    sns.distplot(out_degrees, rug=True)
    plt.xlabel('out-degree')
    plt.ylabel('number')
    plt.title('out-degree distribution')
    plt.savefig('./figures/degree_distribution.png')
    plt.show()
    return {"in": in_degrees, "out": out_degrees}

def triadic_closure(G):
    triangles = nx.triangles(G)
    triadic = {}
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        if len(neighbors) < 2:
            triadic[node] = 0
        else:
            triadic[node] = triangles[node] / comb(len(neighbors), 2)
    triadics = list(triadic.values())
    sns.distplot(list(triadic.values()), rug=True)
    plt.xlabel("ratio")
    plt.ylabel("number")
    plt.title("triangle ratio")
    plt.savefig('./figures/triadic_closure.png')
    plt.show()
    return triadic

def network_component(DiG, plot=False):
    weak_component = list(nx.weakly_connected_components(DiG))
    if plot:
        threshold = 500
        sm_dist = [len(sub) for sub in weak_component if len(sub) <= threshold]
        sns.distplot(sm_dist, rug=True)
        plt.xlabel("size")
        plt.ylabel("number")
        plt.title("weak components")
        plt.savefig('./figures/weak_components.png')
        plt.show()
    return DiG.subgraph(weak_component[0])

def network_structure(DiG):
    G = DiG.to_undirected()
    summary = {}
    summary["num_node"] = len(DiG.nodes())
    summary["num_edge"] = len(DiG.edges())
    clustering = nx.clustering(DiG)
    for node in clustering.keys():
        clustering[node] = round(clustering[node], 4)
    summary["clustering"] = clustering
    summary["num_strong"] = nx.number_strongly_connected_components(DiG)
    summary["num_weak"] = nx.number_weakly_connected_components(DiG)
    if summary["num_strong"] == 1:
        summary["diameter"] = nx.diameter(DiG)
        summary["radius"] = nx.radius(DiG)
        summary["center"] = nx.center(DiG)
    
    return summary

def spectral_network(DiG):
    nx.draw_spectral(DiG, node_size=200, with_labels=True)
    plt.show()


RUNPASSED = 0
if __name__ == "__main__":
    # DiG = nx.read_edgelist("test.edgelist", create_using=nx.DiGraph)
    DiG = nx.read_edgelist("citation.edgelist", create_using=nx.DiGraph)
    G = DiG.to_undirected()
    subgraph = network_component(DiG)
    summary = network_structure(subgraph)
    print(summary["num_weak"])
    print(summary["num_strong"])
    # print(summary["num_node"])
    if RUNPASSED:
        triadic_closure(G)
        degree_distribution(DiG)
        spectral_network(DiG)