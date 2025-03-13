###AI SEMS Agent Code
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class SmartEnergyAgent:
    def __init__(self, data):
        # Assume 'energy_consumption' is the target variable
        self.features = ["occupancy", "outside_temp", "time_of_day"]  # Correct input features
        self.target = "energy_consumption"  # What we're predicting

        self.X = data[self.features]  # Only use selected features
        self.y = data[self.target]  # Target variable

        self.model = RandomForestRegressor()

    def train_model(self):
        self.model.fit(self.X, self.y)  # Train the model

    def predict_energy_consumption(self, occupancy, outside_temp, time_of_day):
        input_data = pd.DataFrame([[occupancy, outside_temp, time_of_day]], columns=self.features)
        return self.model.predict(input_data)[0]  # Predict energy consumption

# Sample training data
data = pd.DataFrame({
    'occupancy': [10, 30, 50, 20, 5],
    'outside_temp': [30, 28, 25, 20, 18],
    'time_of_day': [10, 12, 14, 18, 22],
    'energy_consumption': [500, 700, 600, 550, 400]  # Target variable
})

# Initialize and train agent
agent = SmartEnergyAgent(data)
agent.train_model()

# Predict with correct feature inputs
predicted_energy = agent.predict_energy_consumption(occupancy=40, outside_temp=27, time_of_day=14)
print(f"Predicted Energy Consumption: {predicted_energy:.2f}")
