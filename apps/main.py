from models.PowerGrid import PowerGrid
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output, Dash
from apps.dataParse import *
from apps.templates import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)',

        }
    },
    {
        'selector': 'edge',
        'style': {
            'label': 'data(label)',
            'curve-style': 'bezier',
            'source-arrow-shape': 'triangle',
            'arrow-scale': 2,
        }
    },
    {
        'selector': '.green',
        'style': {
            'background-color': 'green',
        }
    },
    {
        'selector': '.red',
        'style': {
            'background-color': 'red',
        }
    },
]
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'width': '30%',
        'height': '50px'
    }
}

app.layout = html.Div([html.Div([html.H1("Power Grid Analysis")], style={'textAlign': "center"}),

                       dcc.Slider(1, 24, 1,
                                  value=12,
                                  id='my-slider'
                                  ),


                       cyto.Cytoscape(
                           id='cytoscape-callbacks-1',
                           elements=[],
                           style={'width': '100%', 'height': '700px'},
                           layout={
                                'name': 'breadthfirst',
                           },
                           stylesheet=default_stylesheet
                       ),
                        html.P(id='cytoscape-tapNodeData-output'),
                        html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre'])
                       ])

@app.callback(
    Output('cytoscape-callbacks-1', 'elements'),
    Input('my-slider', 'value')
)
def hourUpdate(value):

    dataSet = getData(value)
    powerGrid = PowerGrid(dataSet)

    nodes = [
        {
            'data': {'id': short, 'label': label},
            'grabbable': False,
            'classes': color
        }
        for short, label, color in (
            prepNodes(dataSet[0])
        )
    ]


    edges = [
        {'data': {'id': source + target, 'source': source, 'target': target, 'label': label}}
        for target, source, label in (
            prepBranches(dataSet[1])
        )
    ]
    return nodes + edges


@app.callback(Output('cytoscape-tapNodeData-json', 'children'),
              Input('cytoscape-callbacks-1', 'tapNodeData'))
def displayTapNodeData(data):
    return format(data)



@app.callback(Output('cytoscape-callbacks-1', 'stylesheet'),
              Input('cytoscape-callbacks-1', 'tapNodeData'),
              )
def displayTapNodeData(data):
    id_ = data['id']
    new_style = [{
        'selector': f'[source = "{id_}"]',
        'style': {
            'line-color': 'green',
            'arrow-scale': 3,
            'source-arrow-color': 'green'
        }
    },
        {
            'selector': f'[target = "{id_}"]',
            'style': {
                'line-color': 'red',
                'arrow-scale': 3,
                'source-arrow-color': 'red'
            }
        },
        {
            'selector': f'[id = "{id_}"]',
            'style': {
                'background-color': 'blue',
            }
        }
    ]
    return default_stylesheet + new_style


