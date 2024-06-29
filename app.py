# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 13:35:24 2021

@author: User
"""
import dash
from dash import Dash, dcc, html, Input, Output,callback,State
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
import pgeocode

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

Restaurant = pd.read_excel('restaurant.xlsx')

rest_name = Restaurant['NAME'].to_list()


navbar = dbc.Navbar(
                    [
                            # Use row and col to control vertical alignment of logo / brand
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src='/static/images/pngegg.png', height="40px",width = "120px")),
                                    dbc.Col(dbc.NavbarBrand("Food Wastage Management",className = "ml-2")),
                                ],
                                align="center",
                                className="g-0",
                            ),
                    ],
                    color="dark",
                    dark=True,
                    sticky = "top")


layout = html.Div([ navbar,
                    html.Br(),
                    html.Br(),
                    html.Div([                                    
                            html.Div([
                                    html.Label('Select the Restaurant',htmlFor = 'restaurant'),
                                    html.Div(
                                    dcc.Dropdown(id = 'restaurant',
                                                 options = rest_name ,value = 'de Paradise'),className = 'dropdown'
                            )
                                    ],className = 'col-3 firstelement'),
                            html.Div([
                                    dbc.Col(html.Label('Address of Restaurant ',htmlFor = 'address')),
                                    dbc.Col(children = dcc.Input(id = 'address', type = 'text',className = 'col-8')),                                           
                                    ],className = 'col-8 firstelement'),
                            ],className = 'row'),
                    html.Br(),
                    html.Br(),
                    html.Div([
                             html.Div([
                                    dbc.Col(html.Label('Zip Code',htmlFor = 'zip_code')),
                                    dbc.Col(dcc.Input(id = 'zip_code', type = 'text')), 
                                    ],className = 'col-3 firstelement'),                                                       
                            html.Div([
                                    html.Label('Food Surplus (in Kg)',htmlFor = 'food_surplus'),
                                    dcc.Input(id = 'food_surplus', type = 'number')  
                                    ],className = 'col-2 firstelement'),

                            ],className = 'row'),
                    html.Br(),
                    html.Div(                           
                    html.Button(id='submit-val',children='Submit',n_clicks=0),className = 'firstelement'),        
                    html.Div([                    
                            html.Br(),
                            html.Div(id = 'testing',className = 'datatable')
                            ])
                    
                ])



app.layout = layout

@callback(
    Output('address', 'value'),
    Output('zip_code', 'value'),
    Output('food_surplus', 'value'),
    Input('restaurant', 'value')
)
def update_info(value):
    if value is None:
        raise PreventUpdate
    else:
        df = Restaurant[Restaurant['NAME'] == value]
        address = df['ADDRESS'].values[0]
        pin_code = str(df['PIN CODE'].values[0])
        food_surplus = df['Food Surplus'].values[0]
        return address,pin_code,food_surplus

@callback(
    Output('testing', 'children'),
    State('zip_code', 'value'),
    Input('submit-val', 'n_clicks')
)
def get_food_bank(value,n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    elif value is None:
        raise PreventUpdate    
    else:
        food_bank = pd.read_excel('FOODBANK.xlsx')        
        zip_code = food_bank['Zip Code'].astype(str).to_list()        
        dist = pgeocode.GeoDistance('in')
        zip_list = [str(value)]*len(food_bank)
        food_bank['Distance in (KM)'] = dist.query_postal_code(zip_list, zip_code)
        food_bank['Distance in (KM)'] = food_bank['Distance in (KM)'].apply(lambda x: round(x, 2))
        sort_data = food_bank.sort_values(by=['Distance in (KM)']).head(10)
        
        return dash_table.DataTable(sort_data.to_dict('records'), [{"name": i, "id": i} for i in sort_data.columns])


if __name__ == "__main__":
    app.run_server()