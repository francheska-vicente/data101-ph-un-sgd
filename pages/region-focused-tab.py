import pandas as pd
from dash import html, dcc, Dash, Input, Output, State, callback, register_page
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

register_page (
    __name__, 
    name = 'Region-focused Tab',
    path = '/region-focused-tab'
)

sdg_targets_df = pd.read_csv ('data/sdg_info_fixed.csv')
sdg_targets_df = sdg_targets_df ['Target'].unique ()

control_card = dbc.Card (children = [
            dbc.CardHeader ('Chart Controls for the Target', className="w-100"),
            dbc.CardBody (children = [
                dbc.Row (children = [
                    dbc.Col (children = [
                        dbc.Row (children = [
                            html.H6 ('What is the target you want to visualize?'),
                            dmc.MultiSelect(
                                id = 'target-dropdown',
                                data = [{'label': i, 'value': i} for i in sdg_targets_df],
                                description="You can select one or more targets.",
                                searchable=True,
                                clearable=True,
                                nothingFound="No options found",
                            ),
                            html.Div (id = 'target-warning', style = {'padding-top' : '10px'})
                        ])
                    ], className = 'col-12')
                ])
            ])
        ], className="mt-3 w-100")

def create_info_label(target):
    return dmc.AccordionControl(target)

def create_info_item(info):
    return dmc.AccordionPanel(dmc.Text(info, size="sm"))

info_card = dbc.Card (children = [
        dbc.CardHeader ('Chosen Target Information', className="w-100"),
        dbc.CardBody (children = [
            html.H6 ('Select a target to view their details.', id='info-desc', className="text-center"),
            dmc.Accordion(
                chevronPosition="right",
                variant="separated",
                children=[],
                id="info-accordion"
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

heatmap_card = dbc.Card (children = [
            dbc.CardHeader ('Correlation of the Goals based on the National Data', className="w-100"),
            dbc.CardBody (children = [
                html.H6 ('chika hir', className="text-center"),
                html.Img (src = dash.get_asset_url ('heatmap.png'),
                    style = {
                        'max-width' : '100%'
                        }
                    ),
            ])
        ], className="mt-3 flex justify-content-center align-items-center")

def create_linechart_card(target, chart):
    return dbc.Card (children = [
            dbc.CardHeader ('Line Chart of the indicators under ' + target, className="w-100"),
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
        html.H2("Region-Focused Tab"),
        control_card,
        dbc.Row (children =[
            dbc.Col (children = [
                choropleth_card,
                heatmap_card
            ], className="col-6 ps-0"),
            dbc.Col (children = [
                info_card,
                html.Div (children = [], id="linechart_div")
            ], className="col-6 pe-0")
        ], className="mx-0 w-100")
    ],
    className = 'p-5',
    style = {
        'background-image' : 'linear-gradient(to bottom,rgba(255, 255, 255, 1.0),rgba(255, 255, 255, 0)), url("/assets/bg3.jpg")',
        'background-size' : 'cover',
        'min-width' : '100vw'
})

@callback(Output("target-dropdown", "error"), Input("target-dropdown", "value"))
def select_value(value):
    return "Select at least one target." if len(value) < 1 else ""

# @callback(Output("heatmap", "figure"), Input("target-dropdown", "value"))
# def filter_heatmap():
#     fig = px.imshow(None)
#     return fig

@callback(Output("info-accordion", "children"), Input("target-dropdown", "value"))
def update_accordion(targets):
    children = []
    for target in targets:
        children.append(
            dmc.AccordionItem([
                        create_info_label(target),
                        create_info_item('chuchu'),
                ], value=target,
            )
        )
    
    return children

@callback(Output("info-desc", "children"), Input("target-dropdown", "value"))
def update_text(targets):
    return "Select a target to view their details." if len(targets) < 1 else ""

@callback(Output("linechart_div", "children"), Input("target-dropdown", "value"))
def update_div(targets):
    children = []
    for target in targets:
        children.append(
            create_linechart_card(target, '')
        )
    
    return children