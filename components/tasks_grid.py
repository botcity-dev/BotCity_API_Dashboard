import dash_ag_grid as dag

def build_tasks_grid() -> dag.AgGrid:
    """ Monta um grid para as tarefas executadas """

    column_defs = [
        {
            'headerName': 'Status',
            'field': 'status',
            'tooltipField': 'status',
            'tooltipComponentParams': {'color': '#303030'},
            'tooltipComponent': 'TaskErrorTooltip',
            'width': 80,
            'resizable': False,
            'cellStyle': {
                'styleConditions': [
                    {'condition': "params.value == 'START'", 'style': {'backgroundColor': '#D2D2D2', 'color': '#303030'}},
                    {'condition': "params.value == 'RUNNING'", 'style': {'backgroundColor': '#189FF5', 'color': '#303030'}},
                    {'condition': "params.value == 'SUCCESS'", 'style': {'backgroundColor': '#309B81', 'color': '#303030'}},
                    {'condition': "params.value == 'PARTIALLY_COMPLETED'", 'style': {'backgroundColor': '#F58918', 'color': '#303030'}},
                    {'condition': "params.value == 'FAILED'", 'style': {'backgroundColor': '#F51818', 'color': '#303030'}},
                ]
            }
        },
        {
            'headerName': '',
            'field': 'error_message',
            'hide': True,
        },
        {
            'headerName': 'ID',
            'field': 'id',
            'width': 100,
        },
        {
            'headerName': 'Bot',
            'field': 'bot',
            'width': 200,
        },
        {
            'headerName': 'Automações',
            'field': 'automations',
            'width': 140,
        },
        {
            'headerName': 'Descrição',
            'field': 'description',
            'width': 200,
        },
        {
            'headerName': 'Início',
            'field': 'start_date',
            'width': 150,
        },
        {
            'headerName': 'Término',
            'field': 'end_date',
            'width': 150,
        },
        {
            'headerName': 'Runner',
            'field': 'runner',
            'width': 130,
        },
        {
            'headerName': 'Criador',
            'field': 'creator',
            'width': 170,
        },
        {
            'headerName': 'Mensagem',
            'field': 'message',
        }
    ]

    default_column_def = {
        'filter': False,
        'resizable': True,
        'sortable': False,
        'editable': False,
        'floatingFilter': False,
    }

    tasks_grid = dag.AgGrid(
        id='tasks-grid',
        className='ag-theme-alpine-dark',
        columnDefs=column_defs,
        defaultColDef=default_column_def,
        dashGridOptions={'tooltipShowDelay': 100}
    )

    return tasks_grid