import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import copy
from layouts.includes.utils import make_graph, getInputByContainerOption, decimalFormat
import layouts.includes.baseClass as bc
from layouts.params import _standardInputsEP,\
                                    _operadoresEP,\
                                    _standardInputsGA,\
                                    _operadoresGA,\
                                    _standardInputsES,\
                                    _operadoresES,\
                                    getOperands
import layouts.dummyCreateConfig as dm
from testFile import optimizationProblem, aptitudeFunction
import numpy as np
import pandas as pd
from pyristic.heuristic.EvolutiveProgramming_search import EvolutionaryProgramming
from pyristic.heuristic.EvolutionStrategy_search import EvolutionStrategy
from pyristic.heuristic.GeneticAlgorithm_search import Genetic
from pyristic.utils.helpers import get_stats


def getIndexByName(name):
    indexDict = {_name: i for i, _name in enumerate(['EP','EE','GA'])}
    return indexDict[name]

def createDataInput(userInputs, saveLabels, algorithm, firstDropdown, startInput):
    dictInputs = {}
    dictInputs['algorithm'] = algorithm
    for i in range(len(saveLabels)):
        dictInputs[saveLabels[i]] = userInputs[i]

    operadores = getOperands(algorithm)
    labels = saveLabels[firstDropdown:]
    end = startInput
    for i in range(len(labels)):
        array_ = getInputByContainerOption(operadores[i])
        indL,indR = array_[userInputs[firstDropdown+i]]
        dictInputs[f'{labels[i]}Params'] = userInputs[end+ indL : end + indR]
        end += array_[-1][-1]
    # print(dictInputs)
    return dictInputs

class EPConfig(bc.BaseConfig):
    _id = "EP"
    _name = "Programación evolutiva"
    inputs =  _standardInputsEP #Entradas del algoritmo optimize.
    operands = copy.deepcopy(_operadoresEP)   #Configuración de operadores  (seleccion, cruza, mutacion).

    def callback(click, *userInputs):
        saveLabels = ['generation','parents','mutationX','mutationSigma','survivorSelection']
        return createDataInput(userInputs, saveLabels, 'EP', 2, 5)

class GAConfig(bc.BaseConfig):
    _id = "GA"
    _name = "Algoritmos genéticos"
    inputs = _standardInputsGA
    operands = copy.deepcopy(_operadoresGA)

    def callback(click, *userInputs):
        saveLabels = [  'generations', 'parents',\
                        'parentSelection', 'crossoverX',\
                        'mutationX', 'survivorSelection'
                    ]
        return createDataInput(userInputs, saveLabels, 'GA', 2, 6)

class EEConfig(bc.BaseConfig):
    _id = "EE"
    _name = "Estrategias evolutivas"
    inputs = _standardInputsES
    operands = copy.deepcopy(_operadoresES)

    def callback(click, *userInputs):
        saveLabels  = [ 'generations', 'parents',\
                        'offsprings','epsilonSigma',\
                        'crossoverX','mutationX',\
                        'crossoverSigma','mutationSigma',\
                        'survivorSelection'
                    ]
        return createDataInput(userInputs,saveLabels, 'EE',4,9)

class pyristicBoard(bc.Dashboard):
    _id = "heuristic"
    _idConfigurations = ['EP','EE','GA']
    statisticsBoxes = [{
                            'id': 'average',\
                            'color':'orange',\
                            'name':'promedio',\
                        },
                        {
                            'id':'median',\
                            'color':'#e67e22',\
                            'name':'mediana'
                        },
                        {
                            'id':'std',\
                            'color':'#0b8c2b',\
                            'name':'Desviación estandar'
                        }]


    def callback(*data):
        ctx = dash.callback_context
        _id = ctx.triggered[0]['prop_id'].split('.')[0].split('-')[0] 
        configurationSaved = data[getIndexByName(_id)]
        numExecutions = data[-1]

        if _id == 'EP':
            configuration = dm.dummyCreateConfigEP(configurationSaved)
            args = (configurationSaved['generation'],\
                    configurationSaved['parents'],False)
            optimizationClass =  EvolutionaryProgramming(
                                    function= aptitudeFunction,\
                                    decision_variables=optimizationProblem['decision_variables'],\
                                    constraints= optimizationProblem['constraints'],\
                                    bounds= optimizationProblem['bounds'],\
                                    config=configuration)
        
        elif _id == 'EE':
            configuration = dm.dummyCreateConfigEE(configurationSaved)
            args = (configurationSaved['generations'],\
                    configurationSaved['parents'],\
                    configurationSaved['offsprings'],\
                    configurationSaved['epsilonSigma'],False)
            optimizationClass =  EvolutionStrategy(
                                    function= aptitudeFunction,\
                                    decision_variables=optimizationProblem['decision_variables'],\
                                    constraints= optimizationProblem['constraints'],\
                                    bounds= optimizationProblem['bounds'],\
                                    config=configuration)

        elif _id == 'GA':
            configuration = dm.dummyCreateConfigGA(configurationSaved)
            args = (configurationSaved['generations'],\
                    configurationSaved['parents'],1.0 ,False)
            optimizationClass =  Genetic(
                                    function= aptitudeFunction,\
                                    decision_variables=optimizationProblem['decision_variables'],\
                                    constraints= optimizationProblem['constraints'],\
                                    bounds= optimizationProblem['bounds'],\
                                    config=configuration)
        print(configuration)
        statistics = get_stats(optimizationClass, numExecutions, args, transformer=optimizationProblem['function'])
        print(statistics)
        IndWorst = np.argmax(statistics['objectiveFunction'])
        IndBest = np.argmin(statistics['objectiveFunction'])
        fig = make_graph(list(range(numExecutions)),statistics['objectiveFunction'],\
                        'f(x)',[[IndWorst,IndBest],[statistics['Worst solution']['f'],statistics['Best solution']['f']]],\
                        dict(title='Número de ejecución'),dict(title='Valores resultantes de f(x)'))
        return fig,f'Metaheurística: {_id}', decimalFormat(statistics["averageTime"]), decimalFormat(statistics['Mean']), decimalFormat(statistics['Median']), decimalFormat(statistics['Standard deviation'])

    def callbackConfig(*data):
        ctx = dash.callback_context
        _id = ctx.triggered[0]['prop_id'].split('.')[0].split('-')[0] 
        configurationSaved = data[getIndexByName(_id)]
        names, options = [],[]
        if _id == 'EP':
            names, options = dm.getTableEP(configurationSaved)
        elif _id == 'EE':
            names, options = dm.getTableEE(configurationSaved)
        elif _id == 'GA':
            names, options = dm.getTableGA(configurationSaved)
        
        df = pd.DataFrame(
                {
                    "Configuración": names,
                    "Opción seleccionada": options,
                }
            )

        return  html.Div(dbc.Table.from_dataframe(df, striped=True, hover=True),style={'width':'160px'})

continuosAlgorithmsConfig = [EPConfig, EEConfig, GAConfig]
discreteAlgorithmsConfig = []