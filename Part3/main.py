# Title: Final Project (Machine Learning for Prediction) - Part 3
# Authors: Robin de Zwart, Veronika Tatsiy, MachineLearning42
# Date: Mar 24, 2021
# Purpose: Building another model for different data

# -- Imports -- #

import random
import turtle

from sklearn.linear_model import LinearRegression


# -- Functions -- #

def tally_result(e):
    """
    Helper function for counting error margins.
    :param e: error percentage
    """
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
    """
    Uses a turtle to draw a math, and scales output proportional to screen size.
    """
    # Display setup
    s = turtle.Screen()
    s.setup(0.75, 0.5)
    s.setworldcoordinates(0, 0, s.window_width(), s.window_height())
    s.colormode(255)

    # Turtle setup
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # Display math
    best_key = max(results, key=results.get)
    best_perc = results[best_key] / num_valid_entries

    col_gap = 12
    col_width = (s.window_width() / (len(results) + 2)) - col_gap
    height_mult = 1 / best_perc  # scale bars to fit window, based on highest bar

    # Draw headers
    t.pu()
    t.setpos(s.window_width() / 2, s.window_height() - (col_gap * 3))
    t.setheading(0)
    t.write(
        "Number of non-zero predictions and their percentage of total non-zero results.",
        align="center",
        font=("Arial", 10, "bold")
    )
    t.rt(90)
    t.forward(col_gap * 2)
    t.write("Click anywhere to close.", align="center")

    # Draw resulting graph
    t.setpos(0, col_gap * 2)
    t.setheading(0)
    t.forward(col_width)

    for key in results:
        perc = results[key] / num_valid_entries
        col_height = (s.window_height() - (col_gap * 10)) * perc * height_mult

        t.fillcolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        t.setheading(0)
        t.forward(col_gap)
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

    s.exitonclick()


# -- Code -- #

# File vars
file = open("RealEstateValuationData.csv")
header = file.readline()
total_input = []
total_output = []

# Read data
for line in file:
    data = line.strip().split(",")

    numeric_vals = []
    for i in range(1, 5):
        numeric_vals.append(float(data[i]))
    total_input.append(numeric_vals)

    predict_val = float(data[6])
    total_output.append(predict_val)

# Split input and output
splitter = int(len(total_output) * 0.8)

train_input = total_input[:splitter]
train_output = total_output[:splitter]

test_input = total_input[splitter:]
test_output = total_output[splitter:]

# Train the model
predictor = LinearRegression(n_jobs=-1)
predictor.fit(X=train_input, y=train_output)

# Test the model
outcome = predictor.predict(X=test_input)

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

# Calculate performance
num_valid_entries = 0
for i in range(len(outcome)):
    if test_output[i] > 0:
        num_valid_entries += 1
        error = ((abs(test_output[i] - outcome[i])) / test_output[i]) * 100
        tally_result(error)

draw_results()
