import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pymysql.cursors
import dash_auth

def renderHeader():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(
                "BINANCE FUTURES  CALCULATOR", href="#")),
        ],
        brand="BINANCE FUTURES CALCULATOR",
        brand_href="#",
        color="primary",
        dark=True,
    )