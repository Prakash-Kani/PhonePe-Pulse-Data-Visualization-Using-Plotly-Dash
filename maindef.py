import numpy as np
import pandas as pd
import requests
import json
import mysql.connector
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, State, ctx


db = mysql.connector.connect(host = 'localhost',
                             user = 'root',
                             password = 'Prakashk14',
                             database = 'phonepe')
mycursor = db.cursor(buffered = True)

url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response = requests.get(url)
data1 = json.loads(response.content)
geo_state=[i['properties'].get('ST_NM') for i in data1['features']]
geo_state1=geo_state.sort(reverse=False)

def Number_Conversion(number):
    if number // 10**7:
        number = f'{round(number / 10**7,2)} Crores'
    elif number // 10**5:
        number = f'{round(number / 10**5,2)} Lakhs'
    elif number // 10**3:
        number = f'{round(number / 10**3,2)} K'
    elif number == 0:
        number ='Unavailable'
    return number



def Explore_Data_Page():
    page=[html.Div([
        html.Div([
            html.H2("PhonePe Pulse"),

            html.Label('Explore Data'),
            dcc.Dropdown(
            id="explore",
            options=[{"label": x, "value": x} for x in ['Transaction', 'User']],
            value='Transaction',
            clearable=False,
        ),
            html.Label('Select The year'),
            dcc.Dropdown(
            id="year",
            options=[{"label": x, "value": x} for x in [2018, 2019, 2020, 2021, 2022, 2023]],
            value=2018,
            clearable=False,
        ),

            html.Label('Select The quarter'),
            dcc.Dropdown(
            id="quarter",
            options=[{"label": i, "value": i} for i in range(1,5)],
            value=1,
            clearable=False,),

            html.Label('Select The type of transaction'),
            dcc.Dropdown(
            id="type",
            options=[{"label": x, "value": x} for x in ['Recharge & bill payments', 'Peer-to-peer payments','Merchant payments', 'Financial Services','Others']],
            value='Recharge & bill payments',
            clearable=False),
            html.Button("Show Details", id="Show", n_clicks=0),], style={'width': '15%', 'display': 'inline-block','backgroundColor':'#A66EEE'}),


        # Second Column (Figures and Charts)
        html.Div([
            html.H1(children = 'PhonePe Pulse Data Visualization and Exploration',style={'color':'#7F26F0','textAlign':'center'}),
            html.Hr(),
            html.H3("Figures and Charts", style={'textAlign':'center'}),
            # Add your figures and charts here
            dcc.Graph(id="bar-chart"),
            dcc.Graph(id="bar-chart1"),
            dcc.Graph(id='top-10-fig')
        ], style={'width': '60%', 'display': 'inline-block','backgroundColor':"#2F0350"}),
        
    
        html.Div([
            # html.H3("Transaction", style={'textAlign': 'center', 'color': 'blue', 'font-size': '50px','font-weight': 'bold', 'font-style': 'italic'}), 
            # # Add content related to statistical analysis here
            # html.Hr(),
            html.Div(id='statistical-analysis-content'),
            dcc.Markdown("#   "),
            html.Hr(),
            # html.P("This is where you can display statistical analysis results."),
            html.Div(children=[
                html.Button("State", id="State"),
                html.Button("Districts", id="District"),
                html.Button("Postal Code", id="Postal Code"),
            html.Div(id='top-10')

            ])#top 10

        ], style={'width': '25%', 'display': 'inline-block', 'backgroundColor':"#2F0350"}),


        ], style={'display': 'flex', 'flex-direction': 'row'})]

    return page