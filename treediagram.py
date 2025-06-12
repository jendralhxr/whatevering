import networkx as nx
import matplotlib.pyplot as plt
import colorsys
import random

# Create a directed graph
G = nx.DiGraph()

# Tree structure with parent-child relationships
tree_structure = {
    "Feasibility": ["Spatial Planning", "Technical Aspects", "Economics, Finance, Costs", "Environment", "Navigational Safety"],
    "Spatial Planning": ["Child1.1", "Child1.2"],
    "Technical Aspects": ["Child2.1", "Child2.2"],
    "Economics, Finance, Costs": ["Child3.1", "Child3.2"],
    "Environment": ["Child4.1", "Child4.2"],
    "Navigational Safety": ["Child5.1", "Child5.2"]
}

# Track layers (for layout)
layer_map = {"Feasibility": 0}

# Build graph and assign layer depth
for parent, children in tree_structure.items():
    for child in children:
        G.add_edge(parent, child, weight=round(random.uniform(0, 1), 2))  # Random weight
        layer_map[child] = layer_map[parent] + 1

# Assign colors by branch
branches = list(tree_structure["Feasibility"])
branch_colors = {}

for i, branch in enumerate(branches):
    hue = i / len(branches)
    base_color = colorsys.hsv_to_rgb(hue, 0.4, 1.0)
    branch_colors[branch] = base_color

# Generate node colors
node_colors = {"Feasibility": (0.6, 0.6, 0.6)}

def get_color(branch, depth):
    base = branch_colors[branch]
    factor = 1 - (depth * 0.15)
    return tuple(factor * c for c in base)

for branch in branches:
    node_colors[branch] = branch_colors[branch]
    for child in tree_structure[branch]:
        depth = layer_map[child]
        node_colors[child] = get_color(branch, depth)

# Add layer attribute for layout
for node in G.nodes:
    G.nodes[node]["layer"] = layer_map[node]

# Layout and scale for spacing
pos = nx.multipartite_layout(G, subset_key="layer")
pos = {node: (y * 4, -x * 3) for node, (x, y) in pos.items()}  # Spread out horizontally and vertically

# Draw graph
colors = [node_colors[n] for n in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2500, font_weight='bold', arrows=True)

# Draw edge weights
edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9)

plt.title("Tidier 3-Tier Tree with Colored Branches and Edge Weights")
plt.tight_layout()
plt.show()

#----

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
    G.add_edge(row['target'], row['source'], weight=row['weight'])

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

# Generate layout
pos = nx.multipartite_layout(G, subset_key="layer")
pos = {node: (y * 4, -x * 3) for node, (x, y) in pos.items()}

# Draw graph
colors = [node_colors.get(n, (0.9, 0.9, 0.9)) for n in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2500, font_weight='bold', font_size=8, arrows=True)

# Draw edge weights
edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9)

plt.title("Feasibility Tree from CSV (Layers, Colors, Weights)")
plt.tight_layout()
plt.show()
