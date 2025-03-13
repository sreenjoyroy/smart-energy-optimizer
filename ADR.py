###AI Demand Response (ADR) System Code
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from scipy.optimize import minimize

class DemandResponseAgent:
    def __init__(self, energy_data, tariff_rates):
        self.energy_data = energy_data
        self.tariff_rates = tariff_rates
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train_model(self):
        X = self.energy_data[['time_of_day', 'day_of_week', 'temperature']]
        y = self.energy_data['power_demand']
        self.model.fit(X, y)

    def predict_peak_demand(self, time_of_day, day_of_week, temperature):
        feature_names = ["time_of_day", "day_of_week", "temperature"]
        input_data = pd.DataFrame([[time_of_day, day_of_week, temperature]], columns=feature_names)

        # Predict optimized load shift time
        return self.model.predict(input_data)[0]

    def optimize_load_shift(self, time_of_day, day_of_week, temperature):
        def objective(shift):
            adjusted_time = int((time_of_day + shift) % 24)  # Convert to integer
            predicted_demand = self.predict_peak_demand(adjusted_time, day_of_week, temperature)
            return predicted_demand + self.tariff_rates[adjusted_time]  # Optimize based on demand & cost


        optimized_shift = minimize(objective, 0, bounds=[(-3, 3)])  # Shift within ±3 hours
        return (time_of_day + optimized_shift.x[0]) % 24

# Sample Energy Data (IoT Sensors)
data = pd.DataFrame({
    'time_of_day': [10, 12, 14, 18, 22],
    'day_of_week': [1, 1, 2, 3, 4],  # Monday = 1, etc.
    'temperature': [30, 28, 25, 20, 18],
    'power_demand': [800, 1000, 950, 870, 600]
})

# Sample Tariff Rates (Hourly Pricing)
tariff_rates = {hour: np.random.uniform(0.1, 0.5) for hour in range(24)}

# Run AI Demand Response Agent
agent = DemandResponseAgent(data, tariff_rates)
agent.train_model()

# Predict Peak Demand & Optimize Load Shift
current_time = 14
optimized_time = agent.optimize_load_shift(time_of_day=current_time, day_of_week=2, temperature=27)
print(f"Optimized Load Shift Time: {optimized_time:.2f} hours")
