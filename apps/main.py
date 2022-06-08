
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output, Dash
from apps.PowerGridAnalysis import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}



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
                       ])


@app.callback(Output('cytoscape-callbacks-1', 'stylesheet'),
              Input('cytoscape-callbacks-1', 'tapNodeData'),
              )
def displayTapNodeData(data):
    id_=data['id']
    print(data)
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
    }
    ]
    return default_stylesheet + new_style

@app.callback(
    Output('cytoscape-callbacks-1', 'elements'),
    Input('my-slider', 'value')
)
def hourUpdate(value):

    gridLayout = getGridLayout(value)[0]

    nodes = [
        {
            'data': {'id': short, 'label': label},
            'grabbable': False,
            'classes': color
        }
        for short, label, color in (
            prepNodes(gridLayout['nodes'])
        )
    ]

    edges = [
        {'data': {'id': source + target, 'source': source, 'target': target, 'label': label}}
        for source, target, label in (
            prepBranches(gridLayout['branches'])
        )
    ]
    return nodes + edges
