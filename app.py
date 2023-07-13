import pandas as pd
from dash import html, dcc, Dash, Input, Output, State, callback
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

EXTERNAL_BOOTSTRAP = 'https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/lumen/bootstrap.min.css'

sdg_info_df = pd.read_csv ('/data/sdg_info.csv')

fig = go.Figure(go.Icicle(
    ids = sdg_info_df.ids,
    labels = sdg_info_df.labels,
    parents = sdg_info_df.parents,
    root_color="lightgrey"
))
fig.update_layout(
    uniformtext=dict(minsize=10, mode='hide'),
    margin = dict(t=50, l=25, r=25, b=25)
)

app = Dash (
    __name__, 
    external_stylesheets = [EXTERNAL_BOOTSTRAP]
)

tabs_options = dcc.Tabs (id = "tabs-option", 
                         value = 'sdg-info-tab', 
                         children = [
                             dcc.Tab (label = 'SDG Information', value = 'sdg-info-tab'),
                             dcc.Tab (label = 'SDG-Focused Tab', value ='sdg-focused-tab'),
                             dcc.Tab (label = 'Region-Focused Tab', value ='region-focused-tab'),
                        ])

options_in_navbar = dbc.Row (children = [
                dbc.Col (children = [
                    dbc.Nav (children = [
                            dbc.NavItem (dbc.NavLink ('SDG Information', active = True, href = '/')),
                            dbc.NavItem (dbc.NavLink ('SDG-Focused Tab', href = '/sdg-focused-tab')), 
                            dbc.NavItem (dbc.NavLink ('Region-Focused Tab', href = '/region-focused-tab')),   
                        ],
                        navbar = True,
                        pills = True,
                        fill = True
                    )
                ])
            ]),

navbar = dbc.Navbar (children = [
        dbc.Container (children = [
            dbc.Row (children = [
                dbc.Col (children = [
                    # Icon source: https://www.flaticon.com/free-icon/growth_2889137
                    dbc.Container (children = [
                        html.Img(src=dash.get_asset_url('growth.png'), height="40px"),
                        dbc.NavbarBrand ("The Progress of the Philippines in the SDG", 
                                            className = "ms-2 h-50",
                                            style = {
                                                'font-weight' : 'bold',
                                                'height' : '100%'
                                            },
                                        ), 
                        ],
                        )
                    ])
                ], 
                align = 'center',
                className="g-0"
            ),
            dbc.NavbarToggler (id = "navbar-toggler", n_clicks = 0),
            dbc.Collapse(
                options_in_navbar,
                id = "navbar-collapse",
                is_open = False,
                navbar = True,
            ),
        ]) 
    ],
    color = 'primary',
    dark = True,
    sticky = 'Top'
)

app.layout = dbc.Container(id = 'main-container',
                           children = [
                               navbar, 
                               dbc.Container (id = 'content-container', children = [
                                   
                               ])
                            ],
                            style = {
                                'margin-right': '0 !important',
                                'max-width': '100%',
                                'padding' : '0px'
                            }, 
)

# For collapsing navbar for small screens
@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server (debug = True)