import numpy as np
from scipy.optimize import minimize
import sys


sys.stdout.reconfigure(encoding='utf-8')


# AI Agent Outputs (Simulated)
hvac_power_demand = 300  # kW (From Smart HVAC Agent)
lighting_power_demand = 150  # kW (From Smart Lighting Agent)
ev_charging_demand = 200  # kW (From EV Charging Agent)
solar_supply = 250  # kW (From Renewable Energy Agent)
wind_supply = 100  # kW (From Renewable Energy Agent)
grid_capacity = 1000  # Maximum grid load (kW)
demand_response_limit = 800  # kW (From DR System Agent)

# Define Optimization Function: Minimize Total Energy Cost & Grid Load
def energy_optimization(vars):
    hvac, lighting, ev_charging, solar, wind = vars

    # Weighted sum of all energy usage components
    total_energy_cost = (
        0.5 * hvac +  # HVAC weight
        0.3 * lighting +  # Lighting weight
        0.4 * ev_charging -  # EV charging weight
        0.3 * solar -  # Renewable gains
        0.2 * wind
    )
    return total_energy_cost

# Constraints
def grid_limit(vars):
    return grid_capacity - sum(vars)  # Total energy should not exceed grid capacity

def demand_response_constraint(vars):
    return demand_response_limit - sum(vars)  # Adjust load during peak hours

# Initial Values [HVAC, Lighting, EV, Solar, Wind]
initial_guess = [hvac_power_demand, lighting_power_demand, ev_charging_demand, solar_supply, wind_supply]

# Constraints
constraints = (
    {'type': 'ineq', 'fun': grid_limit},  # Ensure grid is not overloaded
    {'type': 'ineq', 'fun': demand_response_constraint}  # Apply Demand Response limits
)

# Bounds for each parameter [Min, Max]
bounds = [(100, 500), (50, 300), (50, 400), (100, 500), (50, 200)]  # [HVAC, Lighting, EV, Solar, Wind]

# Run Optimization
optimized_values = minimize(energy_optimization, initial_guess, bounds=bounds, constraints=constraints)

# Extract optimized values
hvac_opt, lighting_opt, ev_opt, solar_opt, wind_opt = optimized_values.x

# Display Optimized Results
print(f"🔹 Optimized HVAC Power: {hvac_opt:.2f} kW")
print(f"🔹 Optimized Lighting Power: {lighting_opt:.2f} kW")
print(f"🔹 Optimized EV Charging Power: {ev_opt:.2f} kW")
print(f"🔹 Optimized Solar Energy Usage: {solar_opt:.2f} kW")
print(f"🔹 Optimized Wind Energy Usage: {wind_opt:.2f} kW")
