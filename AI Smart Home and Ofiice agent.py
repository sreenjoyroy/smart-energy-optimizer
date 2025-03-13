###📌 AI Smart Home & Office Agent (Python Code)
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import requests
from datetime import datetime
import time

class SmartHomeAgent:
    def __init__(self, energy_data):
        self.energy_data = energy_data
        self.thermostat_model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train_model(self):
        X = self.energy_data[['occupancy', 'outside_temp', 'time_of_day']]
        y = self.energy_data['energy_consumption']
        self.thermostat_model.fit(X, y)

    def predict_energy_usage(self, occupancy, outside_temp, time_of_day):
        return self.thermostat_model.predict([[occupancy, outside_temp, time_of_day]])[0]

    def optimize_hvac(self, current_temp, occupancy, outside_temp):
        def objective(temp):
            predicted_usage = self.predict_energy_usage(occupancy, outside_temp, temp)
            return predicted_usage

        optimized_temp = np.clip(np.mean([outside_temp, 22]), 18, 26)  # Keep within 18-26°C range
        return optimized_temp

    def control_lights(self, motion_detected):
        return "ON" if motion_detected else "OFF"

    def adjust_blinds(self, sunlight_level):
        if sunlight_level > 75:  # Too much sunlight
            return "CLOSE BLINDS"
        elif sunlight_level < 25:  # Low sunlight
            return "OPEN BLINDS"
        else:
            return "ADJUST BLINDS PARTIALLY"

# Sample IoT Sensor Data
data = pd.DataFrame({
    'occupancy': [10, 30, 50, 20, 5],
    'outside_temp': [30, 28, 25, 20, 18],
    'time_of_day': [10, 12, 14, 18, 22],
    'energy_consumption': [500, 700, 600, 550, 400]
})

# Initialize AI Agent
agent = SmartHomeAgent(data)
agent.train_model()

# Simulated Inputs from IoT Sensors
current_temp = 22
occupancy = 40
outside_temp = 27
motion_detected = True
sunlight_level = 80  # High sunlight

# Get AI-Optimized Outputs
optimized_hvac_temp = agent.optimize_hvac(current_temp, occupancy, outside_temp)
light_status = agent.control_lights(motion_detected)
blinds_action = agent.adjust_blinds(sunlight_level)

print(f"Optimized HVAC Temperature: {optimized_hvac_temp:.2f}°C")
print(f"Light Status: {light_status}")
print(f"Blinds Adjustment: {blinds_action}")
