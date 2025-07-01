import pandas as pd
import matplotlib as plt

# Load CSV (downloaded from the source)
df = pd.read_csv("tinggibadan6-15.csv")
print(df.head())

df.columns = ["SchoolID", "Grade", "MeanHeight", "BoysHeight", "GirlsHeight"]

grade_avg = df.groupby("Grade").mean(numeric_only=True)

plt.plot(grade_avg.index, grade_avg["MeanHeight"], label="All Students", marker='o')
plt.plot(grade_avg.index, grade_avg["BoysHeight"], label="Boys", linestyle="--", marker='x')
plt.plot(grade_avg.index, grade_avg["GirlsHeight"], label="Girls", linestyle="--", marker='s')
plt.xlabel("Grade")
plt.ylabel("Height (cm)")
plt.title("Average Height by Grade")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Simulate raw students based on school-level means and stds
import numpy as np
raw_heights = []

for _, row in df.iterrows():
    n_students = 60  # or pull actual sample size if available
    # Simulate from boys/girls height average with small variation
    for _ in range(n_students // 2):
        raw_heights.append([row["Grade"], np.random.normal(row["BoysHeight"], 2.0)])
        raw_heights.append([row["Grade"], np.random.normal(row["GirlsHeight"], 2.0)])

raw_data = np.array(raw_heights)
X = raw_data[:, 1].reshape(-1, 1)  # only the height column
grades = raw_data[:, 0].astype(int)


# heights at HMM states


from hmmlearn import hmm

model = hmm.GaussianHMM(n_components=6, covariance_type="diag", n_iter=100)
model.fit(X)
hidden_states = model.predict(X)

plt.figure(figsize=(10, 6))
plt.scatter(grades + np.random.normal(0, 0.1, len(grades)), X.flatten(), c=hidden_states, cmap='tab10', alpha=0.6)
plt.xlabel("Grade")
plt.ylabel("Student Height (cm)")
plt.title("Height by Grade with HMM-Inferred Hidden States")
plt.colorbar(label="HMM State")
plt.grid(True)
plt.tight_layout()
plt.show()


import networkx as nx

def plot_hmm_graph(model):
    G = nx.DiGraph()

    # Add nodes
    for i in range(model.n_components):
        G.add_node(i, label=f"Grade~State {i}")

    # Add edges based on transition probabilities
    for i in range(model.n_components):
        for j in range(model.n_components):
            prob = model.transmat_[i, j]
            if prob > 0.01:
                G.add_edge(i, j, weight=prob)

    pos = nx.spring_layout(G, seed=42)
    edge_labels = { (i, j): f"{prob:.2f}" for i, j, prob in G.edges(data='weight') }

    plt.figure(figsize=(6, 5))
    nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=1200)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("HMM State Transition Graph (Grade Progression)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

plot_hmm_graph(model)

#------ GMM

from sklearn.mixture import GaussianMixture

gmm = GaussianMixture(n_components=4)
gmm.fit(X)
labels = gmm.predict(X)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(grades + np.random.normal(0, 0.1, len(grades)), X.flatten(), c=labels, cmap='tab10', alpha=0.6)
plt.xlabel("Grade")
plt.ylabel("Student Height (cm)")
plt.title("Student Height Clusters by GMM")
plt.grid(True)
plt.colorbar(label="GMM Cluster")
plt.tight_layout()
plt.show()



