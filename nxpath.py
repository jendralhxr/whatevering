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

# ------------------

import networkx as nx

# Create a graph with mesh complex edges
G = nx.Graph()

# Add some nodes and edges
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (2, 5), (5, 6), (6, 3), (3, 7), (7, 8), (8, 5)])

# Function to delete edges shorter than a given threshold
def delete_short_edges(graph, threshold):
    edges_to_remove = []
    for edge in graph.edges():
        if nx.shortest_path_length(graph, source=edge[0], target=edge[1]) < threshold:
            edges_to_remove.append(edge)
    graph.remove_edges_from(edges_to_remove)

# Example usage
threshold = 3
delete_short_edges(G, threshold)

# Print remaining edges
print("Remaining Edges:", G.edges())

#-------


def remove_short_paths(G, hops):
    paths_to_remove = []
    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                paths = list(nx.all_simple_paths(G, source, target))
                for path in paths:
                    if len(path) < hops:
                        paths_to_remove.append(path)
    for path in paths_to_remove:
        G.remove_edges_from(zip(path[:-1], path[1:]))
    isolated_nodes = list(nx.isolates(G))
    G.remove_nodes_from(isolated_nodes)
    
    #-----
    
    import networkx as nx

def remove_short_paths(G, threshold):
    # Identify all simple paths and their lengths
    all_paths = []
    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                paths = nx.all_simple_paths(G, source, target)
                all_paths.extend(paths)
    
    # Group paths by their start and end nodes
    paths_by_start_end = {}
    for path in all_paths:
        start, end = path[0], path[-1]
        if (start, end) not in paths_by_start_end:
            paths_by_start_end[(start, end)] = []
        paths_by_start_end[(start, end)].append(path)
    
    # Keep only the longest path for each start-end pair
    longest_paths = [max(paths, key=len) for paths in paths_by_start_end.values()]
    
    # Remove short paths while preserving the longer branches
    for path in longest_paths:
        for u, v in zip(path[:-1], path[1:]):
            if G.has_edge(u, v):
                G[u][v]['keep'] = True
    
    for u, v, attrs in G.edges(data=True):
        if 'keep' not in attrs:
            G.remove_edge(u, v)
        else:
            del attrs['keep']
    
    # Remove isolated nodes
    isolated_nodes = list(nx.isolates(G))
    G.remove_nodes_from(isolated_nodes)

# Example usage:
G = nx.Graph()
# Add nodes and edges to the graph...

threshold = 4  # Set your threshold here

# Call the function to remove paths shorter than the threshold
remove_short_paths(G, threshold)
