from models.PowerGrid import PowerGrid
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output, Dash, State, dash_table
from apps.dataParse import *
from apps.templates import *
import base64
import datetime
import io
import plotly.express as px

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
            'line-color': 'data(color)',
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

app.layout = html.Div([
    html.Div([html.H1("Power Grid Analysis")], style={'textAlign': "center"}),
    html.Div([
        dcc.Slider(1, 24, 1,
                   value=12,
                   id='my-slider',
                   className='six columns'
                   ),
        dcc.Slider(1, 6, 1,
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

    cyto.Cytoscape(
        id='cytoscape-callbacks-1',
        elements=[],
        style={'width': '100%', 'height': '570px'},
        layout={
            'name': 'breadthfirst',
        },

        zoom=100,
        userZoomingEnabled=False,
        userPanningEnabled=False,
        stylesheet=default_stylesheet
    ),

    html.Div([html.H1(children=''),
              dcc.Graph(id='genCost',
                        style={
                            'width': '50%',
                            'height': '400px'
                        },
                        className='six columns'
                        ),
              html.Pre(id='cytoscape-tapNodeData-json',
                       style=styles['pre'],
                       className='six columns'),
              ], className='row'),
    html.P(id='cytoscape-tapNodeData-output'),

], className='row')


@app.callback(
    [Output('cytoscape-callbacks-1', 'elements'),
     Output('genCost', 'figure')],
    [Input('my-slider', 'value'),
     Input('upload-data', 'contents'),
     Input('cluster-slider', 'value')],
)
def hourUpdate(value, content, nCluster):
    if content:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        # print(read_hdf_from_buffer(decoded))

    dataSet = getData(value, nCluster)
    powerGrid = PowerGrid(dataSet, nCluster)
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


    figure = px.bar(powerGrid.costPlotGenerators(),
                    title=f'Koszt produkcji jednostki energi o godzinie: {value}:00',
                    x='Lokalizacja generatora',
                    y='Generowana Moc',
                    barmode='stack'
                    )

    return nodes + edges, figure


@app.callback(
    [Output('cytoscape-callbacks-1', 'stylesheet'),
     Output('cluster-slider', 'value')],
    Input('cytoscape-callbacks-1', 'tapNodeData'),
)
def displayTapNodeData2(data):
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
    else:
        return default_stylesheet
    return default_stylesheet + new_style, 1


@app.callback(
    Output('cytoscape-tapNodeData-json', 'children'),
    Input('cytoscape-callbacks-1', 'tapNodeData')
)
def displayTapNodeData(data):
    return format(data)
