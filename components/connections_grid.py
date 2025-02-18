import dash_ag_grid as dag

def build_connections_grid() -> dag.AgGrid:
    """ Monta um grid para as conexões com as bases de dados """

    column_defs = [
        {
            'headerName': 'Status',
            'field': 'availability',
            'tooltipField': 'availability',
            'tooltipComponentParams': {'color': '#303030'},
            'tooltipComponent': 'ConnectionErrorTooltip',
            'width': 80,
            'resizable': False,
            'cellStyle': {
                'styleConditions': [
                    {'condition': "params.value >= 1.0", 'style': {'backgroundColor': '#309B81', 'color': '#309B81'}},
                    {'condition': "params.value < 1.0", 'style': {'backgroundColor': '#F51818', 'color': '#F51818'}},
                ]
            }
        },
        {
            'headerName': 'Sistema',
            'field': 'name',
            'width': 300,
            'resizable': False,
        },
        {
            'headerName': '',
            'field': 'failed_connections',
            'hide': True,
            'resizable': False,
        },
    ]

    default_column_def = {
        'filter': False,
        'resizable': True,
        'sortable': False,
        'editable': False,
        'floatingFilter': False,
    }

    connections_grid = dag.AgGrid(
        id='connections-grid',
        className='ag-theme-alpine-dark',
        columnDefs=column_defs,
        defaultColDef=default_column_def,
        style={'height': '300px', 'width': '100%'},
        dashGridOptions={'tooltipShowDelay': 100}
    )

    return connections_grid