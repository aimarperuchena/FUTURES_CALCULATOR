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
from layout_components import renderHeader
from input_test import test_input_data
from calc_functions import table_calc, min_max_calc
USERNAME_PASSWORD_PAIRS = [
    ['aimar', 'aimar']
]

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.COSMO, {
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}], meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
],)
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)


def Average(lst):
    return sum(lst) / len(lst)


form_layout = html.Div([
    dbc.Card(
        dbc.CardBody(dbc.Row([
            dbc.Col(dbc.FormGroup(
                [
                    dbc.Label("Balance", html_for="balance-input"),
                    dbc.Input(type="number", id="balance-input",
                              placeholder="Enter balance"),
                ]
            )),
            dbc.Col(dbc.FormGroup(
                [
                    dbc.Label("Unit Value", html_for="unit-input"),
                    dbc.Input(type="number", id="unit-input",
                              placeholder="Enter Unit Value"),
                ]
            )),
            dbc.Col(dbc.FormGroup(
                [
                    dbc.Label("Open Price", html_for="open-input"),
                    dbc.Input(type="number", id="open-input",
                              placeholder="Enter Open Price"),
                ]
            )),
            dbc.Col(dbc.FormGroup(
                [
                    dbc.Label("Percentage Change",
                              html_for="percentage-input"),
                    dbc.Input(type="number", id="percentage-input",
                              placeholder="Enter Percentage Change"),
                ]
            )),
            dbc.Col(dbc.FormGroup(
                [
                    dbc.Label("LONG/SHORT", html_for="long-short-input"),
                    dbc.RadioItems(
                        id="long-short-input",
                        options=[
                            {"label": "LONG", "value": 'LONG'},
                            {"label": "SHORT", "value": 'SHORT'},
                        ],
                    ),
                ]
            )),

        ])),
        className="m-3",
    ),

])

app_layout = html.Div([
    renderHeader(),
    form_layout,
    html.Div(id='price-table')
])


app.layout = app_layout


@app.callback(Output('price-table', 'children'),
              Input('balance-input', 'value'), Input('unit-input', 'value'), Input('open-input', 'value'), Input('long-short-input', 'value'), Input('percentage-input', 'value'))
def pnl_update(balance, unit, open, type, percentage):
    test_result = test_input_data(balance, unit, open, type, percentage)

    if test_result == True:
        data = table_calc(float(balance), float(
            unit), float(open), str(type), float(percentage))

        df = pd.DataFrame(
            {
                "Open Price": data,

            }
        )

        table = dbc.Table.from_dataframe(
            df, striped=True, bordered=True, hover=True,size='sm')
        min=data[0]
        max=data[len(data)-1]
        change=min_max_calc(type,min,max)
        render = dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(html.H1('TABLE PRICE'))
                ]),
                dbc.Row(dbc.Col(
                    html.H3('AVERAGE PRICE: '+str(round(Average(data),3)))
                )),
                dbc.Row(dbc.Col(
                    html.H3('PRICE VARIATION: '+str(round(change,2))+' %')
                )),
                dbc.Row(dbc.Col(
                   table 
                ))

            ]),
            className="m-3")
        return render


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
