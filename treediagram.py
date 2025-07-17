import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import colorsys
import math
import numpy as np

# Load edges and weights
nodes_df = pd.read_csv("nodes.csv")
edges_df = pd.read_csv("edges2.csv")

# Create directed graph
G = nx.DiGraph()
# for _, row in edges_df.iterrows():
#     G.add_edge(row['source'], row['target'], weight=row['weight'])
for _, row in edges_df.iterrows():
    style = 'solid' if row['line_style'] == 's' else 'dashed'
    G.add_edge(row['source'], row['target'], weight=row['weight'], style=style)


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



weights = [d['weight'] for u, v, d in G.edges(data=True)]

colors = [node_colors.get(n, (0.9, 0.9, 0.9)) for n in G.nodes()]

depths = nx.single_source_shortest_path_length(G, root)

span1= 2
span2= 1

pos= nx.kamada_kawai_layout(G, scale=1.2)
pos[root]= [0,0]
neighbors = list(G.successors(root))
n = len(neighbors)
circle_positions = {}
for i, node in enumerate(neighbors):
    angle = 2 * math.pi * i / n
    x = math.cos(angle) * span1
    y = math.sin(angle) * span1
    pos[node] = (x, y) 

for trunk in list(G.successors(root)):
    for branch in list(G.successors(trunk)):
        pos[branch] = np.array(pos[trunk]) * (2*span1 + span2) + (np.random.rand(2) * 2 - 1) * (2*span2)


PHI = 1.6180339887498948482  # ppl says this is a beautiful number :)
# chatgpt
span1 = 1   # distance from root to trunks
span2 = 0.8   # base distance from trunk to branch
fan_angle = math.radians(180/PHI)  # total fan spread per trunk (in radians)

# Position root
pos = {root: np.array([0, 0])}

# Depth-1: Place trunks in a circle
neighbors = list(G.successors(root))
n = len(neighbors)

for i, trunk in enumerate(neighbors):
    angle = 2 * math.pi * i / n
    trunk_pos = np.array([math.cos(angle), math.sin(angle)]) * span1
    pos[trunk] = trunk_pos

    # Depth-2: Branches of this trunk
    children = list(G.successors(trunk))
    m = len(children)
    if m == 0:
        continue

    # Get direction vector from root → trunk
    direction = trunk_pos / np.linalg.norm(trunk_pos)

    # Create a perpendicular vector for fanning
    perp = np.array([-direction[1], direction[0]])

    for j, child in enumerate(children):
        # Fan branches around the trunk direction
        if m == 1:
            offset = np.array([0.0])  # no spread needed
        else:
            # angle offset from central direction
            theta = -fan_angle / 2 + j * (fan_angle / (m - 1))
            # rotate direction by theta using 2D rotation formula
            #offset = (math.cos(theta) * direction + math.sin(theta) * perp) * span2 * np.random.rand() * PHI/G.edges[(trunk,child)]['weight']
            offset = (math.cos(theta) * direction + math.sin(theta) * perp) * span2 * PHI
        pos[child] = pos[trunk] + offset

# # nx.planar_layout(G)
# nx.draw(G, pos,
#         with_labels=True,
#         node_color=colors,
#         node_size=200,
#         font_weight='bold',
#         font_size=6,
#         width=[w * 8 for w in weights],  # Edge thickness
#         arrows=True)

# with line style
# Separate edges by style
solid_edges = [(v,u) for u, v, d in G.edges(data=True) if d.get('style') == 'solid']
dashed_edges = [(v,u) for u, v, d in G.edges(data=True) if d.get('style') == 'dashed']

# Edge weights
edge_weights = nx.get_edge_attributes(G, 'weight')

# Draw solid edges
plt.margins(0)
nx.draw_networkx_edges(
    G, pos,
    edgelist=solid_edges,
    width=[edge_weights[(v,u)] * 8 for u, v in solid_edges],
    style='solid',
    arrows=True,
    arrowstyle='->',
    edge_color='dimgray',
    connectionstyle='arc3,rad=0.1'
)

nx.draw_networkx_edges(
    G, pos,
    edgelist=dashed_edges,
    width=[edge_weights[(v,u)] * 4 for u, v in dashed_edges],
    style='dashed',
    arrows=True,
    arrowstyle='->',
    edge_color='gray',
    connectionstyle='arc3,rad=0.1'
)


max_depth = max(depths.values())
node_sizes = [200 * (max_depth + 1 - depths[n]) for n in G.nodes()]


# Draw nodes and labels once
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=node_sizes)
nx.draw_networkx_labels(G, pos, font_size=6)


# Draw edge weights
edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=4.5)

#plt.title("Feasibility Tree from CSV (Layers, Colors, Weights)")
plt.axis('off')                           # Turn off the axis
plt.margins(0)                            # Remove margins
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove space around figure
plt.tight_layout(pad=0)  
