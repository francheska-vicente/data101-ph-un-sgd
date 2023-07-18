import pandas as pd
from dash import html, dcc, Dash, Input, Output, State, callback, register_page
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

register_page (
    __name__, 
    name = 'Region-focused Tab',
    path = '/region-focused-tab'
)

sdg_info = pd.read_csv ('https://raw.githubusercontent.com/francheska-vicente/datapre-project/main_v2/data_output/combined_data.csv')
sdg_regions_available = sdg_info ['Geolocation'].unique () [1 : ]
sdg_indicators_available = sdg_info.columns [2 : ]

control_card = dbc.Row (children = [
        dbc.Card (children = [
            dbc.CardHeader ('Chart Controls for the Target'),
            dbc.CardBody (children = [
                dbc.Row (children = [
                    dbc.Col (children = [
                        dbc.Row (children = [
                            html.H6 ('What is the target you want to visualize? (Maximum of 1)'),
                            dcc.Dropdown(
                                id = 'target-tab3-dropdown',
                                options = [{'label': i, 'value': i} for i in sdg_regions_available],
                                multi = True,
                            ),
                            html.Div (id = 'region-tab3-warning', style = {'padding-top' : '10px'})
                        ])
                    ], className = 'col-12')
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
        html.H2("Region-Focused Tab"),
        html.P("Choose a target to display ganito ganito.", className = "pb-3 text-center fw-light fst-italic"),
        control_card
    ],
    className = 'p-5',
    style = {
        'background-image' : 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/bg3.jpg")',
        'background-size' : 'cover',
        'height' : 'calc(100vh - 54px)',
        'min-width' : '100vw'
})

@callback (
    Output ('region-tab3-dropdown', 'options'),
    Output ('region-tab3-warning', 'children'),
    Input ('region-tab3-dropdown', 'value'),
    prevent_initial_callbacks = True
)
def region_dropdown_control (region_selected):
    options = sdg_regions_available
    input_warning = None

    if region_selected is None:
        return options, input_warning

    if len (region_selected) >= 1:
        input_warning = html.P (id = 'region-tab3-warning-message', 
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
    Output ('indicator-tab3-dropdown', 'options'),
    Output ('indicator-tab3-warning', 'children'),
    Input ('indicator-tab3-dropdown', 'value'),
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