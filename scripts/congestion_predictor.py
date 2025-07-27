# Hybrid prediction model (save as congestion_predictor.py)
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd

class CongestionPredictor:
    def __init__(self):
        self.model = GradientBoostingRegressor()
        self.features = ["hour", "is_peak", "weather", "prev_speed"]
        
    def train(self, data_file="congestion_log.csv"):
        data = pd.read_csv(data_file)
        X = data[self.features]
        y = data["speed"]
        self.model.fit(X, y)
        
    def predict(self, current_state):
        return self.model.predict([current_state])