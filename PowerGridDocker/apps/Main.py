from models.PowerGrid import PowerGrid
from models.Colors import Colors
from dash import html, dcc, Input, Output, Dash, dash_table
from apps.DataParse import *
from apps.Templates import *

import dash_cytoscape as cyto
import base64

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
                {'data': {'id': 'three', 'label': 'Picked Node'}, 'classes': 'blue'},
                {'data': {'source': 'one', 'target': 'two', 'label': 'Power flow'}}
            ],
            stylesheet=default_stylesheet,
            style={'width': '50%', 'height': '100px'},
            layout={
                'name': 'grid'
            },
            zoom=100,
            userZoomingEnabled=True,
            userPanningEnabled=True,
            className='six columns'
        ),

        dash_table.DataTable(
            id='genCost',
            style_cell={'textAlign': 'center'},
            style_table={'width': '50%'}
        )

    ], className='row'),

    html.P("Nodes balance: ", style={'textAlign': "center"}),

    html.Div([
        dash_table.DataTable(
            id='nodeTable',
            style_cell={'textAlign': 'center'},
        ),
    ], className='row'),
    dcc.Store(id='dataSet'),
    dcc.Store(id='colorList'),
], className='row',

)


@app.callback(
    [Output('cytoscape-callbacks-1', 'elements'),
     Output('genCost', 'columns'),
     Output('genCost', 'data'),
     Output('nodeTable', 'columns'),
     Output('nodeTable', 'data'),
     Output('clusterData', 'data'),
     Output('clusterData', 'style_data_conditional'),
     Output('nodeData', 'data'),
     ],
    [Input('my-slider', 'value'),
     Input('upload-data', 'contents'),
     Input('cluster-slider', 'value'),
     Input('cytoscape-callbacks-1', 'mouseoverNodeData')],
)
def hourUpdate(value, content, nCluster, data):
    # get byte string from uploaded data
    if content:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        dataSet = getData(value, nCluster, decoded)
    # get data from defoult datafile
    else:
        dataSet = getData(value, nCluster)
    # Color List for n of clusters
    colorsList = Colors(nCluster).getColorList()
    # Object of Power Grid Class
    powerGrid = PowerGrid(dataSet, colorsList, nCluster)
    # Cytoscape Nodes
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
    # Cytoscape Edges
    edges = [
        {'data': {'id': source + target, 'source': source, 'target': target, 'label': label, 'color': color}}

        for source, target, label, color in (
            powerGrid.prepBranches()
        )
    ]
    # Generators info
    genColumns = [{'id': 'Location of Generator', 'name': 'Location of Generator'}]
    genRows = {'Location of Generator': 'Price of 1 MW'}
    for col, value in powerGrid.costPlotGenerators():
        genColumns.append({'id': col, 'name': col})
        genRows[col] = value
    # Node balance info
    nodeColumns = [{'id': 'Node number', 'name': 'Node number'}]
    nodeRows = {'Node number': 'Node power balance [MW]'}
    for col, value in powerGrid.prepNodeDataFrame():
        nodeColumns.append({'id': col, 'name': col})
        nodeRows[col] = value

    # Cluster Info
    clusterRows = []
    style_data_conditional = []
    dataCluster = powerGrid.clustersDataFrame()
    for row in dataCluster.iterrows():
        clusterDict = {'Cluster number': row[0], 'Max': "{:.2f}".format(row[1][1]),
                       'Min': "{:.2f}".format(row[1][0])}
        clusterRows.append(clusterDict)
        style_data_conditional.append({'if': {'row_index': row[0]}, 'backgroundColor': colorsList[int(row[0])]})
    # Node info
    if data:
        nodeDict = powerGrid.getNodeInfo(data['label'])
        dataRows = [{'Node Id': nodeDict['Node Id'], 'Node Type': nodeDict["Node Type"],
                     'Node Demand': nodeDict['Node Demand']}]
    else:
        dataRows = []

    return nodes + edges, genColumns, [genRows], nodeColumns, [
        nodeRows], clusterRows, style_data_conditional, dataRows


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
