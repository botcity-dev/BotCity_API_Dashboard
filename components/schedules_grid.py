import dash_ag_grid as dag

def build_schedules_grid() -> dag.AgGrid:
    """ Monta um grid para os schedulings """

    column_defs = [
        {
            'headerName': 'Bot',
            'field': 'bot',
            'width': 200,
            'resizable': False,
        },

        {
            'headerName': 'Início',
            'field': 'start_date',
            'width': 200,
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

    schedules_grid = dag.AgGrid(
        id='schedules-grid',
        className='ag-theme-alpine-dark',
        columnDefs=column_defs,
        defaultColDef=default_column_def,
        style={'height': '300px', 'width': '100%'}
    )

    return schedules_grid