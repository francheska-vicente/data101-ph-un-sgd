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
sdg_columns = sdg_data.columns[:-15]
sdg_data = sdg_data[sdg_columns]
sdg_score = pd.read_csv("data/sdg_target_score.csv")
sdg_info = pd.read_csv("data/sdg_infov3.csv")
sdg_regions_available = sdg_data["Geolocation"].unique()[1:]
sdg_indicators_available = sdg_data.columns[2:]

linechart_desc_default = "Choose an indicator to track its progress over the years."
barchart_desc_default = "Choose an indicator to compare its progress between all regions for the latest year."

barchart1_is_ascending = False
barchart2_is_ascending = False


def generate_linechart(regions_selected, indicator):
    two_region = pd.DataFrame()

    if len(regions_selected) == 0:
        regions_selected.append("PHILIPPINES")

    for region in regions_selected:
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

    x = 0
    while indicator != sdg_score.iloc[x]["Indicator"]:
        x = x + 1

    y = 0
    while y < len(df_visualization["Year"].unique()):
        target = " ".join(indicator.split(" ")[1:])
        new_row = {
            "Geolocation": "Target " + target,
            indicator: sdg_score.iloc[x]["Target"],
            "Year": df_visualization["Year"].unique()[y],
        }
        print (new_row)
        temp_row = pd.DataFrame (new_row, index = [0])
        df_visualization = pd.concat ([df_visualization, temp_row]).reset_index (drop = True)
        y = y + 1

    fig = px.line(
        df_visualization,
        x="Year",
        y=indicator,
        markers=True,
        labels={indicator: label},
        color="Geolocation",
    )
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


def generate_barchart(regions_selected, indicator, selected_year, is_ascending):
    two_region = pd.DataFrame()

    if len(regions_selected) == 0:
        regions_selected.append("PHILIPPINES")

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

    if selected_year == None:
        selected_year = year_values[-1]

    df_visualization_curr = df_visualization[
        df_visualization["Year"] == int(selected_year)
    ]

    df_visualization_curr = df_visualization_curr.drop_duplicates()
    regions_list = []

    for temp in df_visualization_curr ['Geolocation']:
        regions_list.append (temp.split (":")[0])

    fig = px.bar(
        df_visualization_curr,
        x=indicator,
        y=regions_list,
        labels={indicator: label},
        color=regions_list,
    )

    fig.update_layout(
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
            {
                "categoryorder": "total ascending"
                if is_ascending
                else "total descending"
            },
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


    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def get_latest_year(indicator):
    temp_region = sdg_data[["Geolocation", "Year", indicator]]
    temp_region = temp_region[temp_region["Geolocation"] != "PHILIPPINES"]
    temp_region = temp_region.dropna(thresh=len([indicator]) + 1)
    temp_region["Year"] = temp_region["Year"].astype("int")
    temp_region = temp_region.dropna()
    year_values = temp_region["Year"].unique()
    return year_values[-1]


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
        dbc.CardHeader("Line Chart", id="linechart1_title", className="w-100"),
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

linechart2_card = dbc.Card(
    children=[
        dbc.CardHeader("Line Chart", id="linechart2_title", className="w-100"),
        dbc.CardBody(
            children=[
                dcc.Graph(figure=px.line(), id="linechart2"),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    linechart_desc_default,
                    className="text-center",
                    id="linechart2_desc",
                ),
            ],
            className="w-100",
        ),
    ],
    className="hidden mt-3 flex justify-content-center align-items-center",
    id="linechart2_card",
)

barchart1_card = dbc.Card(
    children=[
        dbc.CardHeader("Bar Chart", id="barchart1_title", className="w-100"),
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

barchart2_card = dbc.Card(
    children=[
        dbc.CardHeader("Bar Chart", id="barchart2_title", className="w-100"),
        dbc.CardBody(
            children=[
                dcc.Graph(figure=px.bar(), id="barchart2"),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    barchart_desc_default,
                    className="text-center",
                    id="barchart2_desc",
                ),
            ],
            className="w-100",
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
    id="barchart2_card",
)

layout = dbc.Container(
    children=[
        html.H2("SGD-Focused Tab"),
        control_card,
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        region_info_card,
                        choropleth_card,
                        barchart1_card,
                        barchart2_card,
                    ],
                    className="col-6 ps-0",
                ),
                dbc.Col(
                    children=[indicator_info_card, linechart1_card, linechart2_card],
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


@callback(
    Output("region-dropdown", "error"),
    Output("region-info-desc", "children"),
    Input("region-dropdown", "value"),
)
def update_text(region):
    if region == None or len(region) < 1:
        return "Select at least one region.", "Select a region to view their details."
    return "", ""


@callback(
    Output("indicator-dropdown", "error"),
    Output("indicator-info-desc", "children"),
    Input("indicator-dropdown", "value"),
)
def update_text(indicator):
    if indicator == None or len(indicator) < 1:
        return (
            "Select at least one indicator.",
            "Select a indicator to view their details.",
        )
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
    Output("linechart1_title", "children"),
    Output("barchart1", "figure"),
    Output("barchart1_title", "children"),
    Output("linechart1_desc", "children"),
    Output("barchart1_desc", "children"),
    Output("linechart2", "figure"),
    Output("linechart2_title", "children"),
    Output("barchart2", "figure"),
    Output("barchart2_title", "children"),
    Output("linechart2_desc", "children"),
    Output("barchart2_desc", "children"),
    Input("region-dropdown", "value"),
    Input("indicator-dropdown", "value"),
    Input("linechart1", "clickData"),
    Input("linechart2", "clickData"),
    Input("barchart1", "clickData"),
    Input("barchart2", "clickData"),
)
def update_charts(
    regions,
    indicators,
    linechart1_click,
    linechart2_click,
    barchart1_click,
    barchart2_click,
):
    year = None
    if linechart1_click != None:
        year = linechart1_click["points"][0]["x"]
    if linechart2_click != None:
        year = linechart2_click["points"][0]["x"]

    if barchart1_click != None:
        global barchart1_is_ascending
        barchart1_is_ascending = not barchart1_is_ascending

    if barchart2_click != None:
        global barchart2_is_ascending
        barchart2_is_ascending = not barchart2_is_ascending

    if regions == None:
        regions = []

    if indicators != None and len(indicators) == 1:
        return (
            generate_linechart(regions, indicators),
            "Line Chart of the " + " ".join(indicators[0].split(" ")[1:]) + " per Year",
            generate_barchart(regions, indicators, year, barchart1_is_ascending),
            "Bar Chart of the "
            + " ".join(indicators[0].split(" ")[1:])
            + " of the Year "
            + str(get_latest_year(indicators[0])),
            [
                "This linechart provides a visual representation of the selected indicator's trend over the years, represented by the blue line. The red line (if available) signifies the target goal for the indicator; closer proximity between the blue and red data points indicates better progress for the specific year.",
                html.Br(),
                html.Br(),
                "Click on a data point to see the information for that specific year on the bar graphs.",
            ],
            [
                "This barchart allows you to compare the progress of the chosen indicator between regions for a specific year. Each bar represents a region, and its length corresponds to the value of the indicator for that region.",
                html.Br(),
                html.Br(),
                "Click on the bars to toggle the arrangement between ascending and descending.",
            ],
            px.line(),
            "Line Chart",
            px.bar(),
            "Bar Chart",
            linechart_desc_default,
            barchart_desc_default,
        )
    elif indicators != None and len(indicators) == 2:
        return (
            generate_linechart(regions, [indicators[0]]),
            "Line Chart of the " + " ".join(indicators[0].split(" ")[1:]) + " per Year",
            generate_barchart(regions, [indicators[0]], year, barchart1_is_ascending),
            "Bar Chart of the "
            + " ".join(indicators[0].split(" ")[1:])
            + " of the Year "
            + str(get_latest_year(indicators[0])),
            [
                "This linechart provides a visual representation of the selected indicator's trend over the years, represented by the blue line. The red line (if available) signifies the target goal for the indicator; closer proximity between the blue and red data points indicates better progress for the specific year.",
                html.Br(),
                html.Br(),
                "Click on a data point to see the information for that specific year on all the graphs.",
            ],
            [
                "This barchart allows you to compare the progress of the chosen indicator between regions for a specific year. Each bar represents a region, and its length corresponds to the value of the indicator for that region.",
                html.Br(),
                html.Br(),
                "Click on the bars to toggle the arrangement between ascending and descending.",
            ],
            generate_linechart(regions, [indicators[1]]),
            "Line Chart of the " + " ".join(indicators[1].split(" ")[1:]) + " per Year",
            generate_barchart(regions, [indicators[1]], year, barchart2_is_ascending),
            "Bar Chart of the "
            + " ".join(indicators[1].split(" ")[1:])
            + " of the Year "
            + str(get_latest_year(indicators[1])),
            [
                "This linechart provides a visual representation of the selected indicator's trend over the years, represented by the blue line. The red line (if available) signifies the target goal for the indicator; closer proximity between the blue and red data points indicates better progress for the specific year.",
                html.Br(),
                html.Br(),
                "Click on a data point to see the information for that specific year on all the graphs.",
            ],
            [
                "This barchart allows you to compare the progress of the chosen indicator between regions for a specific year. Each bar represents a region, and its length corresponds to the value of the indicator for that region.",
                html.Br(),
                html.Br(),
                "Click on the bars to toggle the arrangement between ascending and descending.",
            ],
        )
    return (
        px.line(),
        "Line Chart",
        px.bar(),
        "Bar Chart",
        linechart_desc_default,
        barchart_desc_default,
        px.line(),
        "Line Chart",
        px.bar(),
        "Bar Chart",
        linechart_desc_default,
        barchart_desc_default,
    )
