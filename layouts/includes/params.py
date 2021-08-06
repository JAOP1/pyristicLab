
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
# _standardInputsGA = [

# ]

# _crossOptionsGA = [
#     {
#         'label': ,
#         'value': ,
#         'inputs': [{} ,{}]
#     },
#     {
#         'label': ,
#         'value': ,
#         'inputs': []
#     }
# ]

# _mutationOptionsGA = [
#     {
#         'label': ,
#         'value': ,
#         'inputs': []
#     },
#     {
#         'label': ,
#         'value': ,
#         'inputs': []
#     }
# ]

"""
---------------------------------------------------------------------
                    ES configuration
---------------------------------------------------------------------
"""
# _standardInputsES = [
#     {

#     }
# ]

# _crossOptionsES = [
#     {
#         'label': ,
#         'value': ,
#         'inputs': [{} ,{}]
#     },
#     {
#         'label': ,
#         'value': ,
#         'inputs': [{} ,{}]
#     }
# ]

# _mutationOptionES = [
#     {
#         'label': ,
#         'value': ,
#         'inputs': [{} ,{}]
#     },
#     {
#         'label': ,
#         'value': ,
#         'inputs': [{} ,{}]
#     }
# ]

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
    }
]