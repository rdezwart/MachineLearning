# Title: Final Project (Machine Learning for Prediction) - Part 2
# Authors: Robin de Zwart, Veronika Tatsiy, MachineLearning42
# Date: Apr 08, 2021
# Purpose: Building a Model Using Real Data

# -- Imports -- #

import random
import turtle

from sklearn.linear_model import LinearRegression


# -- Functions -- #

def tally_result(e_perc: float) -> None:
    """
    Adds 1 to corresponding dictionary entry, based on category.

    :param e_perc: decimal error percentage
    """
    e_perc *= 100
    if 0 <= e_perc <= 10:
        results["0-10"] += 1
    elif 10 <= e_perc <= 20:
        results["10-20"] += 1
    elif 20 <= e_perc <= 30:
        results["20-30"] += 1
    elif 30 <= e_perc <= 40:
        results["30-40"] += 1
    elif 40 <= e_perc <= 50:
        results["40-50"] += 1
    elif 50 <= e_perc <= 60:
        results["50-60"] += 1
    elif 60 <= e_perc <= 70:
        results["60-70"] += 1
    elif 70 <= e_perc <= 80:
        results["70-80"] += 1
    elif 80 <= e_perc <= 90:
        results["80-90"] += 1
    elif 90 <= e_perc <= 100:
        results["90-100"] += 1
    elif 100 < e_perc:
        results["100+"] += 1


def draw_results() -> None:
    """
    Uses a turtle to draw results, and scales output proportional to screen size.
    """
    # noinspection PyBroadException
    try:
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

        col_gap = s.window_width() // 100
        head_gap = s.window_height() // 50
        col_width = (s.window_width() / (len(results) + 2)) - col_gap
        height_mult = 1 / best_perc  # scale bars to fit window, based on highest bar

        # Draw headers
        t.pu()
        t.setpos(s.window_width() / 2, s.window_height() - (head_gap * 3))
        t.setheading(0)
        t.write(
            "Accuracy of valid (non-zero) predictions and their percentage of all results.",
            align="center",
            font=("Arial", 10, "bold")
        )
        t.rt(90)
        t.forward(head_gap * 2)
        t.write(
            "Total: {0}\tValid: {1}\tMissing: {2}".format(
                len(outcome),
                num_valid_entries,
                len(outcome) - num_valid_entries
            ),
            align="center"
        )
        t.forward(head_gap * 2)
        t.write("Click anywhere to close.", align="center")

        # Draw resulting graph
        t.setpos(head_gap, col_gap * 2)
        t.setheading(0)
        t.forward(col_width)

        for key in results:
            perc = results[key] / num_valid_entries
            col_height = (s.window_height() - (head_gap * 12)) * perc * height_mult

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
            t.fd(head_gap / 2)
            t.write("{0} ({1:.2f}%)".format(results[key], perc * 100), align="center")
            t.bk(head_gap / 2)
            t.right(90)
            t.pd()
            t.forward(col_width / 2)

            t.rt(90)
            t.forward(col_height)
            t.lt(90)

            t.bk(col_width / 2)
            t.pu()
            t.right(90)
            t.fd(head_gap * 2)
            t.write("{0}".format(key), align="center")
            t.bk(head_gap * 2)
            t.left(90)
            t.pd()
            t.bk(col_width / 2)
            t.fd(col_width)

            t.end_fill()
            t.pu()

        print("Done! The final window may be minimized, so check your taskbar. :)")
        s.exitonclick()
    except Exception:
        pass  # just here not throw errors if the user exits the window while still drawing


# -- Code -- #

print("PROGRESS:")

# Prepare for file reading
file = open("SeoulBikeData.csv", encoding="utf8")
header = file.readline()
total_input = []
total_output = []

# Read file and process data
print("\tGathering data...")
for line in file:
    data = line.strip("\n").split(",")

    numeric_values = []
    for i in range(2, 11):
        numeric_values.append(float(data[i]))
    total_input.append(numeric_values)

    rented_bikes = float(data[1])
    total_output.append(rented_bikes)

# Split input and output
print("\tSplitting data...")
splitter = int(len(total_output) * 0.8)
train_input = total_input[:splitter]
train_output = total_output[:splitter]
test_input = total_input[splitter:]
test_output = total_output[splitter:]

# Train the machine learning model
print("\tBeginning training...")
predictor = LinearRegression(n_jobs=-1)
predictor.fit(X=train_input, y=train_output)

# Make a prediction with test data
print("\tBeginning prediction...")
outcome = predictor.predict(X=test_input)

# Track performance
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
print("\tTallying results...")
num_valid_entries = 0
for i in range(len(outcome)):
    if test_output[i] > 0:
        num_valid_entries += 1
        error = (abs(test_output[i] - outcome[i])) / test_output[i]
        tally_result(error)

# Final output
print("\tDrawing results...")
draw_results()  # prints when done
print("\nThank you for using this program, have a nice day.")
