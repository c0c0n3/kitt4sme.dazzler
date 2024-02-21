from typing import Any

from dash import Dash
import pandas as pd
import plotly.express as px

from dazzler.dash.entitymon import EntityMonitorDashboard
from dazzler.ngsy import OPTIPLANT_ESTIMATE_TYPE


def dash_builder(app: Dash) -> Dash:
    return OptiplantDashboard(app).build_dash_app()


class OptiplantDashboard(EntityMonitorDashboard):

    def __init__(self, app: Dash):
        super().__init__(
            app=app,
            title='Machine Status',
            entity_type=OPTIPLANT_ESTIMATE_TYPE
        )

    def empty_data_set(self) -> dict:
        return {
            'index': [0],
            'status': [0]
        }

    def explanation(self) -> str:
        return \
        '''
        This graph shows how **status** estimates for the selected machine
        vary over time. For each time point the graph plots the machine
        status estimate at that time that the AI computed.

        The graph updates automatically every few seconds so you can monitor
        your machine in near real time. To start a monitoring session, load
        the IDs of the machines connected to the system, then select the ID
        of the machine you'd like to monitor. Optionally choose how many data
        points back in time to display from the latest received data point.
        '''

    def make_figure(self, df: pd.DataFrame) -> Any:
        color_map = {'status': 'coral'}
        return px.line(df, x=df.index, y=[df.status],
                        color_discrete_map=color_map)
