from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq

from data_source.botcity import BotcityApiPlugin
from data_access.botcity import BotcityDataAccess

from components.tasks_grid import build_tasks_grid
from components.schedules_grid import build_schedules_grid
from components.runners_grid import build_runners_grid
from components.connections_grid import build_connections_grid

from typing import Hashable, Dict, List, Any
from app import configurations as config

# iniciando app dash
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], title='RPA Operations Center')


# iniciando acesso ao botcity
dso_botcity = BotcityApiPlugin(login=config.MAESTRO_LOGIN, key=config.MAESTRO_KEY)
dao_botcity = BotcityDataAccess(dso_botcity)

# montando grids
tasks_grid = build_tasks_grid()
schedules_grid = build_schedules_grid()
runners_grid = build_runners_grid()
connections_grid = build_connections_grid()

# desenhando o layout do dashboard
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div('RPA Operations Center', className='h2 p-2 text-white'), className='py-2'),
                dbc.Col(html.Div(
                    [daq.BooleanSwitch(on=True, label='Refresh Automático', id='refresh-switch', color="#9B51E0")]),
                        className='py-2')
            ]
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        html.H5('Últimas 100 tarefas executadas', className='h5 p-2 text-white'),
                        dbc.Col(tasks_grid, className='py-1')
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H5('Tarefas agendadas', className='h5 p-2 text-white'),
                            schedules_grid
                        ]
                    ), className='py-1'
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H5('Disponibilidade dos runners', className='h5 p-2 text-white'),
                            runners_grid
                        ]
                    ), className='py-1'
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H5('Disponibilidade dos sistemas', className='h5 p-2 text-white'),
                            connections_grid
                        ]
                    ), className='py-1'
                ),
            ]
        ),
        dcc.Interval(id='refresh-interval', interval=60 * 1000, n_intervals=0),
    ]
)


######################################################################
# As Callback são funções executadas quando um evento refresh ocorre.#
######################################################################

@app.callback(Output('refresh-interval', 'disabled'),
              Input('refresh-switch', 'on'))
def switch_interval(on: bool) -> bool:
    return not on


@app.callback(Output('tasks-grid', 'rowData'),
              Input('refresh-interval', 'n_intervals'))
def refresh_tasks_grid(_) -> List[Dict[Hashable, Any]]:
    return dao_botcity.get_tasks_data()


@app.callback(Output('schedules-grid', 'rowData'),
              Input('refresh-interval', 'n_intervals'))
def refresh_schedules_grid(_) -> List[Dict[Hashable, Any]]:
    return dao_botcity.get_schedules_data()


@app.callback(Output('runners-grid', 'rowData'),
              Input('refresh-interval', 'n_intervals'))
def refresh_runners_grid(_) -> List[Dict[Hashable, Any]]:
    return dao_botcity.get_runners_data()


if __name__ == '__main__':
    app.run(debug=True)
