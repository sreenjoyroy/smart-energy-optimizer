##AI Agent for EV Charging Optimization (Python Code)
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import random

class SmartEVChargingAgent:
    def __init__(self, grid_data):
        self.grid_data = grid_data
        self.charging_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.routing_model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train_models(self):
        # Train charging model
        X_charge = self.grid_data[['grid_load_MW', 'time_of_day', 'electricity_price']]
        y_charge = self.grid_data['optimal_charge_time']
        self.charging_model.fit(X_charge, y_charge)

        # Train routing model
        X_route = self.grid_data[['traffic_level', 'terrain_difficulty', 'battery_level']]
        y_route = self.grid_data['optimal_route_efficiency']
        self.routing_model.fit(X_route, y_route)

    def suggest_charging_time(self, grid_load, time_of_day, electricity_price):
        predicted_charge_time = self.charging_model.predict([[grid_load, time_of_day, electricity_price]])[0]
        return max(0, min(predicted_charge_time, 24))  # Ensure time is within 24 hours

    def optimize_ev_route(self, traffic, terrain, battery_level):
        predicted_efficiency = self.routing_model.predict([[traffic, terrain, battery_level]])[0]
        return max(0, min(predicted_efficiency, 100))  # Efficiency in percentage

# Sample Grid & EV Data for Training
data = pd.DataFrame({
    'grid_load_MW': [500, 600, 700, 800, 900, 1000],
    'time_of_day': [0, 6, 12, 18, 21, 23],
    'electricity_price': [0.10, 0.15, 0.20, 0.25, 0.30, 0.35],
    'optimal_charge_time': [2, 5, 9, 14, 19, 23],
    'traffic_level': [1, 2, 3, 4, 5, 6],
    'terrain_difficulty': [1, 2, 3, 4, 5, 6],
    'battery_level': [90, 80, 70, 60, 50, 40],
    'optimal_route_efficiency': [90, 85, 80, 75, 70, 65]
})

# Initialize AI Agent
agent = SmartEVChargingAgent(data)
agent.train_models()

# Simulated Inputs
grid_load = 850  # MW
time_of_day = 20  # 8 PM
electricity_price = 0.28  # $ per kWh
traffic = 3  # Moderate traffic
terrain = 2  # Flat terrain
battery_level = 75  # %

# Get AI-Driven Recommendations
best_charging_time = agent.suggest_charging_time(grid_load, time_of_day, electricity_price)
optimal_route_efficiency = agent.optimize_ev_route(traffic, terrain, battery_level)

print(f"Recommended Charging Time: {best_charging_time:.2f} hours")
print(f"Optimal Route Efficiency: {optimal_route_efficiency:.2f}%")
