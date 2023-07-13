import pandas as pd
from dash import html, dcc, Dash, Input, Output, State, callback, register_page
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

register_page (
    __name__, 
    name = 'Region-focused Tab',
    path = '/region-focused-tab'
)