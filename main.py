import numpy as np
import pandas as pd
import requests
import json
import mysql.connector
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output, callback, State, ctx, MATCH
import maindef
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MYSQL Connection
mysql_host_name = os.getenv("MYSQL_HOST_NAME")
mysql_user_name = os.getenv("MYSQL_USER_NAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database_name = os.getenv("MYSQL_DATABASE_NAME")

db = mysql.connector.connect(host = mysql_host_name,
                             user = mysql_user_name,
                             password = mysql_password,
                             database = mysql_database_name)
mycursor = db.cursor(buffered = True)




app = Dash(__name__,
           title = 'PhonePe Pulse Data Visualization',
           suppress_callback_exceptions = True)

app.layout = html.Div([
    html.H1(children = 'PhonePe Pulse Data Visualization and Exploration', style={'color':'white','textAlign':'center'}),
    dcc.Tabs(id = "tabs", value = 'Explore Data', children = [
        dcc.Tab(label = 'Home', value = 'Home', style={'color': 'white', 'background-color': '#3C2E75'}),
        dcc.Tab(label = 'Explore Data', value = 'Explore Data', style={'color': 'white', 'background-color': '#3C2E75'}),
        dcc.Tab(label = 'Analysis', value = 'Analysis', style={'color': 'white', 'background-color': '#3C2E75'}),
    ], style={ 'textAlign':'center',  'color': 'blue', 'font-size': '35px', 'font-weight': 'bold', 'font-style': 'italic'}),
    html.Div(id = 'tabs-page')
], style = {'backgroundColor':'#3D2E65'})

@app.callback(Output('tabs-page', 'children'),
          Input('tabs', 'value'),
          prevent_initial_call = False,)

def render_content(tab):
    if tab == 'Explore Data':
        page = maindef.Explore_Data_Page()
        return page
    elif tab == 'Analysis':
        page = maindef.Analysis_Page()
        return page
    elif tab == 'Home':
        page = maindef.Home_Page()
        return page


@app.callback(
    [Output("bar-chart", "figure"), Output("bar-chart1", "figure"), Output('statistical-analysis-content', 'children'),
     Output('top-10', 'children'),Output('top-10-fig', 'figure')],
    [State("explore", "value"), State("year", "value"), State("quarter", "value"), State("type", "value")],
    [Input('Show','n_clicks'),Input("State", "n_clicks"),Input("District", "n_clicks"),Input("Postal Code", "n_clicks")],
    prevent_initial_call = False) 

def Update_Explore_Data(explore, year, quarter, transaction_type, button4, button1, button2, button3):

    # callback for Transactions
    button_clicked = ctx.triggered_id
    if explore == 'Transaction':
        # Output for "bar-chart"
        fig = maindef.transaction_fig1(year, quarter)
        # Output for "bar-chart1"
        fig1 = maindef.transaction_fig2(year, quarter, transaction_type)
        # Output for "statistical-analysis-content"
        statistical_content = maindef.transaction_stats(year, quarter) 
        if button_clicked == 'State':
            top = maindef.top10_transaction_state(year, quarter)
            # Output for "top-10-fig"
            bargraph1 = maindef.top10_transaction_state_fig(year, quarter)
        elif button_clicked == 'District':
            top = maindef.top10_transaction_district(year, quarter)
            bargraph1 = maindef.top10_transaction_district_fig(year, quarter)
        elif button_clicked == 'Postal Code':
            top = maindef.top10_transaction_pincode(year, quarter)
            bargraph1 =maindef.top10_transaction_pincode_fig(year, quarter) 
        else:  
            top = maindef.top10_transaction_state(year, quarter)
            bargraph1 = maindef.top10_transaction_state_fig(year, quarter)    
        return [fig, fig1, statistical_content, top, bargraph1]
    # callback for Users
    elif explore == 'User':
        # Output for "bar-chart"
        fig = maindef.user_fig1(year, quarter)
        # Output for "bar-chart1"
        fig1 = maindef.user_fig2(year, quarter)
        # Output for "statistical-analysis-content"
        statistical_content = maindef.user_stats(year, quarter)
        if button_clicked == 'State':
            top = maindef.top10_user_state(year, quarter)
            # Output for "top-10-fig"
            bargraph1 = maindef.top10_user_state_fig(year, quarter)
        elif button_clicked == 'District':
            top = maindef.top10_user_district(year, quarter)
            bargraph1 = maindef.top10_user_district_fig(year, quarter)
        elif button_clicked == 'Postal Code':
            top = maindef.top10_user_pincode(year, quarter)
            bargraph1 = maindef.top10_user_pincode_fig(year, quarter)
        else:
            top = maindef.top10_user_state(year, quarter)
            bargraph1 = maindef.top10_user_state_fig(year, quarter) 
        return [fig, fig1, statistical_content, top, bargraph1]
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    [Output("bar-chart2", "figure"), Output("bar-chart3", "figure")],
    [State("analysis", "value"), State("year1", "value"), State("quarter1", "value"), State("type1", "value")],
    Input('Show1','n_clicks'),
    prevent_initial_call = False)

def Update_Analysis(analysis, year, quarter, type, button):
    if analysis == 'Day':
        fig = maindef.Day_Analysis(year, quarter, type)
        barchart = maindef.Day_Analysis_barchart(year, quarter, type)
    elif analysis == 'Month':
        fig = maindef.Month_Analysis(year, quarter, type)
        barchart = maindef.Month_Analysis_barchart(year, quarter, type)
    return [fig, barchart]

@app.callback(Output('col1', 'children'),
          Input('col1','children'),
              prevent_initial_call = False,)

def Update_Home(col):
    return maindef.Update_Home_Page()

if __name__ == '__main__':
    app.run(debug = True, port = 8060)