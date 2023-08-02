from dash import html, register_page
import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

register_page(__name__, name="SDG Info", path="/")

from data import *
from constants import *

sdg_stats = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Row(children=[html.H1("17", className="count-sdg")]),
                        dbc.Row(
                            children=[html.H3("Goals", className="count-text-sdg")]
                        ),
                    ],
                    class_name="col-4",
                ),
                dbc.Col(
                    children=[
                        dbc.Row(children=[html.H1("169", className="count-sdg")]),
                        dbc.Row(
                            children=[html.H3("Targets", className="count-text-sdg")]
                        ),
                    ],
                    class_name="col-4",
                ),
                dbc.Col(
                    children=[
                        dbc.Row(children=[html.H1("7", className="count-sdg")]),
                        dbc.Row(
                            children=[
                                html.H3(
                                    "Years Left until 2030", className="count-text-sdg"
                                )
                            ]
                        ),
                    ],
                    class_name="col-4",
                ),
            ]
        )
    ],
    class_name="p-5 d-flex justify-content-around align-items-center",
    style={
        "background-image": 'url ("/assets/bg.jpg")',
        "background-size": "cover",
        "height": "100%",
    },
)

sdg_info = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H1(
                            "The United Nations' Sustainable Development Goals",
                            id="title",
                        ),
                        html.P(
                            "In 2015, the Sustainable Development Goals (SDGs) were established by the United Nations General Assembly. These 17 interconnected global objectives were set with the aim of being accomplished by 2030, with the vision of creating a more sustainable and improved future for everyone.",
                            className="description",
                        ),
                        dmc.Anchor(dmc.Button(
                            "Explore Dashboard",
                            leftIcon=DashIconify(icon="ph:magnifying-glass-bold"),
                            color="lime",
                            size="lg",
                            
                        ), href='/sdg-focused-tab')
                    ],
                    className="col-7",
                ),
                dbc.Col(children=[], className="col-1"),
                dbc.Col(
                    children=[
                        html.Img(
                            src=dash.get_asset_url("sdg_logo.png"),
                            style={"max-width": "100%"},
                        ),
                        html.Img(
                            src=dash.get_asset_url("bg.jpg"), style={"max-width": "0%"}
                        ),
                    ],
                    className="col-4",
                ),
            ],
            className="p-5",
        )
    ],
    className="p-5 d-flex justify-content-center align-items-center",
    style={
        "background-image": 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/background/bg1.jpg")',
        "background-size": "cover",
        "height": "calc(100vh - 54px)",
        "min-width": "100vw",
    },
)


def create_accordion_label(index, label, description):
    return dmc.AccordionControl(
        dmc.Group(
            [
                dmc.Avatar(
                    src=dash.get_asset_url("goal-images/" + str(index) + ".png"),
                    size="lg",
                ),
                html.Div(
                    [
                        dmc.Text(
                            "#" + str(index) + " " + label, className="goal-label"
                        ),
                        dmc.Text(
                            description,
                            className="goal-desc",
                            size="sm",
                            weight=400,
                            color="dimmed",
                        ),
                    ]
                ),
            ]
        )
    )


def create_accordion_content(content):
    return dmc.AccordionPanel(dmc.Text(content, size="sm", className="text-body"))


goals_info = dbc.Container(
    children=[
        dbc.Row(
            children=[
                html.H1("The 17 Goals", className="sub-title pb-5"),
                dmc.Accordion(
                    chevronPosition="right",
                    variant="separated",
                    children=[
                        dmc.AccordionItem(
                            [
                                create_accordion_label(
                                    i + 1, goals_name[i], goals_desc[i]
                                ),
                                create_accordion_content(goals_information[i][0]),
                            ],
                            value=goals_name[i],
                        )
                        for i in range(len(goals_name))
                    ],
                ),
            ]
        )
    ],
    className="p-5",
)

layout = dbc.Container(
    id="main-container",
    children=[
        sdg_info,
        goals_info,
    ],
    style={
        "margin-right": "0 !important",
        "max-width": "100%",
        "padding": "0px",
    },
)
