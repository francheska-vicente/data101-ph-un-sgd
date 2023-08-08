import numpy as np
import pandas as pd
import scipy
from dash import html, dcc, Input, Output, callback, register_page, callback_context
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import os

from data import *
from constants import *

register_page(__name__, name="SDG-focused Tab", path="/sdg-focused-tab")

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

        temp_row = pd.DataFrame(new_row, index=[0])
        df_visualization = pd.concat([df_visualization, temp_row]).reset_index(
            drop=True
        )
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

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

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

    for temp in df_visualization_curr["Geolocation"]:
        regions_list.append(temp.split(":")[0])

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


def generate_choropleth(indicators_selected, selected_year):
    if len (indicators_selected) == 1:
        fig = choropleth_one_indicator (indicators_selected, selected_year)
    else:
        fig = choropleth_two_indicator (indicators_selected)
    return fig

def choropleth_one_indicator (indicators_selected, selected_year):
    choropleth_data = create_choropleth_data(indicators_selected [0], selected_year)
    fig = px.choropleth_mapbox(choropleth_data[0],
                          geojson=region.geometry,
                          locations='Geolocation',
                          color=choropleth_data[1],
                          center={'lat': 12.099, 'lon': 122.733}, 
                          zoom = 4)
    return fig

def choropleth_two_indicator (indicators_selected):
    df = create_choropleth_df (indicators_selected)
    fig = px.choropleth_mapbox(df,
                          geojson=region.geometry,
                          locations='Geolocation',
                          color=df.columns [1],
                          center={'lat': 12.099, 'lon': 122.733}, 
                          zoom = 4)
    return fig

def create_choropleth_data(selected_indicator, selected_year):
    # check if a csv file for this indicator already exists
    check_file = os.path.isfile(selected_indicator+'.csv')
    
    # if csv file does not exist
    if check_file == False:
        gdf = gdf_shp[['geometry', 'Geolocation', 'Year', selected_indicator]]
        pvt_gdf = pd.pivot_table(gdf, index='Geolocation', columns='Year', values=selected_indicator).reset_index()
        pvt_gdf.to_csv('./data/indicator_csv/'+selected_indicator+'.csv', index = False)
    
    pvt_gdf = pd.read_csv('./data/indicator_csv/'+selected_indicator+'.csv')
    
    # Checking if there is year data based on the selected year and selected indicator 
    year_list = pvt_gdf.columns [1:]
        
    if selected_year == None:
        selected_year = year_list [-1]
    pvt_gdf = pvt_gdf[['Geolocation',  selected_year]]
    print('\n[SDG Indicator] ' + selected_indicator)
    print('[Year Data] ' + selected_year)
    return pvt_gdf, str(selected_year)

def create_choropleth_df (indicators_selected):
    ind_1 = pd.read_csv('./data/indicator_csv/'+indicators_selected[0]+'.csv')
    ind_1_T = ind_1.T
    ind_2 = pd.read_csv('./data/indicator_csv/'+indicators_selected[1]+'.csv')
    ind_2_T = ind_2.T
    df = pd.DataFrame([])
    for i in range(17): 
        j = 1
        print(i)
        data_regional_1 = ind_1_T[i]
        data_regional_2 = ind_2_T[i]
    
        if i == 3:
            j = 3
        x = np.array(data_regional_1[j:])
        y = np.array(data_regional_2[j:])
    
        r, p = scipy.stats.pearsonr(x, y)
        temp_df = pd.DataFrame ({'Geolocation': data_regional_1[0], 'Correlation': r}, index = [0])
        df = pd.concat ([df, temp_df])

    return df

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
    return dmc.AccordionControl(item, className="text-body fw-bold")


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


def retrieve_region_info(region):
    info = []
    info.append(
        "region-images/"
        + region_images[list(region_info["Region"].unique()).index(region)]
    )

    region_information = list(
        region_info[region_info["Region"] == region]["Description"].values
    )
    for region_infor in region_information:
        info.append(region_infor)
    return info


def retrieve_indicator_info(indicator):
    goal_num = int(indicator.split(".")[0])
    target_num = indicator.split(" ")[0][slice(4)]
    goal_name = list(
        sdg_info[sdg_info["Target Number"] == target_num][["Main SDG"]].values
    )[0]

    info = []
    info.append("goal-images/" + str(goal_num) + ".png")
    info.append("This indicator is under the goal of " + goal_name + ".")
    for goal_info in goals_information[goal_num - 1]:
        info.append(goal_info)

    return info


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
    id="region_info_card",
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
    id="indicator_info_card",
)

choropleth_card = dbc.Card(
    children=[
        dbc.CardHeader("Choropleth Map of the Indicators", className="w-100"),
        dbc.CardBody(
            children=[
                dcc.Loading(dcc.Graph(figure=px.choropleth(), id="choropleth")),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    sdg_linechart_desc_default,
                    className="text-center",
                    id="choropleth_desc",
                ),
            ],
            className="w-100",
        ),
    ],
    className="mt-3 flex justify-content-center align-items-center",
)

linechart1_card = dbc.Card(
    children=[
        dbc.CardHeader("Line Chart", id="linechart1_title", className="w-100"),
        dbc.CardBody(
            children=[
                dcc.Loading(dcc.Graph(figure=px.line(), id="linechart1")),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    sdg_linechart_desc_default,
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
                dcc.Loading(dcc.Graph(figure=px.line(), id="linechart2")),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    sdg_linechart_desc_default,
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
                dcc.Loading(dcc.Graph(figure=px.bar(), id="barchart1")),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    sdg_barchart_desc_default,
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
                dcc.Loading(dcc.Graph(figure=px.bar(), id="barchart2")),
                dmc.Divider(variant="dotted", className="p-2"),
                html.H6(
                    sdg_barchart_desc_default,
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
        "background-image": 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/background/bg2.jpg")',
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
                        create_info_item(retrieve_region_info(region)),
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
                        create_info_item(retrieve_indicator_info(indicator)),
                    ],
                    value=indicator,
                )
            )

    return children


@callback(
    Output("choropleth", "figure"),
    Output("choropleth_desc", "children"),
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
    Output("linechart2_card", "style"),
    Output("barchart2_card", "style"),
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
    global barchart1_is_ascending, barchart2_is_ascending
    year = None
    if linechart1_click != None:
        year = linechart1_click["points"][0]["x"]
    if linechart2_click != None:
        year = linechart2_click["points"][0]["x"]

    if callback_context.triggered[0]["prop_id"] == "barchart1.clickData":
        barchart1_is_ascending = not barchart1_is_ascending
    elif callback_context.triggered[0]["prop_id"] == "barchart2.clickData":
        barchart2_is_ascending = not barchart2_is_ascending

    if regions == None:
        regions = []

    linechart_info = [
        sdg_linechart_desc,
        html.Br(),
        html.Br(),
        sdg_linechart_tip,
    ]

    barchart_info = [
        sdg_barchart_desc,
        html.Br(),
        html.Br(),
        sdg_barchart_tip,
    ]

    choropleth1_info = [
        sdg_choropleth_desc1
    ]

    choropleth2_info = [
        sdg_choropleth_desc2,
        html.Br(),
        html.Br(),
        sdg_choropleth_tip2,
    ]

    if indicators != None and len(indicators) == 1:
        return (
            generate_choropleth(indicators, year),
            choropleth1_info,
            generate_linechart(regions, indicators),
            "Line Chart of the " + " ".join(indicators[0].split(" ")[1:]) + " per Year",
            generate_barchart(regions, indicators, year, barchart1_is_ascending),
            "Bar Chart of the "
            + " ".join(indicators[0].split(" ")[1:])
            + " of the Year "
            + (str(get_latest_year(indicators[0])) if year == None else year),
            linechart_info,
            barchart_info,
            px.line(),
            "Line Chart",
            px.bar(),
            "Bar Chart",
            sdg_linechart_desc_default,
            sdg_barchart_desc_default,
            {"display": "none"},
            {"display": "none"},
        )
    elif indicators != None and len(indicators) == 2:
        return (
            generate_choropleth(indicators, year),
            choropleth2_info,
            generate_linechart(regions, [indicators[0]]),
            "Line Chart of the " + " ".join(indicators[0].split(" ")[1:]) + " per Year",
            generate_barchart(regions, [indicators[0]], year, barchart1_is_ascending),
            "Bar Chart of the "
            + " ".join(indicators[0].split(" ")[1:])
            + " of the Year "
            + (str(get_latest_year(indicators[0])) if year == None else year),
            linechart_info,
            barchart_info,
            generate_linechart(regions, [indicators[1]]),
            "Line Chart of the " + " ".join(indicators[1].split(" ")[1:]) + " per Year",
            generate_barchart(regions, [indicators[1]], year, barchart2_is_ascending),
            "Bar Chart of the "
            + " ".join(indicators[1].split(" ")[1:])
            + " of the Year "
            + (str(get_latest_year(indicators[1])) if year == None else year),
            linechart_info,
            barchart_info,
            {"display": "block"},
            {"display": "block"},
        )
    return (
        blank_chart,
        sdg_choropleth_desc_default,
        blank_chart,
        "Line Chart",
        blank_chart,
        "Bar Chart",
        sdg_linechart_desc_default,
        sdg_barchart_desc_default,
        blank_chart,
        "Line Chart",
        blank_chart,
        "Bar Chart",
        sdg_linechart_desc_default,
        sdg_barchart_desc_default,
        {"display": "none"},
        {"display": "none"},
    )
