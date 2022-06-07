import random
import h5py
import numpy as np
from model.DataClass import Node
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output, Dash
from apps.PowerGridAnalysis import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


gridLayout = getGridLayout()[0]

nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20 * lat, 'y': -20 * long}
    }
    for short, label, long, lat in (
        prepNodes(gridLayout['nodes'])
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        prepBranches(gridLayout['branches'])
    )
]

elements = nodes + edges

app.layout = html.Div([html.Div([html.H1("Power Grid Analysis")], style={'textAlign': "center"}),

                        dcc.Slider(1, 24, 1,
                                   value=12,
                                   id='my-slider'
                                   ),
                        html.Div(id='slider-output-container'),

                        cyto.Cytoscape(
                            id='cytoscape-layout-9',
                            elements=elements,
                            style={'width': '100%', 'height': '700px'},
                            layout={
                                'name': 'cose'
                            }
                        )
                        ])


@app.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value'))
def update_output(value):
    return format(readData(value, hour_dict))