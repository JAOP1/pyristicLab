import pyristic.utils.test_function as pcTF
import numpy as np

# Ackley example.
optimizationProblem = pcTF.ackley_

def aptitudeFunction(X: np.array) -> np.array:
    return -1 * optimizationProblem['function'](X)

#Beale example.
# optimizationProblem = pcTF.beale_

# def aptitudeFunction(X: np.array) -> np.array:
#     return 1 / (optimizationProblem['function'](X) +1)