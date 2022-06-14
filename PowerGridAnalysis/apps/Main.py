from models.PowerGrid import PowerGrid
from models.Colors import Colors
from dash import html, dcc, Input, Output, Dash, dash_table
from apps.DataParse import *
from apps.Templates import *
from collections import namedtuple
from guppy import hpy


import dash_cytoscape as cyto
import base64

h = hpy()

print(h.heap())
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([html.H3("Power Grid Analysis")], style={'textAlign': "center"}),

    html.Div([html.P("Hour: ", className='six columns'),
              html.P("Amount of clusters:", className='three columns')],
             style={'textAlign': "center"},
             className='row'),

    html.Div([
        dcc.Slider(1, 24, 1,
                   value=12,
                   id='my-slider',
                   className='six columns'
                   ),

        dcc.Slider(1, 10, 1,
                   value=1,
                   id='cluster-slider',
                   className='three columns'
                   ),

        dcc.Upload(id='upload-data',
                   children=html.Div([
                       'Drag and drop or',
                       html.A(' select file')
                   ]),
                   style={
                       'width': '20%',
                       'height': '60px',
                       'lineHeight': '60px',
                       'borderWidth': '1px',
                       'borderStyle': 'dashed',
                       'borderRadius': '5px',
                       'textAlign': 'center',
                       'margin': '10px'
                   },
                   className='two columns'
                   )], className='row'),

    html.Div([
        cyto.Cytoscape(
            id='cytoscape-callbacks-1',
            elements=[],
            style={'width': '80%', 'height': '500px'},
            layout={
                'name': 'breadthfirst'
            },
            responsive=True,
            zoom=100,
            userZoomingEnabled=False,
            userPanningEnabled=False,
            stylesheet=default_stylesheet,
            className='nine columns'
        ),
        dash_table.DataTable(
            id='clusterData',
            style_table={'width': '15%'},
            columns=[{'id': 'Cluster number', 'name': 'Cluster number'}, {'id': 'Max', 'name': 'Max'},
                     {'id': 'Min', 'name': 'Min'}]
        ),
        dash_table.DataTable(
            id='nodeData',
            style_table={'width': '15%'},
            columns=[{'id': 'Node Id', 'name': 'Node Id'}, {'id': 'Node Type', 'name': 'Node Type'},
                     {'id': 'Node Demand', 'name': 'Node Demand'}]
        )
    ], className='row'),

    html.Div([
        html.P("Legend: ", className='six columns'),
        html.P("Genreators:", className='six columns')],
        style={'textAlign': "center"},
        className='row'),

    html.Div([
        cyto.Cytoscape(
            id='cytoscape-legend',
            elements=[
                {'data': {'id': 'one', 'label': 'Power Balance < 0'}, 'classes': 'red'},
                {'data': {'id': 'two', 'label': 'Power Balance = 0'}, 'classes': 'green'},
                {'data': {'id': 'three', 'label': 'Node with generator'}, 'classes': 'generator'},
                {'data': {'source': 'one', 'target': 'two', 'label': 'Power flow'}}
            ],
            stylesheet=default_stylesheet,
            style={'width': '50%', 'height': '100px'},
            layout={
                'name': 'grid'
            },
            userZoomingEnabled=False,
            userPanningEnabled=False,
            className='six columns'
        ),

        dash_table.DataTable(
            id='genCost',
            style_cell={'textAlign': 'center'},
            style_table={'width': '50%'}
        )

    ], className='row'),

    html.P("Unbalanced Nodes: ", style={'textAlign': "center"}, className='six columns'),

    html.Div([
        dash_table.DataTable(
            id='nodeTable',
            style_cell={'textAlign': 'center'},
            style_table={'width': '75%'}
        ),
    ], className='row'),
    dcc.Store(id='powerGrid')
], className='row',

)


@app.callback(
    [Output('cytoscape-callbacks-1', 'elements'),
     Output('clusterData', 'data'),
     Output('clusterData', 'style_data_conditional'),
     Output('powerGrid', 'data')
     ],
    [Input('my-slider', 'value'),
     Input('upload-data', 'contents'),
     Input('cluster-slider', 'value')]
)
def hourUpdate(value, content, nCluster):
    # get byte string from uploaded data
    if content:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        dataSet = getData(value, nCluster, decoded)
    # get data from default datafile
    else:
        dataSet = getData(value, nCluster)

    # Color List for n of clusters
    colorsList = Colors(nCluster).getColorList()

    # Object of Power Grid Class
    powerGrid = PowerGrid(dataSet, colorsList, nCluster)

    # Cytoscape Nodes
    nodes = powerGrid.prepNodes()

    # Cytoscape Edges
    edges = powerGrid.prepBranches()

    # Cluster Info
    clusterRows, style_data_conditional = powerGrid.clustersDataFrame(colorsList)

    # Generators info
    # genColumns, genRows = powerGrid.genrationPlotGenerators()

    # Node balance info
    # nodeColumns, nodeRows = powerGrid.prepNodeDataFrame()

    # Node stats
    # if data:
    #     dataRows = powerGrid.getNodeInfo(data['label'])
    # else:
    #     dataRows = []

    return nodes + edges, clusterRows, style_data_conditional, [dataSet, colorsList, nCluster]


# Generators info
@app.callback(
    [Output('genCost', 'columns'),
     Output('genCost', 'data')],
    Input('powerGrid', 'data')
)
def generatorsInfo(dataSet):
    powerGrid = PowerGrid(dataSet[0], dataSet[1], dataSet[2])
    genColumns, genRows = powerGrid.genrationPlotGenerators()
    return genColumns, [genRows]


# Node stats
@app.callback(
    Output('nodeData', 'data'),
    [Input('powerGrid', 'data'),
     Input('cytoscape-callbacks-1', 'mouseoverNodeData')]
)
def nodeStats(dataSet, data):
    powerGrid = PowerGrid(dataSet[0], dataSet[1], dataSet[2])
    # Node stats
    if data:
        dataRows = powerGrid.getNodeInfo(data['label'])
    else:
        dataRows = []
    return dataRows


# Node balance info
@app.callback(
    [Output('nodeTable', 'columns'),
     Output('nodeTable', 'data'), ],
    Input('powerGrid', 'data')
)
def nodesBalanceInfo(dataSet):
    powerGrid = PowerGrid(dataSet[0], dataSet[1], dataSet[2])
    nodeColumns, nodeRows = powerGrid.prepNodeDataFrame()
    return nodeColumns, [nodeRows],


@app.callback(
    Output('cytoscape-callbacks-1', 'stylesheet'),
    Input('cytoscape-callbacks-1', 'tapNodeData'),
    Input('cluster-slider', 'value'),
)
def displayTapNodeData(data, value):
    # Node specific information
    if value != 1:
        data = None
    if data:
        val = data['id']
        new_style = [{
            'selector': f'[source = "{val}"]',
            'style': {
                'line-color': 'green',
                'arrow-scale': 3,
                'target-arrow-color': 'green'
            }
        },
            {
                'selector': f'[target = "{val}"]',
                'style': {
                    'line-color': 'red',
                    'arrow-scale': 3,
                    'target-arrow-color': 'red'
                }
            },
            {
                'selector': f'[id = "{val}"]',
                'style': {
                    'background-color': 'blue',
                }
            }
        ]
        return default_stylesheet + new_style
    else:
        return default_stylesheet


def customStudentDecoder(gridDict):
    return namedtuple('X', gridDict.keys())(*gridDict.values())
