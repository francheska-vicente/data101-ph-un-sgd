import pandas as pd
from dash import html, dcc, Dash, Input, Output, State, callback, register_page
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

register_page (
    __name__, 
    name = 'SDG-focused Tab',
    path = '/sdg-focused-tab'
)

sdg_info = pd.read_csv ('https://raw.githubusercontent.com/francheska-vicente/datapre-project/main_v2/data_output/combined_data.csv')
sdg_regions_available = sdg_info ['Geolocation'].unique () [1 : ]
sdg_indicators_available = sdg_info.columns [2 : ]

control_card = dbc.Row (children = [
        dbc.Card (children = [
            dbc.CardHeader ('Chart Controls for the Regions and Indicators'),
            dbc.CardBody (children = [
                dbc.Row (children = [
                    dbc.Col (children = [
                        dbc.Row (children = [
                            html.H6 ('What are the regions you want to visualize? (Maximum of 2)'),
                            dcc.Dropdown(
                                id = 'region-dropdown',
                                options = [{'label': i, 'value': i} for i in sdg_regions_available],
                                multi = True,
                            ),
                            html.Div (id = 'region-warning', style = {'padding-top' : '10px'})
                        ])
                    ], className = 'col-6'),
                    dbc.Col (children = [
                        dbc.Row (children = [
                            html.H6 ('What are the indicators you want to visualize? (Maximum of 2)'),
                            dcc.Dropdown(
                                id = 'indicator-dropdown',
                                options = [{'label': i, 'value': i} for i in sdg_indicators_available],
                                multi = True,
                            ),
                            html.Div (id = 'indicator-warning', style = {'padding-top' : '10px'})
                        ])
                    ], className = 'col-6')
                ])
            ])
        ])
    ],
    style = {
        'width' : '100%',
        'margin' : 'auto'
    }
)

layout = dbc.Container (children = [
        html.H2("SGD-Focused Tab"),
        html.P("Choose regions and indicators to display ganito ganito.", className = "pb-3 text-center fw-light fst-italic"),
        control_card
    ],
    className = 'p-5',
    style = {
        'background-image' : 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/bg2.jpg")',
        'background-size' : 'cover',
        'height' : 'calc(100vh - 54px)',
        'min-width' : '100vw'
    })

@callback (
    Output ('region-dropdown', 'options'),
    Output ('region-warning', 'children'),
    Input ('region-dropdown', 'value'),
    prevent_initial_callbacks = True
)
def region_dropdown_control (region_selected):
    options = sdg_regions_available
    input_warning = None

    if region_selected is None:
        return options, input_warning

    if len (region_selected) >= 2:
        input_warning = html.P (id = 'region-warning-message', 
                                children = 'Maximum number of regions reached!',
                                className = "fw-light fst-italic",
                                style = {
                                    'text-align' : 'right',
                                    'margin-bottom' : '0px',
                                    'font-size' : '14px'
                                })
        options = [
            {
                'label' : option,
                'value' : option,
                'disabled' : True
            } for option in options
        ]

    return options, input_warning

@callback (
    Output ('indicator-dropdown', 'options'),
    Output ('indicator-warning', 'children'),
    Input ('indicator-dropdown', 'value'),
    prevent_initial_callbacks = True
)
def indicator_dropdown_control (indicator_selected):
    options = sdg_indicators_available
    input_warning = None

    if indicator_selected is None:
        return options, input_warning

    if len (indicator_selected) >= 2:
        input_warning = html.P (id = 'indicator-warning-message', 
                                children = 'Maximum number of indicators reached!',
                                className = "fw-light fst-italic",
                                style = {
                                    'text-align' : 'right',
                                    'margin-bottom' : '0px',
                                    'font-size' : '14px'
                                })
        options = [
            {
                'label' : option,
                'value' : option,
                'disabled' : True
            } for option in options
        ]

    return options, input_warning