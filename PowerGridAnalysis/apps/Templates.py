# basic style templates
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
            'target-arrow-shape': 'triangle',
            'target-arrow-color': 'data(color)',
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
        'selector': '.generatorP',
        'style': {
            'shape': 'square',
            'background-color': 'green',
        }
    },
    {
        'selector': '.generatorN',
        'style': {
            'shape': 'square',
            'background-color': 'red',
        }
    },
    {
        'selector': '.generator',
        'style': {
            'shape': 'square',
        }
    },
]

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'width': '9%',
        'height': '100px'
    }
}

