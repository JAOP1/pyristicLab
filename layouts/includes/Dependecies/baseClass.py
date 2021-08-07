from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from layouts.includes.Dependecies.utils import  form_group,\
                                        decimalFormat,\
                                        create_title,\
                                        create_control,\
                                        make_graph
import plotly.graph_objects as go
import plotly.express as px
from functools import partial
from pprint import pprint 
from typing import Union
import pandas as pd
import numpy as np
import json
import time

class operandConfig:
    def __init__(self,_id,description,inputs):
        self.inputs = inputs
        self.description = description
        self.id = _id
        self._idOptions = []
        self.setupControls()
        self.setupCallback()

    def getIdOptions(self):
        return self._idOptions

    def getDropdownId(self):
        return f'{self.id}-dropdown'

    def setupControls(self):
        dropdownSettings = {   
                'desc': self.description,\
                'dropdown':True,\
                'default': 0,\
                'options': [{'label': self.inputs[i]['label'], 'value': i} for i in range(len(self.inputs))]
                }
        # self.dropdown = [dbc.Alert(create_control(dropdownSettings, f'{self.id}-dropdown'), color="success")]
        self.dropdown = [create_control(dropdownSettings, f'{self.id}-dropdown')]
        self.dropdownDivs = []
    
        for i in range(len(self.inputs)):
            option = self.inputs[i]
            if(len(option['inputs']) == 0):
                self.dropdownDivs.append(html.Div(
                                            dbc.Alert(dcc.Markdown('¡Sin parámetros de entrada!'), color="info"),
                                            className='rounded-corners',
                                            id=f'{self.id}-{i}'
                                            ))
                continue
            self._idOptions += [f"{self.id}-{i}-{item['id']}" for item in option['inputs']]
            inputItems = [create_control(item,f"{self.id}-{i}-{item['id']}") for item in option['inputs']]
            self.dropdownDivs.append(html.Div(id=f'{self.id}-{i}',\
                        children =inputItems))

    def setupCallback(self):
        @app.callback(
            [Output( f'{self.id}-{i}', 'style') for i in range(len(self.inputs))],
            Input(self.getDropdownId(), 'value'),
            [State(f'{self.id}-{i}','style') for i in range(len(self.inputs))]
        )
        def displayContent(optionSelected,*containersStyles):
            size = len(containersStyles)
            styles = [{'display':'none'}] * size
            styles[optionSelected] = {}
            return  styles

    def getLayout(self):
        return [html.Div(self.dropdown + self.dropdownDivs, className='blue-left-line')]

class BaseConfig:
    @classmethod
    def setup(cls):
        cls._idInputs = []
        cls.setupControls()
        cls.setuplayout()
        cls.setupCallback()

    @classmethod
    def setupControls(cls):
        cls.controls = []
        for inp in cls.inputs:
            idInput = f"{cls._id}-{inp['id']}"
            cls.controls.append(create_control(inp, idInput))
            cls._idInputs.append(idInput)
        
        for i in range(len(cls.operands)):
            id_ = cls.operands[i]['id']
            desc_ = cls.operands[i]['desc']
            inputs_ = cls.operands[i]['items']
            cls.operands[i] = operandConfig(id_,desc_,inputs_)
        

    @classmethod
    def setupCallback(cls):
        @app.callback(
            Output(f"collapse-{cls._id}", "is_open"),
            [Input(f"group-{cls._id}-toggle", "n_clicks")],
            [State(f"collapse-{cls._id}", "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        idsDropdown = []
        idsOptions = []
        for operand in cls.operands:
            idsDropdown.append(State(operand.getDropdownId(),'value'))
            idsOptions += [State(idInput,'value') for idInput in operand.getIdOptions()]

        app.callback(
            Output(f'{cls._id}-storage','data'),
            Input(f'{cls._id}-button','n_clicks'),
            [State(idInput,'value') for idInput in cls._idInputs] + 
            idsDropdown + 
            idsOptions
        )(cls.callback)
        
    @classmethod
    def setuplayout(cls):
        cls.content_layout = []
        additionalFeatures = []
        storageConfig = [dcc.Store(id=f'{cls._id}-storage')]

        for operand in cls.operands:
            additionalFeatures += operand.getLayout()

        ExecuteButton = [html.Div(
                                dbc.Button(
                                    f'Ejecutar {cls._id}',\
                                    color="info",\
                                    outline=True,\
                                    id=f"{cls._id}-button"),\
                                className='text-center')]
        cls.content_layout.append(dbc.Card(
            [
                dbc.CardHeader(
                    html.H2(
                        dbc.Button(
                            cls._name,
                            id=f"group-{cls._id}-toggle",
                            color='warning',
                            block=True
                        )
                    )
                ),
                dbc.Collapse(
                    dbc.CardBody(storageConfig + cls.controls + additionalFeatures + ExecuteButton,
                        className='toggle-display'
                    ),
                    id=f"collapse-{cls._id}",
                )
            ],
            color="warning"
        ))

    
    @classmethod
    def layout(cls):
        return cls.content_layout

class Dashboard:
    
    @classmethod
    def setup(cls):
        cls.setupLayout()
        cls.setupCallback()

    @classmethod
    def setupLayout(cls):
        cls.graph_layout = dbc.Container(
                    dcc.Loading(
                        dcc.Graph(id=f"graph", 
                            style={"height": "500px"},
                            config={'displaylogo': False}
                        )
                    )
                    , className='graph-box orange-left-line')

        content =[]
        for item in cls.statisticsBoxes:
            content.append(
                dbc.Col( 
                    dbc.Container(
                        [
                            dbc.Row(
                                [
                                    #Input value.
                                    dbc.Col(
                                        html.Div(
                                            [
                                                dbc.Spinner(html.H4('None',id=f"{item['id']}-value",style={'color':'#696969','paddingTop':'15px'}),color='warning'),
                                                html.Hr(className='dividersm'),
                                                html.P( f"{item['name']}",className='gray_text')
                                            ],style={'backgroundColor':'rgb(247, 249, 249)','height':'85.8px'}
                                            , className='left-rounded-corners text-center bottom-right-shadow'
                                        )
                                        ,lg = 9, md=9, sm=9, xs=9
                                    ),
                                    dbc.Col(
                                        html.Div(
                                        html.I(className=f"fas fa-chart-bar fa-3x setting-icon"),
                                        className='right-rounded-corners bottom-right-shadow',
                                        style={'backgroundColor':item['color'],'height':'85.8px'},
                                        )
                                        ,lg=3, md=3, sm=3,xs=3
                                    )
                                ]
                                , no_gutters=True
                            )
                        ]
                        ,style={'width':'280px'}
                    ),
                    lg=4, md=4, sm=12
                )
            )
        cls.outputBox_layout = dbc.Container(
                                    dbc.Row(content),
                                    style={'paddingBottom':'35px','maginTop':'100px'},
                                    fluid=True
                                )

    @classmethod
    def setupCallback(cls):
        items = [   ('graph','figure'), ('dashboard-title','children')]
        items += [(f"{element['id']}-value",'children') for element in  cls.statisticsBoxes]
        
        app.callback(
            [Output(itemName, itemUpdate) for itemName, itemUpdate in items],
            [Input(f'{metaId}-button','n_clicks') for metaId in cls._idConfigurations],
            [State(f'{metaId}-storage', 'data') for metaId in cls._idConfigurations],
            prevent_initial_call=True
        )(cls.callback)

    @classmethod
    def layout(cls):
        layout_content = [create_title('Metaheurística: No seleccionada',_id='dashboard-title')]
        layout_content.append(cls.outputBox_layout)
        layout_content.append(cls.graph_layout)
        return [html.Div(layout_content, style={'marginTop': '50px'})]

class SidebarOptions:

    def __init__(self, options, id = 'sidebar'):
        self.id = id    
        self.options = options

    def setup(self):
        self.setupLayout()
        self.setupCallback()

    def setupLayout(self):
        controlSettings={   
                            'desc': "Tipo de problema de optimización:",\
                            'dropdown':True,\
                            'default': 0,\
                            'options': [{'label': self.options[i]['label'], 'value': i} for i in range(len(self.options))]
                        }
        controlStats = {
                        "id": "metaheuristicTimes", 
                        "name": "metaheuristicTimes",
                        "desc": "Número de ejecuciones metaheurística:", 
                        "default": 10,
                        "step":1,
                        "min": 1
                        }
        self.close = html.Div(html.Button(html.I(className="fas fa-angle-left"),className='gear-button', id='closeSidebar'), className='closebtn')
        self.optimizationTimes = create_control(controlStats,'optimization-time')
        self.optimizationType = create_control(controlSettings, 'optimization-type')
        self.storage = dcc.Store(id=f'general-storage')
        self.containerOptions = []
        for i in range(len(self.options)):
            if self.options[i]['layout_items'] == []:
                self.containerOptions.append(html.Div(
                                            dbc.Alert([ html.I(className="fas fa-info-circle fa-3x"),
                                                        html.Br(),
                                                        html.P("Sin algoritmos para mostrar.")], 
                                                        className='rounded-corners',
                                                        color="info"),
                                            id=f'sidebar-{i}-content',
                                            ))
                continue
            self.containerOptions.append(html.Div(id=f'sidebar-{i}-content', children=self.options[i]['layout_items'],  className="accordion"))
        # self.containerOptions = [ for i in range(len(self.options))]

    def setupCallback(self):
        print("Entra aqui")
        @app.callback(
            [Output( f'sidebar-{i}-content', 'style') for i in range(len(self.options))] + [Output('general-storage','data')],
            Input('optimization-type', 'value'),
            [State( f'sidebar-{i}-content', 'style') for i in range(len(self.options))]+ [State('optimization-time','value')]
        )
        def callback(option, *states):
            numOptimizationDivs = len(states)-1
            styles = [{'display':'none'}] * numOptimizationDivs
            print(option)
            styles[option] = {}
            styles.append({
                'executions': states[-1]
                })
            return  styles

    def layout(self):
        layout = []
        # layout += self.storage 
        layout += [self.close , self.storage, self.optimizationTimes, self.optimizationType] 
        layout += self.containerOptions
        
        return layout