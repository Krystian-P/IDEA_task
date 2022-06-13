from models.PowerGrid import PowerGrid
from models.Colors import Colors
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output, Dash, dash_table
from apps.dataParse import *

import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
powerGrid = None
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
            'line-color': 'data(color)',
            'curve-style': 'bezier',
            'source-arrow-shape': 'triangle',
            'arrow-color': 'data(color)',
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
    {
        'selector': '.blue',
        'style': {
            'background-color': 'blue',
        }
    },
    {
        'selector': '.triangle',
        'style': {
            'shape': 'triangle',
        }
    }
]
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'width': '30%',
        'height': '50px'
    }
}

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
        
        dcc.Slider(1, 15, 1,
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
                       'width': '15%',
                       'height': '60px',
                       'lineHeight': '60px',
                       'borderWidth': '1px',
                       'borderStyle': 'dashed',
                       'borderRadius': '5px',
                       'textAlign': 'center',
                       'margin': '10px'
                   },
                   className='two columns'
                   )
    ], className='row'),
    
    html.Div([
        cyto.Cytoscape(
            id='cytoscape-callbacks-1',
            elements=[],
            style={'width': '80%', 'height': '570px'},
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
            style_table={'width': '20%'}
        )
    ], className='row'),
    
    html.Div([
        html.P("Legend: ", className='six columns'),
        html.P("Genreators:", className='six columns')],
        style={'textAlign': "center"},
        className='row'),
    
    html.Div(   
        cyto.Cytoscape(
            id='cytoscape-legend',
            elements=[
                {'data': {'id': 'one', 'label': 'nr. węzła \n Power Balance < 0', 'classes': 'red'},
                {'data': {'id': 'one', 'label': 'nr. węzła \n Power Balance > 0', 'classes': 'green'},
                {'data': {'id': 'one', 'label': 'nr. węzła \n Power Balance = 0', 'classes': 'blue'},
                {'data': {'id': 'one', 'label': 'nr. węzła \n Node with generator', 'classes': 'triangle'},
                {'data': {'source': 'one', 'target': 'two', 'label': 'Power flow'}}
            ],
            style={'width': '50%', 'height': '100px'},
            layout={
                'name': 'grid'
            },
            responsive=True,
            zoom=100,
            userZoomingEnabled=False,
            userPanningEnabled=False,
            stylesheet=default_stylesheet
        ),
             
        dash_table.DataTable(
            id='genCost',
            style_cell={'textAlign': 'center'},
            style_table={'width': '50%'}
        ),
        html.P(id='cytoscape-mouseoverNodeData-output'),
        ], className='row'),
             
    html.P("Nodes balance: ", style={'textAlign': "center"}),
             
    html.Div([
        dash_table.DataTable(
            id='nodeTable',
            style_cell={'textAlign': 'center'},
        ),
    ], className='row'),

], className='row')


@app.callback(
    [Output('cytoscape-callbacks-1', 'elements'),
     Output('genCost', 'columns'),
     Output('genCost', 'data'),
     Output('nodeTable', 'columns'),
     Output('nodeTable', 'data'),
     Output('clusterData', 'columns'),
     Output('clusterData', 'data'),
     Output('clusterData', 'style_data_conditional'),
     ],
    [Input('my-slider', 'value'),
     Input('upload-data', 'contents'),
     Input('cluster-slider', 'value')],
)
def hourUpdate(value, content, nCluster):
    if content:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        dataSet = getData(value, nCluster, decoded)
    else:
        dataSet = getData(value, nCluster)
    colorsList = Colors(nCluster).getColorList()
    powerGrid = PowerGrid(dataSet, nCluster, colorsList)
    nodes = [
        {
            'data': {'id': short, 'label': label},
            'grabbable': False,
            'classes': color
        }

        for short, label, color in (
            powerGrid.prepNodes()
        )
    ]

    edges = [
        {'data': {'id': source + target, 'source': source, 'target': target, 'label': label, 'color': color}}

        for target, source, label, color in (
            powerGrid.prepBranches()
        )
    ]
    genColumns = [{'id': 'Location of Generator', 'name': 'Location of Generator'}]
    genRows = {'Location of Generator': 'Price of 1 MW'}
    for col, value in powerGrid.costPlotGenerators():
        genColumns.append({'id': col, 'name': col})
        genRows[col] = value

    columns = [{'id': 'Node number', 'name': 'Node number'}]
    rows = {'Node number': 'Node power balance [MW]'}
    for col, value in powerGrid.prepNodeDataFrame():
        columns.append({'id': col, 'name': col})
        rows[col] = value

    clusterColumns = [{'id': 'Cluster number', 'name': 'Cluster number'}, {'id': 'Max', 'name': 'Max'},
                      {'id': 'Min', 'name': 'Min'}]
    clusterRows = []
    dataCluster = powerGrid.clustersDataFrame()
    i = 1
    style_data_conditional = []
    stylesheet=[]
    for row in dataCluster.iterrows():
        clusterDict = {'Cluster number': i, 'Max': "{:.2f}".format(row[1][1]),
                       'Min': "{:.2f}".format(row[1][0])}
        i += 1
        clusterRows.append(clusterDict)
        style_data_conditional.append({'if': {'row_index': row[0]}, 'backgroundColor': colorsList[int(row[0])]})

    return nodes + edges, genColumns, [genRows], columns, [rows], clusterColumns, clusterRows, style_data_conditional


@app.callback(
    Output('cytoscape-callbacks-1', 'stylesheet'),
    Input('cytoscape-callbacks-1', 'tapNodeData'),
    Input('cluster-slider', 'value'),
)
def displayTapNodeData(data, value):
    if value != 1:
        data = None
    if data:
        val = data['id']
        new_style = [{
            'selector': f'[source = "{val}"]',
            'style': {
                'line-color': 'green',
                'arrow-scale': 3,
                'source-arrow-color': 'green'
            }
        },
            {
                'selector': f'[target = "{val}"]',
                'style': {
                    'line-color': 'red',
                    'arrow-scale': 3,
                    'source-arrow-color': 'red'
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


@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('cytoscape-callbacks-1', 'mouseoverNodeData'))
def displayMouseoverNodeData(data):
    if data:
        return "You recently hovered over the city: " + data['label']
