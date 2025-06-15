# utils.py

import joblib
import pandas as pd

def load_model(path="model_knn.pkl"):
    return joblib.load(path)

def get_leaderboard(path="score.csv"):
    try:
        return pd.read_csv(path).sort_values(by="Skor", ascending=False).head(10)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nama", "Sekolah", "Skor"])
