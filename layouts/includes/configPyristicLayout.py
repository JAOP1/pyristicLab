import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app

import layouts.includes.Dependecies.baseClass as bc
from layouts.includes.params import _standardInputsEP,_operadoresEP,_standardInputsGA, _operadoresGA

class EPConfig(bc.BaseConfig):
    _id = "EP"
    _name = "Programación evolutiva"
    inputs =  _standardInputsEP #Entradas del algoritmo optimize.
    operands = _operadoresEP   #Configuración de operadores  (seleccion, cruza, mutacion).

    def callback(click, *userInputs):
        return {
                'algortimo': 'EP',\
                'seleccionSobrevivientes': 'selección más',\
                'mutacionSol': 'mutacionSigma',\
                'mutacionSigma': 'sigma_blah'}

class GAConfig(bc.BaseConfig):
    _id = "GA"
    _name = "Algoritmos genéticos"
    inputs = _standardInputsGA
    operands = _operadoresGA

    def callback(click, *userInputs):
        return {
                'algortimo': 'GA',\
                'seleccionSobrevivientes': 'seleccion mas',\
                'mutacionSol': 'blahMutacion',\
                'cruzaSol': 'blahCruza',\
                'seleccionPadres': 'blahSeleccion'
                }

# class EEConfig(bc.BaseConfig):
#     _id = "EE"
#     inputs = _standardInputsEE
#     operands = _operadoresEE

#     def callback(click, *userInputs):
#         return {
#                 'algortimo': 'EE',\
#                 'seleccionSobrevivientes': 'seleccion mas',\
#                 'mutacionSol': 'blahMutacion',\
#                 'cruzaSol': 'blahCruzaSol',\
#                 'mutacionSigma': 'blahMutacion',\
#                 'cruzaSigma': 'blahCruza',\
#                 }


class pyristicBoard(bc.Dashboard):
    _idConfigurations = ['EP']
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
# continuosAlgorithmsConfig = [EPConfig, EEConfig, GAConfig]
continuosAlgorithmsConfig = [EPConfig, GAConfig]

discreteAlgorithmsConfig = []