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
    name = 'SDG Info',
    path = '/'
)

sdg_info_df = pd.read_csv ('./data/sdg_info_fixedv1.csv')

sdg_stats = dbc.Container (children = [
    dbc.Row (children = [
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
], class_name = 'p-5 d-flex justify-content-around align-items-center',
style = {
    'background-image' : 'url ("/assets/bg.jpg")',
    'background-size' : 'cover',
    'height' : '100%'
})

sdg_info = dbc.Container (children = [
    dbc.Row (children = [
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
                    ),
            html.Img (src = dash.get_asset_url ('bg.jpg'),
                    style = {
                        'max-width' : '0%'
                        }
                    )
        ], className = 'col-4'),
    ], className = 'p-5')
], className = 'p-5 d-flex justify-content-center align-items-center',
style = {
    'background-image' : 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/bg1.jpg")',
    'background-size' : 'cover',
    'height' : 'calc(100vh - 54px)',
    'min-width' : '100vw'
})

goals_list = [
    {
        "id": "sgd1",
        "image": "SDG_Icons_Inverted_Transparent_WEB-01.png",
        "label": "#1 No Poverty",
        "description": "End poverty in all its forms everywhere.",
        "targets": [
            {
                "target": "By 2030, achieve the complete elimination of extreme poverty for all individuals globally, such as no individuals will be living on less than $1.25 per day.",
                "indicators": []
            }
        ],
    },
    {
        "id": "sgd2",
        "image": "SDG_Icons_Inverted_Transparent_WEB-02.png",
        "label": "#2 Zero Hunger",
        "description": "End hunger, achieve food security and improved nutrition and promote sustainable agriculture.",
        "content": "chuchu",
    },
    {
        "id": "sgd3",
        "image": "SDG_Icons_Inverted_Transparent_WEB-03.png",
        "label": "#3 Good Health and Well-Being",
        "description": "Ensure healthy lives and promote well-being for all at all ages.",
        "content": "chuchu",
    },
    {
        "id": "sgd4",
        "image": "SDG_Icons_Inverted_Transparent_WEB-04.png",
        "label": "#4 Quality Education",
        "description": "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all.",
        "content": [

        ],
    }
]

def create_accordion_label(label, image, description):
    return dmc.AccordionControl(
        dmc.Group(
            [
                dmc.Avatar(src=dash.get_asset_url (image), size="lg"),
                html.Div(
                    [
                        dmc.Text(label, className="goal-label"),
                        dmc.Text(description, className="goal-desc", size="sm", weight=400, color="dimmed"),
                    ]
                ),
            ]
        )
    )

def create_accordion_content(content):
    return dmc.AccordionPanel(dmc.Text(content, size="sm"))

goals_info = dbc.Container (children = [
    dbc.Row (children = [
        html.H1 ('The 17 Goals', className = 'sub-title pb-5'),
        dmc.Accordion(
            chevronPosition="right",
            variant="separated",
            children=[
                dmc.AccordionItem(
                    [
                        create_accordion_label(
                            goal["label"], goal["image"], goal["description"]
                        ),
                        create_accordion_content("chuchuchu"),
                    ],
                    value=goal["id"],
                )
                for goal in goals_list
            ],
        )
    ])
], className = 'p-5')

layout = dbc.Container(id = 'main-container',
                           children = [
                                   sdg_info,
                                   #sdg_stats,
                                   goals_info,
                               ],
                            style = {
                                'margin-right': '0 !important',
                                'max-width': '100%',
                                'padding' : '0px',
                            }, 
)