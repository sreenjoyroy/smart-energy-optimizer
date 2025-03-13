##AI Renewable Energy Integration Agent (Python Code)
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import requests

class RenewableEnergyAgent:
    def __init__(self, energy_data):
        self.energy_data = energy_data
        self.solar_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.wind_model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train_models(self):
        # Train solar energy prediction model
        X_solar = self.energy_data[['sunlight_hours', 'temperature', 'humidity']]
        y_solar = self.energy_data['solar_energy']
        self.solar_model.fit(X_solar, y_solar)

        # Train wind energy prediction model
        X_wind = self.energy_data[['wind_speed', 'air_pressure', 'temperature']]
        y_wind = self.energy_data['wind_energy']
        self.wind_model.fit(X_wind, y_wind)

    def predict_solar_energy(self, sunlight_hours, temperature, humidity):
        return self.solar_model.predict([[sunlight_hours, temperature, humidity]])[0]

    def predict_wind_energy(self, wind_speed, air_pressure, temperature):
        return self.wind_model.predict([[wind_speed, air_pressure, temperature]])[0]

    def optimize_battery_storage(self, solar_output, wind_output, current_demand, battery_capacity):
        total_energy = solar_output + wind_output
        excess_energy = total_energy - current_demand

        if excess_energy > 0:
            stored_energy = min(excess_energy, battery_capacity)  # Store in battery
            grid_supply = excess_energy - stored_energy  # Feed remaining to grid
        else:
            stored_energy, grid_supply = 0, 0  # No excess energy

        return stored_energy, grid_supply

    def adjust_solar_panel_angle(self, sun_elevation_angle):
        optimal_angle = max(15, min(sun_elevation_angle, 75))  # Keep within 15° - 75°
        return optimal_angle

# Sample Renewable Energy Data (IoT + Weather API)
data = pd.DataFrame({
    'sunlight_hours': [8, 10, 12, 6, 4],
    'temperature': [30, 28, 25, 20, 18],
    'humidity': [40, 45, 50, 60, 65],
    'solar_energy': [500, 700, 900, 400, 200],
    'wind_speed': [10, 12, 15, 8, 5],
    'air_pressure': [1012, 1010, 1008, 1015, 1020],
    'wind_energy': [300, 400, 500, 200, 100]
})

# Initialize AI Agent
agent = RenewableEnergyAgent(data)
agent.train_models()

# Simulated Inputs from IoT & Weather API
sunlight_hours = 9
temperature = 27
humidity = 50
wind_speed = 14
air_pressure = 1011
current_demand = 800
battery_capacity = 500
sun_elevation_angle = 60  # Example sun angle at noon

# Get AI Predictions & Optimizations
predicted_solar = agent.predict_solar_energy(sunlight_hours, temperature, humidity)
predicted_wind = agent.predict_wind_energy(wind_speed, air_pressure, temperature)
stored_energy, grid_supply = agent.optimize_battery_storage(predicted_solar, predicted_wind, current_demand, battery_capacity)
optimized_angle = agent.adjust_solar_panel_angle(sun_elevation_angle)

print(f"Predicted Solar Energy Output: {predicted_solar:.2f} kWh")
print(f"Predicted Wind Energy Output: {predicted_wind:.2f} kWh")
print(f"Stored Energy in Battery: {stored_energy:.2f} kWh")
print(f"Energy Supplied to Grid: {grid_supply:.2f} kWh")
print(f"Optimized Solar Panel Angle: {optimized_angle:.2f}°")
