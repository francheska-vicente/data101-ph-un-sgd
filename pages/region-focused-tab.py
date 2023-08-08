import numpy as np
import pandas as pd
from dash import html, dcc, Input, Output, callback, register_page
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from data import *
from constants import *

register_page(__name__, name="Region-focused Tab", path="/region-focused-tab")

px.set_mapbox_access_token(open(".mapbox_token").read())


def generate_heatmap(region_selected):
    targets_df = pd.DataFrame([targets_value], columns=sdg_columns)

    region_df = sdg_data[sdg_data["Geolocation"] == region_selected]
    region_df = pd.concat([targets_df, region_df]).reset_index(drop=True)
    region_df = region_df.T
    region_df.columns = region_df.iloc[0]
    region_df = region_df.drop(["Geolocation", "Year"], axis=0)
    region_df = region_df.groupby("Target Number", group_keys=True).mean().T
    region_df = region_df.drop([""], axis=1)

    temp_sdg_info = sdg_info[["Target Number", "Shortened Target"]].drop_duplicates()

    new_col_names = []

    for target in region_df.columns:
        info = list(
            temp_sdg_info[temp_sdg_info["Target Number"] == target][
                "Shortened Target"
            ].values
        )[0]
        new_col_names.append(info)

    region_df.columns = new_col_names
    region_df_corr = region_df.corr()

    mask = np.zeros_like(region_df_corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    df_corr_viz = (
        region_df_corr.mask(mask).dropna(how="all").dropna(axis="columns", how="all")
    )

    fig = px.imshow(df_corr_viz, text_auto=True)
    fig.update_layout(
        yaxis=dict(tickfont=dict(size=7)), xaxis=dict(tickfont=dict(size=7))
    )
    return fig


def generate_linechart(region_selected, target_selected):
    target_selected = (
        sdg_info[sdg_info["Shortened Target"] == target_selected]
        .drop_duplicates(["Shortened Target"])["Target Number"]
        .values[0]
    )

    targets_df = pd.DataFrame([targets_value], columns=sdg_columns)

    region_df = sdg_data[sdg_data["Geolocation"] == region_selected]
    region_df = pd.concat([targets_df, region_df]).reset_index(drop=True)
    region_df = region_df.drop("Geolocation", axis=1)
    region_df.loc[0, "Year"] = "Target Number"
    region_df = region_df.T
    region_df.columns = region_df.iloc[0]
    region_df = region_df.drop("Year", axis=0)
    region_df = region_df[region_df["Target Number"] == target_selected].T
    region_df = region_df.drop("Target Number", axis=0)
    region_df = region_df.dropna()

    if len(region_df) == 0:
        return no_data_chart

    fig = px.line(region_df, markers=True)

    fig.update_layout(
        # axis and legend font
        font_family="Cambria",
        font_color="#000000",
        # x-axis
        xaxis_title="Year",
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="#000000",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Cambria",
                size=16,
                color="#000000",
            ),
        ),
        # y-axis
        yaxis_title="Indicator Value",
        yaxis=dict(
            showgrid=False,
            showline=True,
            showticklabels=True,
            linecolor="#000000",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Cambria",
                size=16,
                color="#000000",
            ),
        ),
        hovermode="x unified",
        autosize=True,
        showlegend=True,
        plot_bgcolor="light gray",  # BG COLOR INSIDE CHART
    )

    fig.update_xaxes(type="category")

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def generate_choropleth():
    sdg = sdg_data["Geolocation"].unique()[1:]
    sdg = pd.DataFrame({"Geolocation": sdg})
    geo = pd.DataFrame(region_area["Area"])

    updated_region_area = pd.concat([sdg, geo["Area"]], axis=1)
    for i in range(len(updated_region_area)):
        area = float(updated_region_area.loc[i, "Area"].replace(",", "").split(" ")[0])
        updated_region_area["Area"] = updated_region_area["Area"].replace(
            [updated_region_area.loc[i, "Area"]], area
        )

    fig = px.choropleth_mapbox(
        updated_region_area,
        geojson=region.geometry,
        locations="Geolocation",
        color="Area",
        center={"lat": 12.099, "lon": 122.733},
        zoom=4,
    )

    return fig


control_card = dbc.Card(
    children=[
        dbc.CardHeader("Chart Controls for the Target", className="w-100"),
        dbc.CardBody(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                dbc.Row(
                                    children=[
                                        html.H6(
                                            "What is the target you want to visualize?"
                                        ),
                                        dmc.MultiSelect(
                                            id="target-dropdown",
                                            data=[
                                                {"label": i, "value": i}
                                                for i in target_info
                                            ],
                                            description="You can select one or more targets.",
                                            searchable=True,
                                            clearable=True,
                                            nothingFound="No options found",
                                        ),
                                        html.Div(
                                            id="target-warning",
                                            style={"padding-top": "10px"},
                                        ),
                                    ]
                                )
                            ],
                            className="col-12",
                        )
                    ]
                )
            ]
        ),
    ],
    className="mt-3 w-100",
)


def create_info_label(target):
    return dmc.AccordionControl(target)


def create_info_item(info):
    children = []
    for i in range(len(info)):
        if i == 1:
            children.append(
                html.Img(src=dash.get_asset_url(info[0]), className="w-100 mb-2")
            )
        elif i == 0:
            children.append(dmc.Text(info[1], className="text-body", size="sm"))
            children.append(html.Br())
        else:
            children.append(dmc.Text(info[i], className="text-body", size="sm"))
            children.append(html.Br())
    return dmc.AccordionPanel(children, className="flex")


def retrieve_target_info(target):
    target_num = str(
        sdg_info[sdg_info["Shortened Target"] == target][["Target Number"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .loc[0]
    )
    goal_num = int(target_num.split(".")[0].split(" ")[-1])
    goal_name = list(
        sdg_info[
            sdg_info["Target Number"] == str(target_num.split(" ")[5].split("\n")[0])
        ][["Main SDG"]].values
    )[0]

    info = []
    info.append("goal-images/" + str(goal_num) + ".png")
    info.append("This target is under the goal of " + goal_name + ".")
    for goal_info in goals_information[goal_num - 1]:
        info.append(goal_info)

    return info


info_card = dbc.Card(
    children=[
        dbc.CardHeader("Chosen Target Information", className="w-100"),
        dbc.CardBody(
            children=[
                html.H6(
                    "Select a target to view their details.",
                    id="target-info-desc",
                    className="text-center",
                ),
                dmc.Accordion(
                    chevronPosition="right",
                    variant="separated",
                    children=[],
                    id="target-info-accordion",
                ),
            ],
            className="w-100",
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
)

choropleth_card = dbc.Card(
    children=[
        dbc.CardHeader("Choropleth Map of the Indicators", className="w-100"),
        dbc.CardBody(
            children=[
                dcc.Loading(dcc.Graph(figure=generate_choropleth(), id="choropleth")),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    className="text-center",
                    id="choropleth_desc",
                ),
            ],
            className="w-100",
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
)

heatmap_card = dbc.Card(
    children=[
        dbc.CardHeader(
            "Correlation of the Goals based on the National Data",
            className="w-100",
            id="heatmap_title",
        ),
        dbc.CardBody(
            children=[
                dcc.Loading(
                    dcc.Graph(figure=generate_heatmap("PHILIPPINES"), id="heatmap")
                ),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    className="text-center",
                    id="heatmap_desc",
                ),
            ],
            className="w-100",
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
)


def create_linechart_card(region, target, desc):
    return dbc.Card(
        children=[
            dbc.CardHeader(
                'Line Chart of the Indicators under the target, "' + target + '"',
                className="w-100",
            ),
            dbc.CardBody(
                children=[
                    dcc.Loading(dcc.Graph(figure=generate_linechart(region, target))),
                    dmc.Divider(variant="dotted", className="p-2"),
                    html.H6(
                        children=desc,
                        className="text-center",
                    ),
                ]
            ),
        ],
        className="mt-3 flex justify-content-center align-items-center",
    )


layout = dbc.Container(
    children=[
        html.H2("Region-Focused Tab", id="title"),
        control_card,
        dbc.Row(
            children=[
                dbc.Col(
                    children=[choropleth_card, heatmap_card], className="col-6 ps-0"
                ),
                dbc.Col(
                    children=[info_card, html.Div(children=[], id="linechart_div")],
                    className="col-6 pe-0",
                ),
            ],
            className="mx-0 w-100",
        ),
    ],
    className="p-5",
    style={
        "background-image": 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/background/bg3.jpg")',
        "background-size": "cover",
        "min-width": "100vw",
    },
)


@callback(
    Output("target-dropdown", "error"),
    Output("target-info-desc", "children"),
    Input("target-dropdown", "value"),
)
def update_text(target):
    if target == None or len(target) < 1:
        return "Select at least one target.", "Select a target to view their details."
    return "", ""


@callback(
    Output("target-info-accordion", "children"), Input("target-dropdown", "value")
)
def update_accordion(targets):
    children = []
    if targets:
        for target in targets:
            children.append(
                dmc.AccordionItem(
                    [
                        create_info_label(target),
                        create_info_item(retrieve_target_info(target)),
                    ],
                    value=target,
                )
            )

    return children


@callback(
    Output("title", "children"),
    Output("heatmap", "figure"),
    Output("heatmap_title", "children"),
    Output("heatmap_desc", "children"),
    Output("linechart_div", "children"),
    Input("target-dropdown", "value"),
    Input("choropleth", "clickData"),
)
def update_charts(targets, choropleth_click):
    title = "Region-Focused Tab"
    region = "PHILIPPINES"
    if choropleth_click != None:
        region = choropleth_click["points"][0]["location"]

    heatmap_title = "Correlation of the Goals based on the National Data"
    if region != "PHILIPPINES":
        heatmap_title = "Correlation of the Goals based on " + region + " Data"
        title = "Region-Focused Tab: " + region

    heatmap_info = [reg_heatmap_desc]

    linechart_info = [
        reg_linechart_desc,
        html.Br(),
        html.Br(),
        reg_linechart_tip,
    ]

    linechart_cards = []
    if targets:
        for target in targets:
            linechart_cards.append(
                create_linechart_card(region, target, linechart_info)
            )

    return (title, generate_heatmap(region), heatmap_title, heatmap_info, linechart_cards)
