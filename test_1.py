import networkx as nx
from networkx.generators import random_graphs
from test import *

chance = 0.3
trials = 20
tries = 100


def test_run():
    G = random_graphs.dense_gnm_random_graph(1000, 5000)
    trd_graph = G.copy()
    trd_graph = test_on_graph(trd_graph, True)
    (trd_graph, trd_sqr_diff) = process_graph(trd_graph)
    prd_graph = G.copy()
    prd_graph = test_on_graph(prd_graph, False)
    (prd_graph, prd_sqr_diff) = process_graph(prd_graph)
    return trd_sqr_diff, prd_sqr_diff


def test_on_graph(G, is_trd):
    if is_trd:
        for node_index in G.nodes:
            trd_seq = getTRDSequence(chance, trials)
            length = len(trd_seq)
            G.nodes[node_index]['hit'] = length
    else:
        for node_index in G.nodes:
            prd_seq = getPRDSequence(chance, trials)
            length = len(prd_seq)
            G.nodes[node_index]['hit'] = length
    return G


def process_graph(G):
    graph_sqr_diff = 0.0
    for node_index in G.nodes:
        hit = G.nodes[node_index]['hit']
        if len(G.adj[node_index]) == 0:
            mean_sqr_diff = 0.0
        else:
            sum_sqr_diff = 0.0
            for nbr_index in G.adj[node_index]:
                nbr_hit = G.nodes[nbr_index]['hit']
                sum_sqr_diff += (hit - nbr_hit) ** 2
            mean_sqr_diff = sum_sqr_diff / len(G.adj[node_index])
        G.nodes[node_index]['mean_sqr_diff'] = mean_sqr_diff
        graph_sqr_diff += mean_sqr_diff
    graph_sqr_diff /= len(G.nodes)
    return G, graph_sqr_diff


total_trd_diff = 0
total_prd_diff = 0
for i in range(0, 10):
    (trd_sqr_diff, prd_sqr_diff) = test_run()
    total_prd_diff += prd_sqr_diff
    total_trd_diff += trd_sqr_diff

print(total_trd_diff, total_prd_diff)