## AI Agent for Smart Lighting & HVAC (Python Code)
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import random

class SmartLightingHVACAgent:
    def __init__(self, sensor_data):
        self.sensor_data = sensor_data
        self.hvac_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.lighting_model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train_models(self):
        # Train HVAC model
        X_hvac = self.sensor_data[['temperature_C', 'humidity', 'occupancy']]
        y_hvac = self.sensor_data['hvac_power_kW']
        self.hvac_model.fit(X_hvac, y_hvac)

        # Train lighting model
        X_lighting = self.sensor_data[['ambient_light', 'occupancy']]
        y_lighting = self.sensor_data['lighting_power_kW']
        self.lighting_model.fit(X_lighting, y_lighting)

    def optimize_hvac(self, temperature, humidity, occupancy):
        predicted_hvac_power = self.hvac_model.predict([[temperature, humidity, occupancy]])[0]
        return max(0.5, min(predicted_hvac_power, 5.0))  # Keep within reasonable range

    def adjust_lighting(self, ambient_light, occupancy):
        if occupancy == 0:
            return 0  # Turn off lights if no one is present
        predicted_lighting_power = self.lighting_model.predict([[ambient_light, occupancy]])[0]
        return max(0.5, min(predicted_lighting_power, 3.0))  # Adjust brightness

# Sample Sensor Data for Training
data = pd.DataFrame({
    'temperature_C': [22, 24, 26, 28, 30, 32],
    'humidity': [40, 45, 50, 55, 60, 65],
    'occupancy': [1, 1, 1, 0, 0, 1],
    'hvac_power_kW': [2, 2.5, 3, 1, 0.5, 3.2],
    'ambient_light': [300, 250, 200, 100, 50, 400],
    'lighting_power_kW': [2, 1.5, 1, 0.5, 0, 2.5]
})

# Initialize AI Agent
agent = SmartLightingHVACAgent(data)
agent.train_models()

# Simulated Sensor Inputs
temperature = 27  # °C
humidity = 50  # %
occupancy = 1  # 1 = Room Occupied, 0 = Empty
ambient_light = 150  # Light intensity in Lux

# Get AI-Driven Optimizations
optimized_hvac = agent.optimize_hvac(temperature, humidity, occupancy)
adjusted_lighting = agent.adjust_lighting(ambient_light, occupancy)

print(f"Optimized HVAC Power Consumption: {optimized_hvac:.2f} kW")
print(f"Adjusted Lighting Power Consumption: {adjusted_lighting:.2f} kW")
