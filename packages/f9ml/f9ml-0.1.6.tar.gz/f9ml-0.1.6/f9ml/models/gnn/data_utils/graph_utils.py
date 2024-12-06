import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from torch_geometric.utils.convert import from_scipy_sparse_matrix


def graph_feynman_diagram(node_names_lst, feynman_node_dct, draw=False, keep_names_for_draw=False):
    if type(node_names_lst) is not list:
        node_names_lst = list(node_names_lst)

    node_dct = {}

    for k, v in feynman_node_dct.items():
        idx = node_names_lst.index(k)
        node_dct[idx] = []
        for i in v:
            node_dct[idx].append(node_names_lst.index(i))

    if keep_names_for_draw:
        node_dct = feynman_node_dct

    G = nx.DiGraph()

    for node, neighbors in node_dct.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    if draw:
        pos = nx.nx_pydot.pydot_layout(G, prog="dot")
        # Visualize the directed graph as a tree
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", arrows=True)
        plt.savefig("ml/gnn/data_utils/feynman_diagram.png")
        return None

    A = nx.adjacency_matrix(G, nodelist=sorted(G.nodes()))
    edge_indices, _ = from_scipy_sparse_matrix(A)

    return edge_indices.numpy().astype(np.int64)


def digraph_to_nx(x, edge_indices, graph_builder_obj, edge_attributes=None, data_idx=0, draw=False):
    G = nx.DiGraph()

    node_names = list(graph_builder_obj.node_names)
    node_feature_names = list(graph_builder_obj.node_features)

    node_attr = x[data_idx, :, :]
    if edge_attributes:
        edge_attr = edge_attributes[data_idx, :, :]

    for n in node_names:
        G.add_node(n)

    i_idx, j_idx = edge_indices[data_idx, 0, :], edge_indices[data_idx, 1, :]

    for i, j in zip(i_idx, j_idx):
        G.add_edge(node_names[i], node_names[j])

    dup_node_feature_names, check = [], []
    for name in node_feature_names:
        if name not in check:
            dup_node_feature_names.append(name + "_0")
        else:
            dup_node_feature_names.append(name + "_" + str(check.count(name)))

        check.append(name)

    for n_i, n in enumerate(node_names):
        for f_i, f in enumerate(dup_node_feature_names):
            if f in G._node[n].keys():
                G._node[n][f"{f}_"] = node_attr[n_i, f_i]
            else:
                G._node[n][f] = node_attr[n_i, f_i]

    if edge_attributes:
        node_i_idx, node_j_idx = edge_indices[data_idx, 0, :], edge_indices[data_idx, 1, :]
        edge_attr_names = graph_builder_obj.selection[graph_builder_obj.selection["node"] == "edge"]["feature"].values

        for c, (i, j) in enumerate(zip(node_i_idx, node_j_idx)):
            e_dct = {}
            for e, e_name in enumerate(edge_attr_names):
                e_dct[e_name] = edge_attr[c, e]

            G.add_edge(node_names[i], node_names[j], **e_dct)

    if draw:
        if graph_builder_obj.connection_type == "all_to_all":
            nx.draw_circular(
                G,
                with_labels=True,
                node_shape="s",
                node_color="none",
                node_size=1000,
                bbox=dict(facecolor="skyblue", edgecolor="black", boxstyle="round, pad=0.2"),
            )
        elif graph_builder_obj.connection_type == "feynman":
            pos = nx.nx_pydot.pydot_layout(G, prog="dot")
            nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", arrows=True)
        else:
            raise NotImplementedError

        plt.savefig("ml/gnn/data_utils/digraph.png")

    return G, {"nodes": dict(G.nodes(data=True)), "edges": list(G.edges(data=True))}
