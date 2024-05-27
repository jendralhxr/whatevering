import networkx as nx
import matplotlib.pyplot as plt

def draw_multidigraph_with_edge_labels(G, pos=None):
    # If no position is provided, use a spring layout
    if pos is None:
        pos = nx.spring_layout(G)
    
    # Draw the graph nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold', arrows=True)
    
    # Draw edge labels manually
    for (u, v, key, data) in G.edges(data=True, keys=True):
        # Get the midpoint for the edge
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        x_mid = (x1 + x2) / 2
        y_mid = (y1 + y2) / 2
        
        # Adjust label position slightly to avoid overlap
        if u == v:  # Self-loop
            plt.text(x_mid, y_mid, f"{data['label']}", fontsize=12, color='red')
        else:
            plt.text(x_mid, y_mid, f"{data['label']}", fontsize=12, color='red', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Display the graph
    plt.show()

# Example usage
G = nx.MultiDiGraph()
G.add_edge(1, 2, key='a', weight=3, label='A')
G.add_edge(2, 1, key='b', weight=4, label='B')
G.add_edge(2, 3, key='c', weight=5, label='C')
G.add_edge(3, 2, key='d', weight=2, label='D')
G.add_edge(3, 4, key='e', weight=6, label='E')
G.add_edge(4, 3, key='f', weight=1, label='F')

draw_multidigraph_with_edge_labels(G)
