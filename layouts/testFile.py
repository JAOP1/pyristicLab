import pyristic.utils.test_function as pcTF
import numpy as np

optimizationProblem = pcTF.beale_

def aptitudeFunction(population_f: np.array) -> np.array:
    return 1/ (population_f+1)
