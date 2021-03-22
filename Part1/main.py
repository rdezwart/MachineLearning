# Title: Final Project - Part 1
# Author: Robin de Zwart, MachineLearning42
# Date: Mar 19, 2021
# Purpose: Generating a training set

# -- Imports -- #

import random


# -- Functions -- #

def generate_training_set(t_min, t_max):
    ret = []
    for i in range(100):
        ret.append([
            random.randint(t_min, t_max),
            random.randint(t_min, t_max),
            random.randint(t_min, t_max)
        ])
    return ret


# -- Code -- #

training_set = generate_training_set(0, 1000)

print(training_set)
