import dash_ag_grid as dag

def build_runners_grid() -> dag.AgGrid:
    """ Monta um grid para os runners """

    column_defs = [
        {
            'headerName': 'Status',
            'field': 'online',
            'width': 80,
            'resizable': False,
            'cellStyle': {
                'styleConditions': [
                    {'condition': "params.value == true", 'style': {'backgroundColor': '#309B81', 'color': '#309B81'}},
                    {'condition': "params.value == false", 'style': {'backgroundColor': '#F51818', 'color': '#F51818'}},
                ]
            }
        },
        {
            'headerName': 'Runner',
            'field': 'name',
            'width': 300,
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

    runners_grid = dag.AgGrid(
        id='runners-grid',
        className='ag-theme-alpine-dark',
        columnDefs=column_defs,
        defaultColDef=default_column_def,
        style={'height': '300px', 'width': '100%'}
    )

    return runners_grid