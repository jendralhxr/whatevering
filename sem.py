import pandas as pd
import numpy as np
from semopy import Model
import networkx as nx
import matplotlib.pyplot as plt

# Latent variable Health affects:
#     PhysicalActivity
#     MentalWellBeing
# Observed variable DietQuality affects:
#     PhysicalActivity
# Latent variable Health indirectly affects MentalWellBeing through PhysicalActivity.

# Generate synthetic dataset
np.random.seed(42)
n = 200
data = pd.DataFrame({
    "PhysicalActivity": np.random.normal(size=n),
    "MentalWellBeing": np.random.normal(size=n),
    "DietQuality": np.random.normal(size=n),
})
data["Health"] = 0.6 * data["PhysicalActivity"] + 0.4 * data["MentalWellBeing"] + np.random.normal(scale=0.2, size=n)
data["PhysicalActivity"] += 0.6 * data["DietQuality"] + np.random.normal(scale=0.1, size=n)
data["MentalWellBeing"] += 0.7 * data["PhysicalActivity"] + np.random.normal(scale=0.1, size=n)

# Define SEM model
model_desc = """
    Health =~ PhysicalActivity + MentalWellBeing
    DietQuality ~ PhysicalActivity
    PhysicalActivity ~~ MentalWellBeing
"""

# Fit the model
model = Model(model_desc)
model.fit(data)

# Extract relationships and coefficients from the model
results = model.inspect()

# Initialize a directed graph
G = nx.DiGraph()

# Add edges based on the fitted model
for _, row in results.iterrows():
    from_node = row['lval']  # Left-hand side variable
    to_node = row['rval']    # Right-hand side variable
    if row['op'] in ['~', '=~']:  # Include regressions and loadings
        label = f"{row['Estimate']:.2f}"  # Coefficient as edge label
        G.add_edge(from_node, to_node, label=label)

# Draw the graph
plt.figure(figsize=(10, 6))
pos = nx.kamada_kawai_layout(G)  # Layout for the graph
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'))
plt.title("SEM Model Visualization")
plt.show()
