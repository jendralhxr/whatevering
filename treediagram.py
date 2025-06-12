#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 19:03:04 2025

@author: rdx
"""

import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges for a 3-tier tree
G.add_edge("Kelayakan", "Child1")
G.add_edge("Kelayakan", "Child2")

G.add_edge("Child1", "Child1.1")
G.add_edge("Child1", "Child1.2")
G.add_edge("Child2", "Child2.1")
G.add_edge("Child2", "Child2.2")

# Use graphviz layout for better tree appearance
pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

# Draw the graph
nx.draw(G, pos, with_labels=True, arrows=True, node_size=2000, node_color="lightblue", font_size=10)
plt.title("3-Tier Tree Diagram")
plt.show()



#-0


import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes with 'layer' attribute (tier level)
G.add_node("Root", layer=0)
G.add_node("Child1", layer=1)
G.add_node("Child2", layer=1)
G.add_node("Child1.1", layer=2)
G.add_node("Child1.2", layer=2)
G.add_node("Child2.1", layer=2)
G.add_node("Child2.2", layer=2)

# Add edges
edges = [
    ("Root", "Child1"), ("Root", "Child2"),
    ("Child1", "Child1.1"), ("Child1", "Child1.2"),
    ("Child2", "Child2.1"), ("Child2", "Child2.2")
]
G.add_edges_from(edges)

# Use multipartite layout
pos = nx.multipartite_layout(G, subset_key="layer")
pos = {node: (y, -x) for node, (x, y) in pos.items()}


# Draw graph
nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=2000, arrows=True)
plt.title("3-Tier Tree Diagram using multipartite_layout")
plt.show()

#-----

import networkx as nx
import matplotlib.pyplot as plt
import colorsys

# Create a directed graph
G = nx.DiGraph()

# Tree structure with parent-child relationships
tree_structure = {
    "Root": ["Child1", "Child2"],
    "Child1": ["Child1.1", "Child1.2"],
    "Child2": ["Child2.1", "Child2.2"]
}

# Track layers (for layout)
layer_map = {"Root": 0}

# Build graph and assign layer depth
for parent, children in tree_structure.items():
    for child in children:
        G.add_edge(parent, child)
        layer_map[child] = layer_map[parent] + 1

# Assign colors by branch
branches = list(tree_structure["Root"])  # Child1, Child2
branch_colors = {}

# Assign a base hue to each root branch
for i, branch in enumerate(branches):
    hue = i / len(branches)  # 0.0, 0.5 for 2 branches
    base_color = colorsys.hsv_to_rgb(hue, 0.6, 1.0)
    branch_colors[branch] = base_color

# Generate node colors
node_colors = {}
node_colors["Root"] = (0.2, 0.2, 0.2)  # root is dark gray

def get_color(branch, depth):
    base = branch_colors[branch]
    factor = 1 - (depth * 0.3)
    return tuple(factor * c for c in base)

# Assign colors to all nodes
for branch in branches:
    node_colors[branch] = branch_colors[branch]
    for child in tree_structure[branch]:
        depth = layer_map[child]
        node_colors[child] = get_color(branch, depth)

# Layout (multipartite, then flipped to vertical)
for node in G.nodes:
    G.nodes[node]["layer"] = layer_map[node]

pos = nx.multipartite_layout(G, subset_key="layer")
pos = {node: (y, -x) for node, (x, y) in pos.items()}

# Draw graph
colors = [node_colors[n] for n in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2000, font_weight='bold', arrows=True)
plt.title("Fancy 3-Tier Tree Diagram (Hue by Branch, Darkness by Depth)")
plt.show()
