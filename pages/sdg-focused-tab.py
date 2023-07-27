import pandas as pd
from dash import html, dcc, Dash, Input, Output, State, callback, register_page
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

register_page(__name__, name="SDG-focused Tab", path="/sdg-focused-tab")

sdg_data = pd.read_csv(
    "https://raw.githubusercontent.com/francheska-vicente/datapre-project/main_v2/data_output/combined_data.csv"
)
sdg_regions_available = sdg_data["Geolocation"].unique()[1:]
sdg_indicators_available = sdg_data.columns[2:]

linechart_desc_default = "Choose an indicator to track its progress over the years."
barchart_desc_default = "Choose an indicator to compare its progress between all regions for the latest year."


def generate_linechart(regions_selected, indicator):
    two_region = pd.DataFrame()

    if len(regions_selected) == 0:
        regions_selected.append("PHILIPPINES")

    for region in regions_selected:
        if len(indicator) > 1:
            temp_region = sdg_data[sdg_data["Geolocation"] == region][
                ["Year", indicator[0], indicator[1]]
            ]
        else:
            temp_region = sdg_data[sdg_data["Geolocation"] == region][
                ["Year", indicator[0]]
            ]

        temp_region = pd.concat([sdg_data["Geolocation"], temp_region], axis=1)

        temp_region = temp_region.dropna(thresh=len(indicator) + 1)
        temp_region["Year"] = temp_region["Year"].astype("int")

        two_region = pd.concat([two_region, temp_region])

    two_region = two_region.reset_index(drop=True)
    indicator = indicator[0]
    label = " ".join(indicator.split(" ")[1:])
    df_visualization = two_region[["Geolocation", "Year", indicator]]
    df_visualization = df_visualization.dropna()

    fig = px.line(
        df_visualization,
        x="Year",
        y=indicator,
        markers=True,
        labels={indicator: label},
        color="Geolocation",
    )
    title = " ".join(indicator.split(" ")[1:]) + " per Year"
    fig.update_layout(
        # TITLE
        title={"text": title, "y": 0.95, "x": 0.5},
        title_font_family="Cambria",
        title_font_color="#000000",
        title_font_size=20,
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
        yaxis_title=label,
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

    return fig


def generate_barchart(regions_selected, indicator):
    two_region = pd.DataFrame()

    if len(regions_selected) == 0:
        regions_selected.append("PHILIPPINES")

    if len(indicator) > 1:
        temp_region = sdg_data[["Year", indicator[0], indicator[1]]]
    else:
        temp_region = sdg_data[["Year", indicator[0]]]

    temp_region = pd.concat([sdg_data["Geolocation"], temp_region], axis=1)
    temp_region = temp_region[temp_region["Geolocation"] != "PHILIPPINES"]
    temp_region = temp_region.dropna(thresh=len(indicator) + 1)
    temp_region["Year"] = temp_region["Year"].astype("int")

    two_region = pd.concat([two_region, temp_region])

    two_region = two_region.reset_index(drop=True)

    geolocation_values = []
    for temp in sdg_data["Geolocation"].unique()[1:]:
        temp = temp.split(":")
        geolocation_values.append(temp[1])

    indicator = indicator[0]
    label = " ".join(indicator.split(" ")[1:])
    df_visualization = two_region[["Geolocation", "Year", indicator]]
    df_visualization = df_visualization.dropna()

    year_values = df_visualization["Year"].unique()

    df_visualization_curr = df_visualization[
        df_visualization["Year"] == year_values[-1]
    ]
    df_visualization_curr = df_visualization_curr.drop_duplicates()
    fig = px.bar(
        df_visualization_curr,
        x=indicator,
        y=geolocation_values,
        labels={indicator: label},
        color="Geolocation",
    )
    title = " ".join(indicator.split(" ")[1:]) + " of the Year " + str(year_values[-1])

    fig.update_layout(
        # TITLE
        title={"text": title, "y": 0.95, "x": 0.5},
        title_font_family="Cambria",
        title_font_color="#000000",
        title_font_size=20,
        # axis font
        font_family="Cambria",
        font_color="#000000",
        # x-axis
        xaxis_title=label,
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="#000000",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Cambria",
                size=14,
                color="#000000",
            ),
        ),
        # y-axis
        yaxis_title="Geolocation",
        yaxis=dict(
            {"categoryorder": "total ascending"},  # ascending values from bottom to top
            showgrid=False,
            showline=True,
            showticklabels=True,
            linecolor="#000000",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Cambria",
                size=10,
                color="#000000",
            ),
        ),
        autosize=True,
        showlegend=True,
        plot_bgcolor="light grey",
    )

    fig.update_xaxes(type="category")

    return fig


control_card = dbc.Card(
    children=[
        dbc.CardHeader("Chart Controls for the Regions and Indicators"),
        dbc.CardBody(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                dbc.Row(
                                    children=[
                                        html.H6(
                                            "What are the regions you want to visualize? (Maximum of 2)"
                                        ),
                                        dmc.MultiSelect(
                                            id="region-dropdown",
                                            data=[
                                                {"label": i, "value": i}
                                                for i in sdg_regions_available
                                            ],
                                            description="You can select a maximum of two regions.",
                                            searchable=True,
                                            clearable=True,
                                            maxSelectedValues=2,
                                            nothingFound="No options found",
                                        ),
                                        html.Div(
                                            id="region-warning",
                                            style={"padding-top": "10px"},
                                        ),
                                    ]
                                )
                            ],
                            className="col-6",
                        ),
                        dbc.Col(
                            children=[
                                dbc.Row(
                                    children=[
                                        html.H6(
                                            "What are the indicators you want to visualize? (Maximum of 2)"
                                        ),
                                        dmc.MultiSelect(
                                            id="indicator-dropdown",
                                            data=[
                                                {"label": i, "value": i}
                                                for i in sdg_indicators_available
                                            ],
                                            description="You can select a maximum of two regions.",
                                            searchable=True,
                                            clearable=True,
                                            maxSelectedValues=2,
                                            nothingFound="No options found",
                                        ),
                                        html.Div(
                                            id="indicator-warning",
                                            style={"padding-top": "10px"},
                                        ),
                                    ]
                                )
                            ],
                            className="col-6",
                        ),
                    ]
                )
            ]
        ),
    ],
    className="mt-3 w-100",
)


def create_info_label(item):
    return dmc.AccordionControl(item)


def create_info_item(info):
    return dmc.AccordionPanel(dmc.Text(info, size="sm"))


region_info_card = dbc.Card(
    children=[
        dbc.CardHeader("Chosen Region Information", className="w-100"),
        dbc.CardBody(
            children=[
                html.H6(
                    "Select a region to view their details.",
                    id="region-info-desc",
                    className="text-center",
                ),
                dmc.AccordionMultiple(
                    chevronPosition="right",
                    variant="separated",
                    children=[],
                    id="region-info-accordion",
                ),
            ],
            className="w-100",
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
)

indicator_info_card = dbc.Card(
    children=[
        dbc.CardHeader("Chosen Indicator Information", className="w-100"),
        dbc.CardBody(
            children=[
                html.H6(
                    "Select an indicator to view their details.",
                    id="indicator-info-desc",
                    className="text-center",
                ),
                dmc.AccordionMultiple(
                    chevronPosition="right",
                    variant="separated",
                    children=[],
                    id="indicator-info-accordion",
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
                html.H6("chika hir", className="text-center"),
                html.Img(
                    src=dash.get_asset_url("map.png"), style={"max-width": "100%"}
                ),
            ]
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
)

linechart1_card = dbc.Card(
    children=[
        dbc.CardHeader("Line Chart", className="w-100"),
        dbc.CardBody(
            children=[
                dcc.Graph(figure=px.line(), id="linechart1"),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    linechart_desc_default,
                    className="text-center",
                    id="linechart1_desc",
                ),
            ],
            className="w-100",
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
)


def generate_linechart2card(regions, indicator):
    return dbc.Card(
        children=[
            dbc.CardHeader("Line Chart", className="w-100"),
            dbc.CardBody(
                children=[
                    dcc.Graph(
                        figure=generate_linechart(regions, indicator), id="linechart2"
                    ),
                    dmc.Divider(variant="dotted", className="p-2"),
                    html.H6(
                        "[Short description of results here.]",
                        className="text-center",
                        id="linechart2_desc",
                    ),
                ],
                className="w-100",
            ),
        ],
        className="mt-3 flex justify-content-center align-items-center",
    )


linechart2_card = html.Div(id="linechart2_card")

barchart1_card = dbc.Card(
    children=[
        dbc.CardHeader("Bar Chart", className="w-100"),
        dbc.CardBody(
            children=[
                dcc.Graph(figure=px.bar(), id="barchart1"),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    barchart_desc_default,
                    className="text-center",
                    id="barchart1_desc",
                ),
            ],
            className="w-100",
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
)


def generate_barchart2card(regions, indicator):
    return dbc.Card(
        children=[
            dbc.CardHeader("Bar Chart", className="w-100"),
            dbc.CardBody(
                children=[
                    dcc.Graph(
                        figure=generate_barchart(regions, indicator), id="barchart2"
                    ),
                    dmc.Divider(variant="dotted", className="p-2"),
                    html.H6(
                        "[Short description of results here.]",
                        className="text-center",
                        id="barchart2_desc",
                    ),
                ],
                className="w-100",
            ),
        ],
        className="mt-3 flex justify-content-center align-items-center",
    )


barchart2_card = html.Div(id="barchart2_card")

layout = dbc.Container(
    children=[
        html.H2("SGD-Focused Tab"),
        control_card,
        dbc.Row(
            children=[
                dbc.Col(
                    children=[region_info_card, choropleth_card], className="col-6 ps-0"
                ),
                dbc.Col(
                    children=[
                        indicator_info_card,
                        linechart1_card,
                        linechart2_card,
                        barchart1_card,
                        barchart2_card,
                    ],
                    className="col-6 pe-0",
                ),
            ],
            className="mx-0 w-100",
        ),
    ],
    className="p-5",
    style={
        "background-image": 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/bg2.jpg")',
        "background-size": "cover",
        "min-width": "100vw",
    },
)


@callback(Output("region-dropdown", "error"), Output("region-info-desc", "children"), Input("region-dropdown", "value"))
def update_text(region):
    if region == None or len(region) < 1:
        return "Select at least one region.", "Select a region to view their details."
    return "", ""

@callback(Output("indicator-dropdown", "error"), Output("indicator-info-desc", "children"), Input("indicator-dropdown", "value"))
def update_text(indicator):
    if indicator == None or len(indicator) < 1:
        return "Select at least one indicator.", "Select a indicator to view their details."
    return "", ""

@callback(
    Output("region-info-accordion", "children"), Input("region-dropdown", "value")
)
def update_accordion(regions):
    children = []
    if regions:
        for region in regions:
            children.append(
                dmc.AccordionItem(
                    [
                        create_info_label(region),
                        create_info_item("[Short description of the region here.]"),
                    ],
                    value=region,
                )
            )

    return children

@callback(
    Output("indicator-info-accordion", "children"), Input("indicator-dropdown", "value")
)
def update_accordion(indicators):
    children = []
    if indicators:
        for indicator in indicators:
            children.append(
                dmc.AccordionItem(
                    [
                        create_info_label(indicator),
                        create_info_item("[Short description of the indicator here.]"),
                    ],
                    value=indicator,
                )
            )

    return children

@callback(
    Output("linechart1", "figure"),
    Output("barchart1", "figure"),
    Output("linechart1_desc", "children"),
    Output("barchart1_desc", "children"),
    Input("region-dropdown", "value"),
    Input("indicator-dropdown", "value"),
)
def update_linechart(regions, indicators):
    if indicators and len(indicators) >= 1:
        if regions == None:
            return (
                generate_linechart([], indicators),
                generate_barchart([], indicators),
                "[Short description of results here.]",
                "[Short description of results here.]",
            )
        elif regions and len(regions) < 3:
            return (
                generate_linechart(regions, indicators),
                generate_barchart(regions, indicators),
                "[Short description of results here.]",
                "[Short description of results here.]",
            )
    return (
        px.line(),
        px.bar(),
        linechart_desc_default,
        barchart_desc_default,
    )


@callback(
    Output("linechart2_card", "children"),
    Output("barchart2_card", "children"),
    Input("region-dropdown", "value"),
    Input("indicator-dropdown", "value"),
)
def update_linechart(regions, indicators):
    if indicators and len(indicators) == 2:
        if regions == None:
            return generate_linechart2card([], [indicators[1]]), generate_barchart2card(
                [], [indicators[1]]
            )
        elif regions and len(regions) < 3:
            return generate_linechart2card(
                regions, [indicators[1]]
            ), generate_barchart2card(regions, [indicators[1]])
    return "", ""






