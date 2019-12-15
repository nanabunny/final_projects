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

chance = 0.7
trials = 20


# curr_trial is the # of trials (curr included) from last success
def PRD(chance, curr_trial):
    """Based on pseudo random method, determine whether it is a hit or not.

    :param chance: the nominal chance of hit.
    :param curr_trial: the number of trials from last success
    :return: True or False. True represents a hit and False represents a miss.

    >>> PRD(0.7,3)
    True
    """

    curr_chance = C[chance] * curr_trial
    if rd.random() < curr_chance:
        return True
    return False


def TRD(chance):
    """Based on true random method, determine whether it is a hit or not.

    :param chance: the nominal chance of hit.
    :return: True or False. True represents a hit and False represents a miss.
    """

    return rd.random() < chance


def getPRDSequence(chance, trials):
    """Based on pseudo random method, generate the sequence recording at which times there is a hit.

    :param chance: the nominal chance of hit.
    :param trials: the number of trials in one round.
    :return: a sequence recording the times that hits.
    """

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
    """Based on true random method, generate the sequence recording at which times there is a hit.

    :param chance: the nominal chance of hit.
    :param trials: the number of trials in one round.
    :return: a sequence recording the times that hits.

    >>> getTRDSequence(1,1)
    [1]

    """
    seq = []
    for trial in range(trials):
        if TRD(chance):
            seq.append(trial)
    return seq


def create_graph():
    """Generate two same graphs containing 1000 nodes(players) and 5000 edges(connections).
    Each node has three attribute: active, hit and total trials.

    :param: no parameter.
    :return: two graphs under TRD and PRD method.
    """

    G = random_graphs.dense_gnm_random_graph(1000, 5000)
    for node_index in G.nodes:
        G.nodes[node_index]['active'] = True
        G.nodes[node_index]['hit'] = 0
        G.nodes[node_index]['total_trials'] = 0
    trd_graph = G.copy()
    prd_graph = G.copy()
    return trd_graph, prd_graph


def gen_sequence(G, is_trd):
    """Based on true random method and pseudo random method, calculate the attribute values of nodes,
    but only process nodes that are active.

    :param G: the graph G to be processed.
    :param is_trd: if the graph is under TRD method, then True.
    :return: the graph G already processed.
    """

    if is_trd:
        for node_index in G.nodes:
            if G.nodes[node_index]['active']:
                trd_seq = getTRDSequence(chance, trials)
                length = len(trd_seq)
                G.nodes[node_index]['hit'] += length
                G.nodes[node_index]['total_trials'] += trials
    else:
        for node_index in G.nodes:
            if G.nodes[node_index]['active']:
                prd_seq = getPRDSequence(chance, trials)
                length = len(prd_seq)
                G.nodes[node_index]['hit'] += length
                G.nodes[node_index]['total_trials'] += trials
    return G


def cal_mean_sqr_diff(G):
    """Only process the active nodes' square difference, and calculate the total difference of a
    graph to present its uniformity.

    :param G: the graph G to be processed.
    :return: the graph G already processed, and the total square difference of the graph, which
    represents the uniformity.
    """

    graph_sqr_diff = 0.0
    for node_index in G.nodes:
        if G.nodes[node_index]['active']:
            hit_rate = G.nodes[node_index]['hit'] / G.nodes[node_index]['total_trials'] * 100
            if len(G.adj[node_index]) == 0:
                mean_sqr_diff = 0.0
            else:
                sum_sqr_diff = 0.0
                sum_diff = 0.0
                for nbr_index in G.adj[node_index]:
                    nbr_hit_rate = G.nodes[nbr_index]['hit'] / G.nodes[nbr_index]['total_trials'] * 100
                    sum_sqr_diff += (hit_rate - nbr_hit_rate) ** 2
                    sum_diff += (hit_rate - nbr_hit_rate)
                mean_sqr_diff = sum_sqr_diff / len(G.adj[node_index])
                mean_diff = sum_diff / len(G.adj[node_index])
            G.nodes[node_index]['mean_diff'] = mean_diff
            graph_sqr_diff += mean_sqr_diff
    graph_sqr_diff /= len(G.nodes)
    return G, graph_sqr_diff


def get_decision(mean_diff):
    """Based on specific standards, determine whether a node is active after this round.

    :param mean_diff: the mean difference of a node(player).
    :return: True or False. True means active, and it is still under our consideration next round.

    >>> get_decision(-100)
    False
    >>> get_decision(5)
    True

    """

    if mean_diff > -5:
        return True
    else:
        return False


def decision(G):
    """Based on the decision in get_decision() function, switch the mode of unqualified node from
    active to inactive.

    :param G: the graph G to be processed.
    :return: the graph G after processing, turning nodes whose mean diff is small to inactive.
    """

    for node_index in G.nodes:
        if G.nodes[node_index]['active']:
            G.nodes[node_index]['active'] = get_decision(G.nodes[node_index]['mean_diff'])
    return G


def count_active(G):
    """Count the number of active nodes in one graph.

    :param G: the graph to be counted.
    :return: the number of active nodes n.
    """

    n = 0
    for node_index in G.nodes:
        if G.nodes[node_index]['active']:
            n += 1
    return n


def main():
    (trd_graph, prd_graph) = create_graph()
    for i in range(0,5):
        trd_graph = gen_sequence(trd_graph, True)
        prd_graph = gen_sequence(prd_graph, False)
        (trd_graph, trd_sqr_diff) = cal_mean_sqr_diff(trd_graph)
        (prd_graph, prd_sqr_diff) = cal_mean_sqr_diff(prd_graph)
        trd_graph = decision(trd_graph)
        prd_graph = decision(prd_graph)
        trd_active = count_active(trd_graph)
        prd_active = count_active(prd_graph)
        print("trd graph total diff(uniformity) = ", trd_sqr_diff)
        print("trd retention rate: ", trd_active/1000)
        print("prd graph total diff(uniformity) = ", prd_sqr_diff)
        print("prd retention rate: ", prd_active/1000)

main()