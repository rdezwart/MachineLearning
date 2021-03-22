# Title: Final Project - Part 2
# Author: Robin de Zwart, MachineLearning42
# Date: Mar 22, 2021
# Purpose: Processing external dataset

# -- Imports -- #

from sklearn.linear_model import LinearRegression

# -- Functions -- #

# -- Code -- #

total_input = []
total_output = []

# Grab data
file = open("SeoulBikeData.csv")
header = file.readline()

# Read data
for line in file:
    data = line.strip().split(",")

    rented_bikes = float(data[1])
    total_output.append(rented_bikes)

    numeric_values = []
    for i in range(2, 11):
        numeric_values.append(float(data[i]))
    total_input.append(numeric_values)

# Split input
train_input = total_input[:7000]
test_input = total_input[7000:]
# Split output
train_output = total_output[:7000]
test_output = total_output[7000:]

# Train the model
predictor = LinearRegression(n_jobs=-1)
# predictor.fit(X=train_input, y=train_output)
predictor.fit(X=total_input[:7000], y=total_output[:7000])

# Test the model
outcome = predictor.predict(X=test_input)


for i in range(len(outcome)):
    if test_output[i] != 0.0:
        error = (abs(test_output[i] - outcome[i])) / test_output[i]
        print("[{0}] - {1:.2f} ({2:.2f}, {3:.0f})".format(i, error*100, outcome[i], test_output[i]))
