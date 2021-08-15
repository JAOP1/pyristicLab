import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import copy
from layouts.includes.Dependecies.utils import make_graph, getInputByContainerOption
import layouts.includes.Dependecies.baseClass as bc
from layouts.includes.params import _standardInputsEP,\
                                    _operadoresEP,\
                                    _standardInputsGA,\
                                    _operadoresGA,\
                                    _standardInputsES,\
                                    _operadoresES,\
                                    getOperands

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
    print(dictInputs)
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
        saveLabels = [  'generation', 'parents',\
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

    def callback(optionEP,optionEE, optionGA, *data):
        ctx = dash.callback_context
        _id = ctx.triggered[0]['prop_id'].split('.')[0]   
        fig = make_graph([1,2,3,4],[1,2,3,4],'Ejemplo',[[2,3],[2,3]],dict(title='Número de ejecución'),dict(title='Mejor punto obtenido'))
        return fig,'Metaheurística: Funciona.',-1,-1,-1

continuosAlgorithmsConfig = [EPConfig, EEConfig, GAConfig]
discreteAlgorithmsConfig = []