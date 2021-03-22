# Title: Final Project - Part 2
# Author: Robin de Zwart, MachineLearning42
# Date: Mar 22, 2021
# Purpose: Processing external dataset

# -- Imports -- #

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
