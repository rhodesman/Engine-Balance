import pandas as pd
import pulp
import numpy as np

# Load the data from the CSV file
df = pd.read_csv('weights.csv')

# Extract columns
pistons = df['Pistons'].to_numpy()
rods = df['Rods'].to_numpy()
pins = df['Pins'].to_numpy()

# Number of parts
num_parts = len(pistons)

# Ensure the number of pistons, rods, and pins are the same
assert len(rods) == num_parts and len(pins) == num_parts, "The number of pistons, rods, and pins must be equal."

# Create a LP problem
prob = pulp.LpProblem("MinimizeWeightVariation", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(num_parts), range(num_parts), range(num_parts)), cat='Binary')

# Objective: Minimize the weight variation
total_weights = [[[(pistons[i] + rods[j] + pins[k]) for k in range(num_parts)] for j in range(num_parts)] for i in range(num_parts)]
average_weight = np.mean(total_weights)
prob += pulp.lpSum([(total_weights[i][j][k] - average_weight)**2 * x[i][j][k] for i in range(num_parts) for j in range(num_parts) for k in range(num_parts)])

# Constraints: Ensure each part is used exactly once
for i in range(num_parts):
    prob += pulp.lpSum([x[i][j][k] for j in range(num_parts) for k in range(num_parts)]) == 1
    prob += pulp.lpSum([x[j][i][k] for j in range(num_parts) for k in range(num_parts)]) == 1
    prob += pulp.lpSum([x[j][k][i] for j in range(num_parts) for k in range(num_parts)]) == 1

# Solve the problem
prob.solve()

# Extract the best combinations
best_combinations = []
for i in range(num_parts):
    for j in range(num_parts):
        for k in range(num_parts):
            if pulp.value(x[i][j][k]) == 1:
                total_weight = pistons[i] + rods[j] + pins[k]
                best_combinations.append((i + 1, j + 1, k + 1, total_weight))

# Convert results to DataFrame
best_combinations_df = pd.DataFrame(best_combinations, columns=['Piston_Number', 'Rod_Number', 'Pin_Number', 'Total_Weight'])

# Display the best combinations
print("Best Combinations:")
for i, row in best_combinations_df.iterrows():
    print(f"Piston {row['Piston_Number']} + Rod {row['Rod_Number']} + Pin {row['Pin_Number']} => Total Weight: {row['Total_Weight']}")

# Save the best combinations to a CSV file
best_combinations_df.to_csv('best_combinations.csv', index=False)