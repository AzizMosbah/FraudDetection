import networkx as nx
import matplotlib.pyplot as plt


def entries_to_remove(entries, the_dict):
    for key in entries:
        if key in the_dict:
            del the_dict[key]


def generate_tripartite(df, s0='deviceId', s1='user_id', s2='credit_card_id', min_deg=2):
    B = nx.Graph()
    B.add_nodes_from(df[s0], bipartite=0)
    B.add_nodes_from(df[s1], bipartite=1)
    B.add_nodes_from(df[s2], bipartite=2)

    B.add_edges_from(
        [(row[s1], row[s2]) for idx, row in df.iterrows()])
    B.add_edges_from(
        [(row[s0], row[s1]) for idx, row in df.iterrows()])

    plt.figure(figsize=(40, 30))

    pos = {node: [0, i] for i, node in enumerate(df[s0])}
    pos.update({node: [1, i] for i, node in enumerate(df[s1])})
    pos.update({node: [2, i] for i, node in enumerate(df[s2])})

    deg = dict(B.degree())
    to_remove = [n for n in list(deg.keys()) if deg[n] <= min_deg and 'id' not in n]

    entries_to_remove(to_remove, deg)

    B.remove_nodes_from(to_remove)

    nx.draw(B, pos, with_labels=False, edge_color='grey', width=0.5, alpha=0.8,
            node_size=[v * 100 for v in deg.values()])
    for p in pos:  # raise text positions
        pos[p][1] += 0.25

    plt.title('{0} to {1} to {2}'.format(s0, s1, s2), fontsize=50)

    return B
