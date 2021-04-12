# Title: Final Project (Machine Learning for Prediction) - Part 4
# Authors: Robin de Zwart, Veronika Tatsiy, MachineLearning42
# Date: Mar 31, 2021
# Purpose: Interactive Model Building

# -- Imports -- #

import random
import time
import turtle
from typing import TextIO  # just here for type hinting

from sklearn.linear_model import LinearRegression


# -- Functions -- #

def get_file() -> TextIO:
    """
    Asks the user for the path of a .CSV file. Loops if an error occurs.

    :return: the resulting file at the given path
    """
    while True:  # input loop
        print(
            "\nEnter the name of your file, including the extension. "
            "Example: 'SeoulBikeData.csv'")
        resp = input("\t> ").strip(" .!")

        try:
            return open(resp, encoding="utf8")  # exit input loop
        except OSError as file_error:
            print(
                "Sorry, something went wrong: "
                "{0}".format(str(file_error).capitalize()))
            print("Please try again.")
        time.sleep(1)


def get_confirmation(question: str) -> str:
    """
    Asks the user for a yes/no answer to a question.

    :param question: prompt to ask for confirmation
    :return: a formatted yes/no version of user's answer
    """
    while True:  # confirmation loop
        print("\n{0} (Yes/No)".format(question))
        resp = input("\t> ").strip(" .!").lower()

        if resp == "yes" or resp == "y":
            return "yes"
        elif resp == "no" or resp == "n":
            return "no"
        else:
            print("Sorry, I don't understand your answer. Please try again.")
        time.sleep(1)


def get_input_indexes(valid_indexes: list[int]) -> list[int]:
    """
    Asks the user for a list of indexes corresponding to desired input columns.

    :param valid_indexes: list of indexes that haven't already been used
    :return: the list of selected indexes, as integers
    """
    while True:  # input loop
        print(
            "Enter a list of indexes, separated by commas. "
            "Example: '1, 2, 4, 5, 10'")
        resp = input("\t> ").strip(" .!")

        resp_list: list = resp.split(",")

        try:
            for i in range(len(resp_list)):
                temp_str: str = resp_list[i]
                resp_list[i] = int(temp_str.strip())

                if resp_list[i] not in valid_indexes:
                    print(
                        "Sorry, something went wrong: Invalid index: "
                        "{0}".format(resp_list[i]))
                    print("Please try again.\n")
                    break  # exit for loop, not triggering else

                if resp_list.count(resp_list[i]) > 1:
                    print(
                        "Sorry, you cannot have duplicate indexes: "
                        "{0}".format(resp_list[i]))
                    print("Please try again.\n")
                    break
            else:  # if for loop finishes without breaking, the index list is OK
                if len(resp_list) == len(valid_indexes):
                    print("Sorry, please select fewer indexes.")
                else:
                    break  # exit input loop
        except ValueError as input_error:
            print(
                "Sorry, something went wrong: "
                "{0}".format(str(input_error).capitalize()))
            print("Please fix that index and try again.\n")
        time.sleep(1)

    return resp_list


def get_output_index(valid_indexes: list[int]) -> int:
    """
    Asks the user for an index corresponding to desired output column.

    :param valid_indexes: list of indexes that haven't already been used
    :return: the selected index
    """
    while True:  # input loop
        print("Enter an index. Example: '8'")
        resp = input("\t> ").strip(" .!")

        try:
            temp_str: str = resp
            resp_int = int(temp_str)

            if resp_int not in valid_indexes:
                print(
                    "Sorry, something went wrong: Invalid index: "
                    "{0}".format(resp_int))
                print("Please try again.\n")
            else:
                break  # exit input loop
        except ValueError as output_error:
            print(
                "Sorry, something went wrong: "
                "{0}".format(str(output_error).capitalize()))
            print("Please fix your index and try again.\n")
        time.sleep(1)

    return resp_int


def get_percent() -> tuple:
    """
    Asks the user for a whole percentage, corresponding to the desired
    training/testing split of data.

    :return: the decimal values of training/testing split
    """
    while True:  # input loop
        print(
            "Enter a whole percentage, between 10 and 90. "
            "Example: '80' or '80%'")
        resp = input("\t> ").strip(" .!")

        try:
            temp_str: str = resp
            resp_float = float(temp_str.strip("%"))

            if resp_float < 10:
                print("Sorry, that percentage is too small. Try again.")
            elif resp_float > 90:
                print("Sorry, that percentage is too big. Try again.")
            else:
                resp_float = resp_float / 100
                ret = (round(resp_float, 3), round(1 - resp_float, 3))
                return ret  # exit input loop
        except ValueError as percent_error:
            print(
                "Sorry, something went wrong: "
                "{0}".format(str(percent_error).capitalize()))
            print("Please try again.\n")
        time.sleep(1)


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


def draw_results(win_x: float, win_y: float) -> None:
    """
    Uses a turtle to draw results and scales output proportional to screen size.

    :param win_x: window width, fraction of total monitor width
    :param win_y: window height, fraction of total monitor height
    """
    # noinspection PyBroadException
    try:
        # Display setup
        s = turtle.Screen()
        s.setup(win_x, win_y)
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
        col_width = (s.window_width() / (len(results) + 2)) - col_gap
        height_mult = 1 / best_perc  # scale bars to fit window based on max val

        # Draw headers
        t.pu()
        t.setpos(s.window_width() / 2, s.window_height() - 30)
        t.setheading(0)
        t.write(
            "Accuracy of valid (non-zero) predictions and their percentage of "
            "all results.",
            align="center",
            font=("Arial", 10, "bold")
        )
        t.rt(90)
        t.forward(20)
        t.write(
            "Total: {0}\tValid: {1}\tMissing: {2}".format(
                len(outcome),
                num_valid_entries,
                len(outcome) - num_valid_entries
            ),
            align="center"
        )
        t.forward(20)
        t.write("Click anywhere to close.", align="center")

        # Draw resulting graph
        t.setpos(0, 25)
        t.setheading(0)
        t.forward(col_width)

        for key in results:
            # Get current item
            perc = results[key] / num_valid_entries
            col_height = (s.window_height() - 150) * perc * height_mult

            # Pick random colour
            t.fillcolor((
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ))

            # Bottom left corner of bar
            t.setheading(0)
            t.forward(col_gap)
            t.pd()
            t.begin_fill()

            # Left side of bar
            t.lt(90)
            t.forward(col_height)
            t.rt(90)

            # Top side of bar, plus writing
            t.forward(col_width / 2)
            t.pu()
            t.left(90)
            t.fd(10)
            t.write("({0:.2f}%)".format(perc * 100), align="center")
            t.fd(15)
            t.write("{0}".format(results[key]), align="center")
            t.bk(25)
            t.right(90)
            t.pd()
            t.forward(col_width / 2)

            # Right side of bar
            t.rt(90)
            t.forward(col_height)
            t.lt(90)

            # Bottom side of bar, plus writing
            t.bk(col_width / 2)
            t.pu()
            t.right(90)
            t.fd(25)
            t.write("{0}".format(key), align="center")
            t.bk(25)
            t.left(90)
            t.pd()
            t.bk(col_width / 2)
            t.fd(col_width)

            # Finish the shape
            t.end_fill()
            t.pu()

        print(
            "Done! The final window may be minimized, so check your taskbar.")

        # Screen size warning
        if s.window_width() < 720 or s.window_height() < 300:
            print("\nWARNING:")
            print(
                "\tThe display window is smaller than the recommended minimum "
                "size of 720x300.")
            print(
                "\tIt is currently "
                "{0}x{1}.".format(s.window_width(), s.window_height()))
            print(
                "\tPlease adjust the arguments of 'draw_results()' at the "
                "bottom of the file.")

        s.exitonclick()
    except Exception:
        pass  # Catch errors if the user exits the window while still drawing


# -- Code -- #

# Get file location from user
print("\nHi there! Please copy your desired .csv file into my folder.")
while True:
    file = get_file()
    print("Thank you.")

    # Prepare file for reading
    data_file = []
    header = file.readline().strip().split(",")
    for line in file:
        data_file.append(line.strip().split(","))

    time.sleep(1)
    print(
        "\nYour file has been processed. "
        "Please verify the following before continuing.")
    print("\tStructure: {0} columns".format(len(header)))
    print("\t{0:>10} {1} rows + 1 header".format("Data:", len(data_file)))

    # Ask user for confirmation
    resp_file = get_confirmation("Was your file read correctly?")
    if resp_file == "yes":
        break  # exit loop and proceed
    elif resp_file == "no":
        print(
            "Sorry, I don't know what happened. "
            "Please double check your file and try again.")
    time.sleep(1)

print("Thank you.")
time.sleep(1)

# Get input indexes from user
while True:
    print("\nPlease indicate input columns:")
    print("[Index] - [Name]: [Example]")
    # Print valid indexes
    valid_input_indexes = []
    for col in range(len(header)):
        valid_input_indexes.append(col)
        print("\t{0:>2} - {1}: {2}".format(col, header[col], data_file[0][col]))
    input_indexes = get_input_indexes(valid_input_indexes)

    print("Selected indexes: {0}".format(input_indexes))

    # Make sure entries are numbers
    for index in input_indexes:
        try:
            conv = float(data_file[0][index])
        except ValueError as e:
            print(
                "Sorry, something went wrong: "
                "{0}".format(str(e).capitalize()))
            print("Please try again.")
            break
    else:
        # Ask user for confirmation
        resp_input = get_confirmation("Are these indexes correct?")
        if resp_input == "yes":
            break  # exit loop and proceed
        elif resp_input == "no":
            print("Sorry, please try again.")
    time.sleep(1)

print("Thank you.")
time.sleep(1)

# Get output index from user
while True:
    print("\nPlease indicate one output column.")
    print("[Index] - [Name]: [Example]")
    # Print valid indexes
    valid_output_indexes = []
    for col in range(len(header)):
        if col not in input_indexes:
            valid_output_indexes.append(col)
            print("\t{0:>2} - {1}: {2}".format(
                col, header[col], data_file[0][col]))
    output_index = get_output_index(valid_output_indexes)

    print("Selected index: {0}".format(output_index))

    # Make sure entry is a number
    try:
        conv = float(data_file[0][output_index])

        # Ask user for confirmation
        resp_output = get_confirmation("Is this index correct?")
        if resp_output == "yes":
            break  # exit loop and proceed
        elif resp_output == "no":
            print("Sorry, please try again.")
    except ValueError as e:
        print("Sorry, something went wrong: {0}".format(str(e).capitalize()))
        print("Please try again.")
    time.sleep(1)

print("Thank you.")
time.sleep(1)

# Get data split from user
while True:
    print(
        "\nYour data will be split between training and testing. "
        "I recommend a value of 80%.")
    data_percent: tuple = get_percent()
    data_left = round(len(data_file) * data_percent[0])
    data_right = round(len(data_file) * data_percent[1])

    print("Selected split: {0}".format(data_percent))

    # Ask user for confirmation
    resp_split = get_confirmation("Is this correct?")
    if resp_split == "yes":
        break  # exit loop and proceed
    elif resp_split == "no":
        print("Sorry, please try again.")
    time.sleep(1)

print("Thank you.")
time.sleep(1)

# Final output - info
print(
    "\nWe will use {0:.0f}% of your data for training, and {1:.0f}% for "
    "testing.".format(data_percent[0] * 100, data_percent[1] * 100))
print("This results in the following split:")
print("\t{0:>8}: {1} rows".format("Training", data_left))
print("\t{0:>8}: {1} rows".format("Testing", data_right))
time.sleep(1)

# Final output - confirmation
print("\nEnter any value to train the model and display your results.")
resp_go = input("\t> ")
print("Here we go.")
time.sleep(1)

# Final output - progress
print("\nPROGRESS:")
print("\tGathering data...")

# Read file and process data
total_input = []
total_output = []
for row in data_file:
    input_vals = []
    for input_index in input_indexes:
        input_vals.append(float(row[input_index]))
    total_input.append(input_vals)

    predict_val = float(row[output_index])
    total_output.append(predict_val)

# Split input and output
print("\tSplitting data...")
splitter = data_left
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
for input_index in range(len(outcome)):
    if test_output[input_index] > 0:
        num_valid_entries += 1
        error = ((abs(test_output[input_index] - outcome[input_index])) /
                 test_output[input_index])
        tally_result(error)

# Final output - drawing
print("\tDrawing results...")
draw_results(0.75, 0.5)  # modify these values if your screen is too small
print("\nThank you for using this program, have a nice day.")
