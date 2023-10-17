import numpy as np
import pandas as pd
import requests
import json
import mysql.connector
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, State, ctx
import maindef


db = mysql.connector.connect(host = 'localhost',
                             user = 'root',
                             password = 'Prakashk14',
                             database = 'phonepe')
mycursor = db.cursor(buffered = True)

def Number_Conversion(number):
    if number // 10**7:
        number = f'{round(number / 10**7,2)} Crores'
    elif number // 10**5:
        number = f'{round(number / 10**5,2)} Lakhs'
    elif number // 10**3:
        number = f'{round(number / 10**3,2)} K'
    return number
def get_state():
    mycursor.execute("""SELECT Distinct(State) FROM aggeregated_user;""")
    data12=mycursor.fetchall()
    return data12

url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response = requests.get(url)
data1 = json.loads(response.content)
geo_state=[i['properties'].get('ST_NM') for i in data1['features']]
geo_state1=geo_state.sort(reverse=False)

app = Dash(__name__,
           title= 'PhonePe Pulse Data Visualization',
           suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1(children = 'PhonePe Pulse Data Visualization and Exploration',style={'color':'#7F26F0','textAlign':'center'}),
    dcc.Tabs(id="tabs-example-graph", value='Explore Data', children=[
        dcc.Tab(label='Home', value='Home'),
        dcc.Tab(label='Explore Data', value='Explore Data'),
        dcc.Tab(label='Analysis', value='Analysis'),
    ]),
    html.Div(id='tabs-content-example-graph')
])


if __name__ == '__main__':
    app.run(debug=True)