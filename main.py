import random as rd
import networkx as nx
from networkx.generators import random_graphs

C = {0.05: 0.003801658303553139101756466, 0.1: 0.014745844781072675877050816,
     0.15: 0.032220914373087674975117359, 0.2: 0.055704042949781851858398652,
     0.25: 0.084744091852316990275274806, 0.3: 0.118949192725403987583755553,
     0.35: 0.157983098125747077557540462, 0.4: 0.201547413607754017070679639,
     0.45: 0.249306998440163189714677100, 0.5: 0.302103025348741965169160432,
     0.55: 0.360397850933168697104686803, 0.6: 0.422649730810374235490851220,
     0.65: 0.481125478337229174401911323, 0.7: 0.571428571428571428571428572,
     0.75: 0.666666666666666666666666667, 0.8: 0.750000000000000000000000000,
     0.85: 0.823529411764705882352941177, 0.9: 0.888888888888888888888888889,
     0.95: 0.947368421052631578947368421}

chance = 0.3
trials = 20


# curr_trial is the # of trials (curr included) from last success
def PRD(chance, curr_trial):
    """Based on pseudo random method,

    :param block: a numpy array of 3 dimensions.
    :return: a list of the ways we can rotate the block. Each is a list of dicts containing parameters for np.rot90()

    >>> a = np.arange(64, dtype=int).reshape(4, 4, 4)  # a cube
    >>> rotations = get_orientations_possible(a)
    >>> len(rotations)
    23
    >>> rotations  # doctest: +ELLIPSIS
    [[{'k': 1, 'axes': (0, 1)}], ... [{'k': 3, 'axes': (1, 2)}, {'k': 3, 'axes': (0, 2)}]]
    >>> a = a.reshape(2, 4, 8)
    >>> len(get_orientations_possible(a))
    3
    >>> a = a.reshape(16, 2, 2)
    >>> len(get_orientations_possible(a))
    7
    >>> get_orientations_possible(np.array([[1, 2], [3, 4]]))
    Traceback (most recent call last):
    ValueError: array parameter block must have exactly 3 dimensions.
    >>> marble_block_1 = np.load(file='data/marble_block_1.npy')
    >>> len(get_orientations_possible(marble_block_1))
    7
    """

    curr_chance = C[chance] * curr_trial
    if rd.random() < curr_chance:
        return True
    return False


def TRD(chance):
    return rd.random() < chance


def getPRDSequence(chance, trials):
    seq = []
    curr_trial = 1
    for trial in range(trials):
        if PRD(chance, curr_trial):
            curr_trial = 1
            seq.append(trial)
        else:
            curr_trial += 1
    return seq


def getTRDSequence(chance, trials):
    seq = []
    for trial in range(trials):
        if TRD(chance):
            seq.append(trial)
    return seq


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
