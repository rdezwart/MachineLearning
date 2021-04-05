# Title: Final Project - Part 4
# Author: Robin de Zwart
# Date: Mar 31, 2021
# Purpose: Interactive Model Building

# -- Imports -- #


# -- Functions -- #

def get_file():
    while True:  # input loop
        print("\nFile name:")
        resp = input("\t> ").strip(" .!")

        try:
            return open(resp)  # exit input loop
        except OSError as e:
            print("Sorry, something went wrong: {0}".format(str(e).capitalize()))
            print("Please try again.")


def get_confirmation(question: str):
    while True:  # confirmation loop
        print("\n{0} (Yes/No)".format(question))
        resp = input("\t> ").strip(" .!").lower()

        if resp == "yes" or resp == "no":
            return resp
        else:
            print("Sorry, I don't understand your answer. Please try again.")


def get_input_indexes(index_list):
    while True:  # input loop
        print("Enter a list of indexes, separated by commas. Example: '1, 2, 4, 5, 10'")
        resp = input("\t> ").strip(" .!")

        resp_list: list = resp.split(",")

        try:
            for i in range(len(resp_list)):
                temp_str: str = resp_list[i]
                resp_list[i] = int(temp_str.strip())

                if resp_list[i] not in index_list:
                    print("Sorry, something went wrong: Invalid index: {0}".format(resp_list[i]))
                    print("Please try again.\n")
                    break  # exit for loop, not triggering else
            else:  # if for loop finishes without breaking, the index list is OK
                if len(resp_list) == len(index_list):
                    print("Sorry, please select fewer indexes.")
                else:
                    break  # exit input loop
        except ValueError as e:
            print("Sorry, something went wrong: {0}".format(str(e).capitalize()))
            print("Please fix that index and try again.\n")

    return resp_list


def get_output_index(index_list):
    while True:  # input loop
        print("Enter an index. Example: '8'")
        resp = input("\t> ").strip(" .!")

        try:
            temp_str: str = resp
            resp_int = int(temp_str)

            if resp_int not in index_list:
                print("Sorry, something went wrong: Invalid index: {0}".format(resp_int))
                print("Please try again.\n")
            else:
                break  # exit input loop
        except ValueError as e:
            print("Sorry, something went wrong: {0}".format(str(e).capitalize()))
            print("Please fix your index and try again.\n")

    return resp_int


def get_percent() -> tuple:
    while True:  # input loop
        print("Enter a whole percentage, between 10 and 90. Example: '80' or '80%'")
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
                return round(resp_float, 3), round(1 - resp_float, 3)  # exit input loop
        except ValueError as e:
            print("Sorry, something went wrong: {0}".format(str(e).capitalize()))
            print("Please try again.")


# -- Code -- #

print("\nHi there! Please copy your desired .csv file into my folder.")
print("Next, enter the name of your file, including the extension. Example: 'SeoulBikeData.csv'")

while True:  # verification loop
    file = get_file()
    print("Thank you.")

    data_file = []
    header = file.readline().strip().split(",")
    for line in file:
        data_file.append(line)

    print("\nYour file has been processed. Please verify the following before continuing.")
    print("\tStructure: {0} columns".format(len(header)))
    print("\t{0:>10} {1} rows + 1 header".format("Data:", len(data_file)))

    resp_file = get_confirmation("Was your file read correctly?")
    if resp_file == "yes":
        break  # exit verification loop
    elif resp_file == "no":
        print("Sorry, I don't know what happened. Please double check your file and try again.")

print("Thank you.")

while True:  # input loop
    print("\nPlease indicate input columns:")
    valid_input_indexes = []
    for col in range(len(header)):
        valid_input_indexes.append(col)
        print("\t{0:>2} - {1}".format(col, header[col]))
    input_indexes = get_input_indexes(valid_input_indexes)

    print("Selected indexes: {0}".format(input_indexes))

    resp_input = get_confirmation("Are these indexes correct?")
    if resp_input == "yes":
        break  # exit input loop
    elif resp_file == "no":
        print("Sorry, please try again.")

print("Thank you.")

while True:  # output loop
    print("\nPlease indicate one output column.")
    valid_output_indexes = []
    for col in range(len(header)):
        if col not in input_indexes:
            valid_output_indexes.append(col)
            print("\t{0:>2} - {1}".format(col, header[col]))
    output_index = get_output_index(valid_output_indexes)

    print("Selected index: {0}".format(output_index))

    resp_output = get_confirmation("Is this index correct?")
    if resp_output == "yes":
        break  # exit output loop
    elif resp_output == "no":
        print("Sorry, please try again.")

print("Thank you.")

print("\nYour data will be split between training and testing. I recommend an 80% split.")
print("I recommend 80%")
data_percent: tuple = get_percent()
data_left = round(len(data_file) * data_percent[0])
data_right = round(len(data_file) * data_percent[1])
print(data_percent)
print("\nWe will use {0:.0f}% of your data for training, and {1:.0f}% for testing.".format(
    data_percent[0] * 100, data_percent[1] * 100))
print("This results in the following split:")
print("\t{0:>8}: {1} rows".format("Training", data_left))
print("\t{0:>8}: {1}".format("Testing", data_right))

print(len(data_file))
print(data_left + data_right)
