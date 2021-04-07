# Title: Final Project - Part 1
# Author: Robin de Zwart, MachineLearning42
# Date: Mar 22, 2021
# Purpose: Generating a training set

# -- Imports -- #

import random
from sklearn.linear_model import LinearRegression


# -- Functions -- #

def generate_training(t_min, t_max):
    ret = []
    for i in range(100):
        ret.append([
            random.randint(t_min, t_max),
            random.randint(t_min, t_max),
            random.randint(t_min, t_max)
        ])
    return ret


def process_training(training):
    """
    Formula: y = (1 * x1) + (2 * x2) + (3 * x3)
    :param training: training_set, 2D array
    :return: output_set, 1D array
    """
    ret = []
    for i in range(len(training)):
        val = 0
        for j in range(3):
            val += (j + 1) * training[i][j]
        ret.append(val)
    return ret


# -- Code -- #

train_input = generate_training(0, 1000)
train_output = process_training(train_input)

predictor = LinearRegression(n_jobs=-1)
predictor.fit(X=train_input, y=train_output)

X_test = [[10, 20, 30]]
outcome = predictor.predict(X=X_test)
coefficients = predictor.coef_

print("Prediction: " + str(outcome))
print("Coefficients: " + str(coefficients))
