import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()

# Add some nodes and edges
G.add_edges_from([(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 3)])

# Function to find all possible paths between two nodes
def find_all_paths(graph, start_node, end_node):
    try:
        # Use the all_simple_paths function to find all simple paths
        all_paths = list(nx.all_simple_paths(graph, source=start_node, target=end_node))
        return all_paths
    except nx.NetworkXNoPath:
        return "No path exists between the two nodes."

# Example usage
start = 1
end = 3
all_paths = find_all_paths(G, start, end)

# Draw the graph with thicker edges for paths
pos = nx.spring_layout(G)  # Position nodes using spring layout

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue')

# Draw edges
nx.draw_networkx_edges(G, pos)

# Draw each path with thicker edges
for path in all_paths:
    nx.draw_networkx_edges(G, pos, edgelist=[(path[j], path[j + 1]) for j in range(len(path) - 1)], width=3)

# Add labels
nx.draw_networkx_labels(G, pos)

# Display the graph
plt.axis('off')
plt.show()
