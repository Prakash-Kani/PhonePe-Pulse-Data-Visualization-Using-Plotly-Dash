import numpy as np
import pandas as pd
import requests
import json
import mysql.connector
import plotly.express as px
import dash
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
 

url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response = requests.get(url)
data1 = json.loads(response.content)
geo_state = [i['properties'].get('ST_NM') for i in data1['features']]
geo_state1 = geo_state.sort(reverse=False)

app = Dash(__name__,
           title = 'PhonePe Pulse Data Visualization',
           suppress_callback_exceptions = True)

app.layout = html.Div([
    html.H1(children = 'PhonePe Pulse Data Visualization and Exploration',style={'color':'#7F26F0','textAlign':'center'}),
    dcc.Tabs(id = "tabs", value = 'Explore Data', children = [
        dcc.Tab(label = 'Home', value = 'Home'),
        dcc.Tab(label = 'Explore Data', value = 'Explore Data'),
        dcc.Tab(label = 'Analysis', value = 'Analysis'),
    ]),
    html.Div(id = 'tabs-page')
])

@callback(Output('tabs-page', 'children'),
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

@callback(Output('col1', 'children'),
          Input('col1','children'),
              prevent_initial_call = False,)

def Update_Home(col):
    return maindef.Update_Home_Page()

if __name__ == '__main__':
    app.run(debug=True, port = 8050)