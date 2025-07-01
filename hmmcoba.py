import numpy as np
from hmmlearn import hmm
import networkx as nx
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Create a Gaussian HMM with 3 hidden states
model = hmm.GaussianHMM(n_components=3, covariance_type="diag", n_iter=100)

# Simulated training data (1D observations)
X = np.concatenate([
    np.random.normal(0, 1, (100, 1)),
    np.random.normal(5, 1, (100, 1)),
    np.random.normal(10, 1, (100, 1))
])

model.fit(X)

# Decode the hidden states
hidden_states = model.predict(X)

print("Transition matrix:")
print(model.transmat_)
print("Means and variances of each hidden state:")
for i in range(model.n_components):
    mean = float(model.means_[i][0])
    var = float(model.covars_[i][0])
    print(f"{i}: mean = {mean:.2f}, variance = {var:.2f}")

def plot_hmm_graph(model):
    G = nx.DiGraph()

    # Add nodes
    for i in range(model.n_components):
        G.add_node(i, label=f"State {i}")

    # Add weighted edges from transition matrix
    for i in range(model.n_components):
        for j in range(model.n_components):
            prob = model.transmat_[i, j]
            if prob > 0.01:  # Ignore tiny transitions
                G.add_edge(i, j, weight=prob)

    # Draw the graph
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f"{v:.2f}" for k, v in edge_labels.items()}

    plt.figure(figsize=(6, 5))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Hidden Markov Model State Transition Graph")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Visualize the graph
plot_hmm_graph(model)

