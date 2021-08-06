
"""
---------------------------------------------------------------------
                    Continuos Optimization Problems
---------------------------------------------------------------------
"""


"""
---------------------------------------------------------------------
                    GA configuration
---------------------------------------------------------------------
"""
_standardInputsGA = [
    {
        "id": "generaciones", 
        "desc": "Número de generaciones:", 
        "default": 10,
        "step": 1,
        "min": 1},
    {
        "id": "poblacionGeneracional", 
        "desc": "Tamaño de la población:",
        "default": 30,
        "step":1,
        "min":10
    }
]


_operadoresGA = [
     {
        'id': 'parentSelection',
        'desc': "Método de selección de padres:",
        'items': [
            {
                'label': 'roulette_sampler',
                'inputs':[]
            },
            {
                'label':'stochastic_universal_sampler',
                'inputs':[]
            },
            {
                'label':'deterministic_sampler',
                'inputs':[]
            },
            {
                'label':'tournament_sampler',
                'inputs':[
                    {
                        "id": "chunk", 
                        "desc": "Tamaño de grupos:", 
                        "default": 2,
                        "step": 1,
                        "min": 2   
                    },
                    {
                        "id": "prob", 
                        "desc": "Probabilidad de seleccionar al mejor:", 
                        "default": 0.5,
                        "step": 0.01,
                        "min": 0,
                        "max": 1   
                    }
                ]
            }
        ]
    },
    {
        'id':'crossOver',
        'desc':'Operador de cruza:',
        'items':[
            {
                'label': 'n_point_crossover',
                'inputs':[
                    {
                        "id": "nPoint", 
                        "desc": "Número de puntos de cruza:", 
                        "default": 1,
                        "step": 1,
                        "min": 1   
                    }
                ]
            },
            {
                'label':'uniform_crossover',
                'inputs':[
                    {
                        "id": "uniform", 
                        "desc": "Probabilidad de cruza:", 
                        "default": 0.5,
                        "step": 0.01,
                        "min": 0,
                        "max":1   
                    }
                ]
            },
            {
                'label':'simulated_binary_crossover',
                'inputs':[
                    {
                        "id": "simulatedBinary", 
                        "desc": "nc:", 
                        "default": 1  
                    }  
                ]

            }
        ]
    },
    {
        'id':'mutation',
        'desc': 'Operadores de mutación',
        'items':[
            {
                'label':'boundary_mutator',
                'inputs':[
                    {
                        "id": "boundInfBoundary", 
                        "desc": "Límite inferior:",
                        'default':0
                    },
                    {
                        "id": 'boundSupBoundary',
                        'desc':'Límite superior:',
                        'default':1
                    }   
                ]
            },
            {
                'label':'uniform_mutator',
                'inputs':[
                    {
                        "id": "boundInfUniform", 
                        "desc": "Límite inferior:",
                        'default':0  
                    },
                    {
                        "id": 'boundSupUniform',
                        'desc':'Límite superior:',
                        'default':1
                    }  
                ]
            },
            {
                'label':'non_uniform_mutator',
                'inputs':[
                    {
                        'id':'sigmaNonUniform',
                        'desc':'Valor de sigma:',
                        'default':1,
                        'min':0.01
                    }
                ]
            }
        ]
    },
    {
        'id':'survivorSelectionGA',
        'desc': 'Esquemas de selección:',
        'items':[
            {
                'label':'merge_selector',
                'inputs':[]
            },
            {
                'label':'replacement_selector',
                'inputs':[]
            }
        ]
    } 
]
"""
---------------------------------------------------------------------
                    ES configuration
---------------------------------------------------------------------
"""
_standardInputsES = [
    {
        "id": "generaciones", 
        "desc": "Número de generaciones:", 
        "default": 10,
        "step": 1,
        "min": 1},
    {
        "id": "poblacionGeneracional", 
        "desc": "Tamaño de la población padre:",
        "default": 30,
        "step":1,
        "min":10
    },
    {
        'id':'poblacionHijos',
        'desc':'Tamaño de la población hija:',
        'default':30,
        'step':1,
        'min':10
    },
    {
        'id':'epsilonSigma',
        'desc':'Mínimo valor aceptado sigma:',
        'default':0.001,
        'min':0,
        'step':0.01
    }
]

_operadoresES = [
    {
        'id': 'crossoverSolES',
        'desc': "Operadores de cruza para la solución:",
        'items': [

        ]
    },
    {
        'id':'mutationSolES',
        'desc':'Operadores de mutación para la solución:',
        'items': []
    },
    {
        'id':'crossoverSigmaES',
        'desc':'Operadores de cruza para los sigma:',
        'items':[]
    },
    {
        'id':'mutationSigmaES',
        'desc': 'Operadores de mutación para los sigma:',
        'items':[]
    },
    {
        'id':'survivorSelectionES',
        'desc':'Esquema de selección de sobrevivientes:',
        'items': [
            {
                'label':'merge_selector',
                'inputs':[]
            },
            {
                'label':'replacement_selector',
                'inputs':[]
            }
        ]
    }
]

"""
---------------------------------------------------------------------
                    EP configuration
---------------------------------------------------------------------
"""
_standardInputsEP = [
    {
        "id": "generaciones", 
        "desc": "Número de generaciones:", 
        "default": 10,
        "step": 1,
        "min": 1},
    {
        "id": "poblacionGeneracional", 
        "desc": "Tamaño de la población:",
        "default": 30,
        "step":1,
        "min":10
    }
]

_operadoresEP = [
    {
        'id': 'operadorMutacionX',
        'desc': "Operadores de mutación en la solución X:",
        'items': [
            {
                'label': 'sigma_mutator',
                'inputs':[]
            }
        ]
    },
    {
        'id': 'operadorMutacionSigma',
        'desc': "Operadores de mutación en la variable de sigma: ",
        'items': [
            {
                'label': "sigma_ep_adaptive_mutator",
                'inputs':[
                    {
                        "id": "alpha", 
                        "desc": "Valor alpha:", 
                        "default": 0.5,
                        "step": 0.01,
                        "min": 0,
                        "max": 1   
                    },
                    {
                        "id": "decisionVariables",
                        "desc": "Número de variables de decisión:",
                        "default": 2,
                        "step":1,
                        "min":1
                    }
                ]
                
            } 
        ]
    },
    {
        'id':'survivorSelectionPE',
        'desc': 'Esquemas de selección:',
        'items':[
            {
                'label':'merge_selector',
                'inputs':[]
            },
            {
                'label':'replacement_selector',
                'inputs':[]
            }
        ]
    } 
]