##AI Energy Audit Agent (Python Code)
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime
import random

class EnergyAuditAgent:
    def __init__(self, energy_data):
        self.energy_data = energy_data
        self.model = IsolationForest(contamination=0.05, random_state=42)  # 5% anomaly threshold

    def train_model(self):
        X = self.energy_data[['power_usage_kW', 'temperature_C', 'humidity', 'operating_hours']]
        self.model.fit(X)

    def detect_anomalies(self, power_usage, temperature, humidity, operating_hours):
        anomaly_score = self.model.decision_function([[power_usage, temperature, humidity, operating_hours]])[0]
        is_anomaly = self.model.predict([[power_usage, temperature, humidity, operating_hours]])[0]
        return "Anomaly Detected" if is_anomaly == -1 else "Normal", anomaly_score

    def recommend_energy_savings(self, power_usage, avg_power, device_type):
        if power_usage > avg_power * 1.2:  # 20% higher than avg
            if device_type == "Motor":
                return "Replace with energy-efficient motor (IE3/IE4 standard)"
            elif device_type == "HVAC":
                return "Optimize HVAC settings or upgrade to a smart HVAC system"
            elif device_type == "Lighting":
                return "Switch to LED lighting with motion sensors"
        return "No action needed"

# Sample IoT Sensor Data (for training)
data = pd.DataFrame({
    'power_usage_kW': [50, 60, 55, 70, 100, 90, 300],  # Last value is an anomaly
    'temperature_C': [22, 23, 24, 25, 26, 27, 30],
    'humidity': [40, 42, 44, 45, 50, 55, 65],
    'operating_hours': [8, 9, 10, 12, 14, 16, 24]
})

# Initialize AI Agent
agent = EnergyAuditAgent(data)
agent.train_model()

# Simulated IoT Sensor Inputs
power_usage = 300  # kW (possible anomaly)
temperature = 30  # °C
humidity = 65  # %
operating_hours = 24  # hrs
device_type = "Motor"

# Get AI Detection & Recommendations
anomaly_status, anomaly_score = agent.detect_anomalies(power_usage, temperature, humidity, operating_hours)
recommendation = agent.recommend_energy_savings(power_usage, data['power_usage_kW'].mean(), device_type)

print(f"Anomaly Status: {anomaly_status} (Score: {anomaly_score:.4f})")
print(f"Energy Saving Recommendation: {recommendation}")
