import pandas as pd
from dash import html, dcc, Dash, Input, Output, State, callback, register_page
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

EXTERNAL_BOOTSTRAP = 'https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/lumen/bootstrap.min.css'

sdg_info_df = pd.read_csv ('./data/sdg_info_fixed.csv')

app = Dash (
    __name__, 
    external_stylesheets = [
        EXTERNAL_BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Source+Serif+4:wght@400;500&display=swap'
    ]
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
                        html.Img(src=dash.get_asset_url('growth_white.png'), height="40px"),
                        dbc.NavbarBrand ("The Progress of the Philippines in the SDG", 
                                            className = "ms-2 h-50",
                                            style = {
                                                'font-weight' : 'bold',
                                                'height' : '100%',
                                                'vertical-align' : 'middle'
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
        ],
        style = {
            'padding-left' : '1%',
            'margin-left' : '0%',
            'padding-top' : '5px',
            'padding-bottom' : '5px'
        }) 
    ],
    color = 'primary',
    dark = True,
    sticky = 'top'
)

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

app.layout = dbc.Container(id = 'main-container',
                           children = [
                               navbar, 
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


register_page (
    __name__, 
    path = '/'
)