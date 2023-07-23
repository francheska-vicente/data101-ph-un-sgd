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

control_card = dbc.Card (children = [
            dbc.CardHeader ('Chart Controls for the Regions and Indicators'),
            dbc.CardBody (children = [
                dbc.Row (children = [
                    dbc.Col (children = [
                        dbc.Row (children = [
                            html.H6 ('What are the regions you want to visualize? (Maximum of 2)'),
                            dmc.MultiSelect(
                                id = 'region-dropdown',
                                data = [{'label': i, 'value': i} for i in sdg_regions_available],
                                description="You can select a maximum of two regions.",
                                searchable=True,
                                clearable=True,
                                maxSelectedValues=2,
                                nothingFound="No options found",
                            ),
                            html.Div (id = 'region-warning', style = {'padding-top' : '10px'})
                        ])
                    ], className = 'col-6'),
                    dbc.Col (children = [
                        dbc.Row (children = [
                            html.H6 ('What are the indicators you want to visualize? (Maximum of 2)'),
                            dmc.MultiSelect(
                                id = 'indicator-dropdown',
                                data = [{'label': i, 'value': i} for i in sdg_indicators_available],
                                description="You can select a maximum of two regions.",
                                searchable=True,
                                clearable=True,
                                maxSelectedValues=2,
                                nothingFound="No options found",
                            ),
                            html.Div (id = 'indicator-warning', style = {'padding-top' : '10px'})
                        ])
                    ], className = 'col-6')
                ])
            ])
        ], className="mt-3 w-100")

def create_info_label(item):
    return dmc.AccordionControl(item)

def create_info_item(info):
    return dmc.AccordionPanel(dmc.Text(info, size="sm"))

region_info_card = dbc.Card (children = [
        dbc.CardHeader ('Chosen Region Information', className="w-100"),
        dbc.CardBody (children = [
            html.H6 ('Select a region to view their details.', id='region-info-desc', className="text-center"),
            dmc.AccordionMultiple(
                chevronPosition="right",
                variant="separated",
                children=[],
                id="region-info-accordion"
            )
        ])
    ], className="mt-3 flex justify-content-center align-items-center")

indicator_info_card = dbc.Card (children = [
        dbc.CardHeader ('Chosen Indicator Information', className="w-100"),
        dbc.CardBody (children = [
            html.H6 ('Select an indicator to view their details.', id='indicator-info-desc', className="text-center"),
            dmc.AccordionMultiple(
                chevronPosition="right",
                variant="separated",
                children=[],
                id="indicator-info-accordion"
            )
        ])
    ], className="mt-3 flex justify-content-center align-items-center")

choropleth_card = dbc.Card (children = [
            dbc.CardHeader ('Choropleth Map of the Indicators', className="w-100"),
            dbc.CardBody (children = [
                html.H6 ('chika hir', className="text-center"),
                html.Img (src = dash.get_asset_url ('map.png'),
                    style = {
                        'max-width' : '100%'
                        }
                    ),
            ])
        ], className="mt-3 flex justify-content-center align-items-center")

linechart_card = dbc.Card (children = [
            dbc.CardHeader ('Line Chart', className="w-100"),
            dbc.CardBody (children = [
                html.H6 ('chika hir', className="text-center"),
                html.Img (src = dash.get_asset_url ('linechart.png'),
                    style = {
                        'max-width' : '100%'
                        }
                    ),
            ])
        ], className="mt-3 flex justify-content-center align-items-center")

barchart_card = dbc.Card (children = [
            dbc.CardHeader ('Bar Chart', className="w-100"),
            dbc.CardBody (children = [
                html.H6 ('chika hir', className="text-center"),
                html.Img (src = dash.get_asset_url ('linechart.png'),
                    style = {
                        'max-width' : '100%'
                        }
                    ),
            ])
        ], className="mt-3 flex justify-content-center align-items-center")

layout = dbc.Container (children = [
        html.H2("SGD-Focused Tab"),
        control_card,
        dbc.Row (children =[
            dbc.Col (children = [
                region_info_card,
                choropleth_card
            ], className="col-6 ps-0"),
            dbc.Col (children = [
                indicator_info_card,
                linechart_card, 
                barchart_card
            ], className="col-6 pe-0")
        ], className="mx-0 w-100")
    ],
    className = 'p-5',
    style = {
        'background-image' : 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/bg2.jpg")',
        'background-size' : 'cover',
        'min-width' : '100vw'
    })

@callback(Output("region-dropdown", "error"), Input("region-dropdown", "value"))
def select_value(value):
    return "Select at least one region." if len(value) < 1 else ""

@callback(Output("indicator-dropdown", "error"), Input("indicator-dropdown", "value"))
def select_value(value):
    return "Select at least one indicator." if len(value) < 1 else ""

@callback(Output("region-info-accordion", "children"), Input("region-dropdown", "value"))
def update_accordion(regions):
    children = []
    for region in regions:
        children.append(
            dmc.AccordionItem([
                        create_info_label(region),
                        create_info_item('chuchu'),
                ], value=region,
            )
        )
    
    return children

@callback(Output("region-info-desc", "children"), Input("region-dropdown", "value"))
def update_text(regions):
    return "Select a region to view their details." if len(regions) < 1 else ""

@callback(Output("indicator-info-accordion", "children"), Input("indicator-dropdown", "value"))
def update_accordion(indicators):
    children = []
    for indicator in indicators:
        children.append(
            dmc.AccordionItem([
                        create_info_label(indicator),
                        create_info_item('chuchu'),
                ], value=indicator,
            )
        )
    
    return children

@callback(Output("indicator-info-desc", "children"), Input("indicator-dropdown", "value"))
def update_text(indicators):
    return "Select a target to view their details." if len(indicators) < 1 else ""