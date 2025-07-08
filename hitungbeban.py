import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ---- Fake Dataset Setup ----
# Features: time, weather, speed, light level
# Labels (multi-label): [fatigue, speeding, alcohol, weather, lighting]

np.random.seed(0)
n_samples = 100

# Random input features (you would replace this with real ones)
X = pd.DataFrame({
    'hour': np.random.randint(0, 24, n_samples),
    'weather': np.random.randint(0, 3, n_samples),   # 0: clear, 1: rain, 2: fog
    'speed': np.random.normal(60, 15, n_samples),
    'light': np.random.randint(0, 2, n_samples),     # 0: day, 1: night
})

# Simulate multi-label targets
Y = pd.DataFrame({
    'fatigue': (X['hour'] > 22).astype(int),
    'speeding': (X['speed'] > 70).astype(int),
    'alcohol': (X['hour'] > 20).astype(int) & (X['light'] == 1),
    'weather_related': (X['weather'] != 0).astype(int),
    'poor_lighting': (X['light'] == 1).astype(int),
})

# ---- Train/Test Split ----
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# ---- Model Setup ----
forest = RandomForestClassifier(n_estimators=100, random_state=42)
multi_target_forest = MultiOutputClassifier(forest)

# ---- Training ----
multi_target_forest.fit(X_train, Y_train)

# ---- Prediction ----
Y_pred = multi_target_forest.predict(X_test)

# ---- Evaluation ----
print(classification_report(Y_test, Y_pred, target_names=Y.columns))
