import pandas as pd
from dash import html, dcc, Dash, Input, Output, State, callback, register_page
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

register_page (
    __name__, 
    Name = 'SDG Info',
    path = '/'
)

sdg_info_df = pd.read_csv ('./data/sdg_info_fixed.csv')

sdg_stats = dbc.Row (children = [
    dbc.Col (children = [
        dbc.Row (children = [
            html.H1 ('17', className = 'count-sdg')
        ]),
        dbc.Row (children = [
             html.H3 ('Goals', className = 'count-text-sdg')
        ]),
    ], class_name = 'col-4'),
    dbc.Col (children = [
        dbc.Row (children = [
            html.H1 ('169', className = 'count-sdg')
        ]),
        dbc.Row (children = [
            html.H3 ('Targets', className = 'count-text-sdg')
        ]),
    ], class_name = 'col-4'),
    dbc.Col (children = [
        dbc.Row (children = [
            html.H1 ('7', className = 'count-sdg')
        ]),
        dbc.Row (children = [
            html.H3 ('Years Left until 2030', className = 'count-text-sdg')
        ]),
    ], class_name = 'col-4')
])

sdg_info = dbc.Row (children = [
    dbc.Col (children = [
        html.H1 ('The United Nations\' Sustainable Development Goals', id = 'title'),
        html.P ('In 2015, the Sustainable Development Goals (SDGs) were established by the United Nations General Assembly. These 17 interconnected global objectives were set with the aim of being accomplished by 2030, with the vision of creating a more sustainable and improved future for everyone.',
                className = 'description')
    ], className = 'col-7'),
    dbc.Col (children = [], className = 'col-1'),
    dbc.Col (children = [
        html.Img (src = dash.get_asset_url ('sdg_logo.png'),
                  style = {
                      'max-width' : '100%'
                      }
                )
    ], className = 'col-4'),
])

card = dbc.Card(
    dbc.CardBody(
        [
            html.H2("#1 No Poverty", className="card-title"),
            html.P('The objective of eradicating extreme poverty for every individual worldwide by 2030 is a crucial aspect of the 2030 Agenda for Sustainable Development.',
                   className="card-text"
            ),
        ]
    ),
    style={"width": "18rem"},
    className = 'card',
)

goals_info = dbc.Row (children = [
    html.H1 ('The 17 Goals', className = 'sub-title'),
    dbc.Row (children = [
        dbc.Col (children = [
            dbc.Container (children = [
                card
            ])
        ], className = 'col-2'),
        dbc.Col (children = [

        ], className = 'col-2'),
        dbc.Col (children = [

        ], className = 'col-2'),
        dbc.Col (children = [

        ], className = 'col-2'),
        dbc.Col (children = [

        ], className = 'col-2'),
        dbc.Col (children = [

        ], className = 'col-2')
    ])
])

layout = dbc.Container(id = 'main-container',
                           children = [
                               dbc.Container (id = 'chart-container', children = [
                                   sdg_info,
                                   html.Hr (),
                                   sdg_stats,
                                   html.Hr (),
                                   dbc.Row (children = [
                                       goals_info
                                   ]),
                               ])
                            ],
                            style = {
                                'margin-right': '0 !important',
                                'max-width': '100%',
                                'padding' : '0px',
                                'width' : '100vw',
                                'height' : '100vh'
                            }, 
)