import pyristic.utils.operators.selection as pcSelection
import pyristic.utils.operators.mutation as pcMutation
import pyristic.utils.operators.crossover as  pcCrossover
from pyristic.utils.helpers import  EvolutionaryProgrammingConfig,\
                                    GeneticConfig,\
                                    EvolutionStrategyConfig,\
                                    ContinuosFixer
from testFile import aptitudeFunction, optimizationProblem


def dummyCreateConfigEP(configuration_:dict):
    configOptimizer = EvolutionaryProgrammingConfig()
    #Operator for X.
    if configuration_['mutationX'] == 0:
        configOptimizer.mutate(pcMutation.sigma_mutator())
    
    #Operator for sigma.
    if configuration_['mutationSigma'] == 0:
        configOptimizer.adaptive_mutation(pcMutation.sigma_ep_adaptive_mutator(optimizationProblem['decision_variables'],*configuration_['mutationSigmaParams']))

    #Survivor selection.
    if configuration_['survivorSelection'] == 0:
        configOptimizer.survivor_selection(pcSelection.merge_selector())
    elif configuration_['survivorSelection'] == 1:
        configOptimizer.survivor_selection(pcSelection.replacement_selector())
    
    return configOptimizer

def dummyCreateConfigEE(configuration_: dict):
    configOptimizer = EvolutionStrategyConfig()
    #Operator for crossover X.
    if configuration_['crossoverX'] == 0:
        configOptimizer.cross(pcCrossover.discrete_crossover())
    elif configuration_['crossoverX'] == 1:
        configOptimizer.cross(pcCrossover.intermediate_crossover(*configuration_['crossoverXParams']))
    #Operator for mutation X.
    if configuration_['mutationX'] == 0:
        configOptimizer.mutate(pcMutation.sigma_mutator())

    #Operator for crossover Sigma.
    if configuration_['crossoverSigma'] == 0:
        configOptimizer.adaptive_crossover(pcCrossover.discrete_crossover())
    elif configuration_['crossoverSigma'] == 1:
        configOptimizer.adaptive_crossover(pcCrossover.intermediate_crossover(*configuration_['crossoverXParams']))
    
    #Operator for mutation sigma.
    if configuration_['mutationSigma'] == 0:
        configOptimizer.adaptive_mutation(pcMutation.single_sigma_adaptive_mutator(optimizationProblem['decision_variables']))
    elif configuration_['mutationSigma'] == 1:
        configOptimizer.adaptive_mutation(pcMutation.mult_sigma_adaptive_mutator(optimizationProblem['decision_variables']))

    #Survivor selection.
    if configuration_['survivorSelection'] == 0:
        configOptimizer.survivor_selection(pcSelection.merge_selector())
    elif configuration_['survivorSelection'] == 1:
        configOptimizer.survivor_selection(pcSelection.replacement_selector())
    
    return configOptimizer
    
def dummyCreateConfigGA(configuration_: dict):
    print(configuration_)
    configOptimizer = GeneticConfig()
    #Operator for selection.
    parameters = [aptitudeFunction] + configuration_['parentSelectionParams']
    if configuration_['parentSelection'] == 0:
        configOptimizer.parent_selection(pcSelection.roulette_sampler(*parameters))
    elif configuration_['parentSelection'] == 1:
        configOptimizer.parent_selection(pcSelection.stochastic_universal_sampler(*parameters))
    elif configuration_['parentSelection'] == 2:
        configOptimizer.parent_selection(pcSelection.deterministic_sampler(*parameters))
    elif configuration_['parentSelection'] == 3:
        configOptimizer.parent_selection(pcSelection.tournament_sampler(*parameters))

    #Operator for crossover X.
    if configuration_['crossoverX'] == 0:
        configOptimizer.cross(pcCrossover.n_point_crossover(*configuration_['crossoverXParams']))
    elif configuration_['crossoverX'] == 1:
        configOptimizer.cross(pcCrossover.uniform_crossover(*configuration_['crossoverXParams']))
    elif configuration_['crossoverX'] == 2:
        configOptimizer.cross(pcCrossover.simulated_binary_crossover(*configuration_['crossoverXParams']))
    elif configuration_['crossoverX'] == 3:
        configOptimizer.cross(pcCrossover.discrete_crossover())
    elif configuration_['crossoverX'] == 4:
        configOptimizer.cross(pcCrossover.intermediate_crossover(*configuration_['crossoverXParams']))
    #Operator for mutation X.
    if configuration_['mutationX'] == 0:
        configOptimizer.mutate(pcMutation.boundary_mutator(optimizationProblem['bounds']))
    elif configuration_['mutationX'] == 1:
        configOptimizer.mutate(pcMutation.uniform_mutator(optimizationProblem['bounds']))
    elif configuration_['mutationX'] == 2:
        configOptimizer.mutate(pcMutation.non_uniform_mutator(*configuration_['mutationXParams']))

    #Survivor selection.
    if configuration_['survivorSelection'] == 0:
        configOptimizer.survivor_selection(pcSelection.merge_selector())
    elif configuration_['survivorSelection'] == 1:
        configOptimizer.survivor_selection(pcSelection.replacement_selector())
    configOptimizer.fixer_invalide_solutions(ContinuosFixer(optimizationProblem['bounds']))
    return configOptimizer



def getTableEP(configuration_: dict):
    names =[
                'Operador de mutación en X', 'Operador de mutación sigma',\
                'Selección de sobrevivientes'
            ]
    options = []
    #Operator for X.
    if configuration_['mutationX'] == 0:
        options.append('sigma_mutator')
    
    #Operator for sigma.
    if configuration_['mutationSigma'] == 0:
        options.append('sigma_ep_adaptive_mutator')

    #Survivor selection.
    if configuration_['survivorSelection'] == 0:
        options.append('merge_selector')
    elif configuration_['survivorSelection'] == 1:
        options.append('replacement_selector')
    
    return names, options

def getTableEE(configuration_: dict):
    names = [  
                'Operador de cruza en X', 'Operador de cruza en Sigma',\
                'Operador de mutación en X', 'Operador de mutación sigma',\
                'Selección de sobrevivientes'
            ]
    options = []
    #Operator for crossover X.
    if configuration_['crossoverX'] == 0:
        options.append('discrete_crossover')
    elif configuration_['crossoverX'] == 1:
        options.append('intermediate_crossover')
    #Operator for mutation X.
    if configuration_['mutationX'] == 0:
        options.append('sigma_mutator')

    #Operator for crossover Sigma.
    if configuration_['crossoverSigma'] == 0:
        options.append('discrete_crossover')
    elif configuration_['crossoverSigma'] == 1:
        options.append('intermediate_crossover')
    
    #Operator for mutation sigma.
    if configuration_['mutationSigma'] == 0:
        options.append('single_sigma_adaptive_mutator')
    elif configuration_['mutationSigma'] == 1:
        options.append('mult_sigma_adaptive_mutator')

    #Survivor selection.
    if configuration_['survivorSelection'] == 0:
        options.append('merge_selector')
    elif configuration_['survivorSelection'] == 1:
        options.append('replacement_selector')
    
    return names, options


def getTableGA(configuration_: dict):
    names = [   
                'Selección de padres', 'Operador de cruza en X',\
                'Operador de mutación en X', 'Selección de sobrevivientes'
            ]
    options = []

    #Operator for selection.
    if configuration_['parentSelection'] == 0:
        options.append('Método de la Ruleta')
    elif configuration_['parentSelection'] == 1:
        options.append('Estocástica universal')
    elif configuration_['parentSelection'] == 2:
        options.append('Método determinista')
    elif configuration_['parentSelection'] == 3:
        options.append('Selección por torneo')

    #Operator for crossover X.
    if configuration_['crossoverX'] == 0:
        options.append('Cruza de N puntos')
    elif configuration_['crossoverX'] == 1:
        options.append('Cruza uniforme')
    elif configuration_['crossoverX'] == 2:
        options.append('Cruza binaria simulada')
    elif configuration_['crossoverX'] == 3:
        options.append('Cruza discreta')
    elif configuration_['crossoverX'] == 4:
        options.append('Cruza intermedia')
    #Operator for mutation X.
    if configuration_['mutationX'] == 0:
        options.append('boundary mutator')
    elif configuration_['mutationX'] == 1:
        options.append('uniform mutator')
    elif configuration_['mutationX'] == 2:
        options.append('non uniform mutator')

    #Survivor selection.
    if configuration_['survivorSelection'] == 0:
        options.append('Merge selector')
    elif configuration_['survivorSelection'] == 1:
        options.append('Replacement selector')
    
    return names, options
