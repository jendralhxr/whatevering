import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import colorsys

# Load edges and weights
nodes_df = pd.read_csv("nodes.csv")
edges_df = pd.read_csv("edges.csv")

# Create directed graph
G = nx.DiGraph()

# Add edges with weights
for _, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

# Assign layer info
layer_map = dict(zip(nodes_df["node"], nodes_df["layer"]))
nx.set_node_attributes(G, layer_map, "layer")

# Get branches (first-level children of the root)
root = "Feasibility"
branches = list(G.successors(root))

# Assign colors by branch (HSV)
branch_colors = {}
for i, branch in enumerate(branches):
    hue = i / len(branches)
    base_rgb = colorsys.hsv_to_rgb(hue, 0.4, 1.0)
    branch_colors[branch] = base_rgb

# Assign node colors
node_colors = {}
node_colors[root] = (0.6, 0.6, 0.6)  # root = gray

def get_color(branch, depth):
    base = branch_colors.get(branch, (0.8, 0.8, 0.8))
    darken = 1 - (depth * 0.15)
    return tuple(darken * c for c in base)

# Assign colors recursively
for branch in branches:
    node_colors[branch] = branch_colors[branch]
    for child in G.successors(branch):
        depth = layer_map[child]
        node_colors[child] = get_color(branch, depth)


colors = [node_colors.get(n, (0.9, 0.9, 0.9)) for n in G.nodes()]

weights = [d['weight'] for u, v, d in G.edges(data=True)]

#pos = nx.multipartite_layout(G, subset_key="layer")
# pos = {node: (y * 4, -x * 3) for node, (x, y) in pos.items()}
pos = nx.kamada_kawai_layout(G, scale=100)


nx.draw(G, nx.planar_layout(G),
        with_labels=True,
        node_color=colors,
        node_size=200,
        font_weight='bold',
        font_size=8,
        width=[w * 10 for w in weights],  # Edge thickness
        arrows=True)


# Draw graph
# nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2500, font_weight='bold', font_size=8, arrows=False)

# Draw edge weights
edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9)

#plt.title("Feasibility Tree from CSV (Layers, Colors, Weights)")
plt.tight_layout()
plt.show()
