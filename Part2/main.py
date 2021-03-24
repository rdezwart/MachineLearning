# Title: Final Project - Part 2
# Author: Robin de Zwart, MachineLearning42
# Date: Mar 23, 2021
# Purpose: Processing and displaying external dataset

# -- Imports -- #

import random
import turtle

from sklearn.linear_model import LinearRegression


# -- Functions -- #

def count_results(e):
    if 0 <= e <= 10:
        results["0-10"] += 1
    elif 10 <= e <= 20:
        results["10-20"] += 1
    elif 20 <= e <= 30:
        results["20-30"] += 1
    elif 30 <= e <= 40:
        results["30-40"] += 1
    elif 40 <= e <= 50:
        results["40-50"] += 1
    elif 50 <= e <= 60:
        results["50-60"] += 1
    elif 60 <= e <= 70:
        results["60-70"] += 1
    elif 70 <= e <= 80:
        results["70-80"] += 1
    elif 80 <= e <= 90:
        results["80-90"] += 1
    elif 90 <= e <= 100:
        results["90-100"] += 1
    else:
        results["100+"] += 1


def draw_results():
    # Prep turtle
    t.setpos(0, col_gap * 2)
    t.forward(col_width)

    # Turtle, engage!
    for key in results:
        perc = results[key] / num_valid_entries
        col_height = (s.window_height() - (col_gap * 10)) * perc * height_mult

        t.forward(col_gap)

        t.fillcolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        t.pd()
        t.begin_fill()

        t.lt(90)
        t.forward(col_height)
        t.rt(90)

        t.forward(col_width / 2)
        t.pu()
        t.left(90)
        t.fd(col_gap / 2)
        t.write("{0} ({1:.2f}%)".format(results[key], perc * 100), align="center")
        t.bk(col_gap / 2)
        t.right(90)
        t.pd()
        t.forward(col_width / 2)

        t.rt(90)
        t.forward(col_height)
        t.lt(90)

        t.bk(col_width / 2)
        t.pu()
        t.right(90)
        t.fd(col_gap * 2)
        t.write("{0}".format(key), align="center")
        t.bk(col_gap * 2)
        t.left(90)
        t.pd()
        t.bk(col_width / 2)
        t.fd(col_width)

        t.end_fill()
        t.pu()


# -- Code -- #

# File vars
file = open("SeoulBikeData.csv")
header = file.readline()
total_input = []
total_output = []

# Read data
for line in file:
    data = line.strip().split(",")

    rented_bikes = float(data[1])
    total_output.append(rented_bikes)

    numeric_values = []
    for i in range(2, 11):
        numeric_values.append(float(data[i]))
    total_input.append(numeric_values)

# Split input and output
train_input = total_input[:7000]
test_input = total_input[7000:]
train_output = total_output[:7000]
test_output = total_output[7000:]

# Train the model
predictor = LinearRegression(n_jobs=-1)
predictor.fit(X=train_input, y=train_output)

# Test the model
outcome = predictor.predict(X=test_input)

# Count performance
results = {
    "0-10": 0,
    "10-20": 0,
    "20-30": 0,
    "30-40": 0,
    "40-50": 0,
    "50-60": 0,
    "60-70": 0,
    "70-80": 0,
    "80-90": 0,
    "90-100": 0,
    "100+": 0
}

# results["50-60"] = 1760

# Calculate performance
num_valid_entries = 0
for i in range(len(outcome)):
    if test_output[i] > 0:
        num_valid_entries += 1
        error = (abs(test_output[i] - outcome[i])) / test_output[i]
        count_results(error * 100)

# Display setup
s = turtle.Screen()
s.setup(0.75, 0.5)
s.setworldcoordinates(0, 0, s.window_width(), s.window_height())
s.colormode(255)

# Turtle setup
t = turtle.Turtle()
t.speed(0)
t.pu()
t.hideturtle()

# Display math
best_key = max(results, key=results.get)
best_perc = results[best_key] / num_valid_entries

col_gap = 12
col_width = (s.window_width() / (len(results) + 2)) - col_gap
height_mult = 1 / best_perc  # scale bars to fit window, based on highest bar

draw_results()

t.setpos(s.window_width() / 2, s.window_height() - (col_gap * 3))
t.write(
    "Number of non-zero predictions and their percentage of total non-zero results.",
    align="center",
    font=("Arial", 10, "bold")
)
t.rt(90)
t.forward(col_gap*2)
t.write("Click anywhere to close.", align="center")

s.exitonclick()
