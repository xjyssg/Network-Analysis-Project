import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import comb
import pandas as pd
import numpy as np

def degree_distribution(DiG, plot=False):
    in_degrees = {}
    out_degrees = {}
    for node in DiG.nodes():
        in_degrees[node] = DiG.in_degree(node)
        out_degrees[node] = DiG.out_degree(node)
    if plot:
        # plt.subplot(1, 2, 1)
        sns.distplot(list(in_degrees.values()), rug=True)
        plt.xlabel('in-degree')
        plt.ylabel('number')
        plt.title('in-degree distribution')
        plt.savefig('./figures/in_degree_distribution.png')
        plt.show()
        # plt.subplot(1, 2, 2)
        sns.distplot(list(out_degrees.values()), rug=True)
        plt.xlabel('out-degree')
        plt.ylabel('number')
        plt.title('out-degree distribution')
        plt.savefig('./figures/out_degree_distribution.png')
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
    # summary["clustering"] = clustering
    summary["num_strong"] = nx.number_strongly_connected_components(DiG)
    summary["num_weak"] = nx.number_weakly_connected_components(DiG)
    # if summary["num_weak"] == 1:
    #     print("!@@@!")
    #     summary["diameter"] = nx.diameter(G)
    #     summary["radius"] = nx.radius(G)
    #     summary["center"] = nx.center(G)
    return summary

def spectral_network(DiG):
    nx.draw_spectral(DiG, node_size=200, with_labels=True)
    plt.show()

def influenced_paper(DiG, plot=False):
    ReDiG = DiG.reverse()
    influenced = {}
    for node in ReDiG.nodes():
        node_list = []
        for n1 in ReDiG.neighbors(node):
            node_list.append(n1)
            for n2 in ReDiG.neighbors(n1):
                node_list.append(n2)
        influenced[node] = len(set(node_list))
    if plot:
        sns.distplot(list(influenced.values()), rug=True)
        plt.xlabel("papers")
        plt.ylabel("number")
        plt.title("influenced papers")
        plt.savefig('./figures/influenced_papers.png')
        plt.show()
    return influenced

def top_papers(records, num):
    sorted_records = sorted(records.items(), key=lambda r:r[1], reverse=True)
    tops = sorted_records[:num]
    rank = 1
    result = {}
    for paper, citation in tops:
        result[paper] = (rank, citation)
        rank += 1
    return result

def citation_comparison(DiG, plot=False):
    degrees = degree_distribution(DiG, plot)
    num = 20
    top_deg = top_papers(degrees["in"], num)
    influenced = influenced_paper(DiG, plot)
    top_inf = top_papers(influenced, num)
    papers = set(top_deg.keys()).union(set(top_inf.keys()))
    df = pd.DataFrame(columns=["deg", "inf"], index=papers)
    for idx in df.index:
        df["deg"][idx] = 1 / top_deg.get(idx, [-20])[0]
        df["inf"][idx] = 1 / top_inf.get(idx, [-20])[0]
    if plot:
        df.plot(kind='bar')
        plt.xlabel("papers")
        plt.ylabel("influence")
        plt.title("popular papers")
        plt.savefig('./figures/citation_comparison.png')
        plt.show()

RUNPASSED = 0
if __name__ == "__main__":
    # DiG = nx.read_edgelist("test.edgelist", create_using=nx.DiGraph)
    DiG = nx.read_edgelist("citation.edgelist", create_using=nx.DiGraph)
    # print(network_structure(DiG))
    G = DiG.to_undirected()
    # subgraph = network_component(DiG)
    # summary = network_structure(subgraph)
    # degrees = degree_distribution(DiG, plot=True)
    # indeg = [degree for degree in list(degrees['in'].values()) if degree < 400]
    # sns.distplot(indeg, rug=True)
    # plt.show()
    # print(summary)
    # citation_comparison(DiG,True)
    lambd1 = 0.7
    lambd2 = 0.4
    x = np.arange(0,15,0.1)
    y1 = lambd1*np.exp(-lambd1*x)
    y2 = lambd2*np.exp(-lambd2*x)
    l1, = plt.plot(x,y1)
    plt.title("exponential distribution")
    plt.legend(handles=[l1,], labels=['lambda=0.7',],  loc='best')
    plt.show()

    if RUNPASSED:
        influenced_paper(DiG)
        triadic_closure(G)
        spectral_network(DiG)