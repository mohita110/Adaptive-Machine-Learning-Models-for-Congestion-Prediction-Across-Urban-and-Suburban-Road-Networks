import pandas as pd
from model_definitions import HybridCongestionPredictor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from joblib import dump
import os

class HybridCongestionPredictor:
    def __init__(self):
        self.rf = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
        self.nn = MLPRegressor(hidden_layer_sizes=(32,16), max_iter=500, random_state=42)
        self.scaler = StandardScaler()
    
    def preprocess(self, urban_path, suburban_path):
        urban = pd.read_csv(urban_path)
        suburban = pd.read_csv(suburban_path)
        
        urban['area_type'] = 1  # Urban
        suburban['area_type'] = 0  # Suburban
        
        combined = pd.concat([urban, suburban])
        combined['hour'] = pd.to_datetime(combined['timestamp']).dt.hour
        combined['is_peak'] = ((combined['hour'] >= 7) & (combined['hour'] <= 9)) | \
                             ((combined['hour'] >= 17) & (combined['hour'] <= 19))
        
        features = combined[['vehicle_count', 'avg_speed_kmh', 'area_type', 'hour', 'is_peak']]
        self.scaler.fit(features)
        
        return combined

    def train(self, X, y):
        X_scaled = self.scaler.transform(X)
        self.rf.fit(X_scaled, y)
        self.nn.fit(X_scaled, y)

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return 0.6*self.rf.predict(X_scaled) + 0.4*self.nn.predict(X_scaled)

# Train and save models
predictor = HybridCongestionPredictor()
data = predictor.preprocess("../output/urban_traffic.csv", "../output/suburban_traffic.csv")

X = data[['vehicle_count', 'avg_speed_kmh', 'area_type', 'hour', 'is_peak']]
y = data['waiting_time_sec']

predictor.train(X, y)
os.makedirs("../models", exist_ok=True)
dump(predictor, "../models/hybrid_predictor.joblib")
print("Model trained and saved successfully")