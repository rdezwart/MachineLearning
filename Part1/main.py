# Title: Final Project (Machine Learning for Prediction) - Part 1
# Authors: Robin de Zwart, Veronika Tatsiy, MachineLearning42
# Date: Apr 07, 2021
# Purpose: Building our first Machine Learning Model

# -- Imports -- #

import random

from sklearn.linear_model import LinearRegression


# -- Functions -- #

def generate_training(t_min: int, t_max: int) -> list[list[int]]:
    """
    Generates 2D array of training data, with values based on parameters.

    :param t_min: minimum value for training data
    :param int t_max: maximum value for training data
    :return: list of lists containing three integers
    """
    ret: list[list[int]] = []
    for i in range(100):
        ret.append([
            random.randint(t_min, t_max),
            random.randint(t_min, t_max),
            random.randint(t_min, t_max)
        ])
    return ret


def process_training(training: list[list[int]]) -> list[int]:
    """
    Takes 2D list of training data and applies a formula, and returns the results.

    Formula: y = (1 * x1) + (2 * x2) + (3 * x3)

    :param training: raw training data
    :return: processed training data
    """
    ret: list[int] = []
    for i in range(len(training)):
        val: int = 0
        for j in range(3):
            val += (j + 1) * training[i][j]
        ret.append(val)
    return ret


# -- Code -- #

# - Step 1 - #
# Implemented in process_training()

# - Step 2 - #
# Generate input and output training data
train_input: list[list[int]] = generate_training(0, 1000)
train_output: list[int] = process_training(train_input)

# - Step 3 - #
# Train the machine learning model
predictor = LinearRegression(n_jobs=-1)
predictor.fit(X=train_input, y=train_output)

# - Step 4 - #
# Make a prediction with test data
X_test = [[10, 20, 30]]
outcome = predictor.predict(X=X_test)
coefficients = predictor.coef_
# Final output
print("Prediction: " + str(outcome))
print("Coefficients: " + str(coefficients))
