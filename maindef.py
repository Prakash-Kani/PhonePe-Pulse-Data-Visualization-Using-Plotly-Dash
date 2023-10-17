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

# ---------------------------------------------------/          Page Design        /---------------------------------------------------------

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

def Analysis_Page():
    page=[html.Div([
        html.Div([
            html.H2("PhonePe Pulse"),

            html.Label('Select The Type of Analysis'),
            dcc.Dropdown(
            id="analysis",
            options=[{"label": x, "value": x} for x in ['Day', 'Month']],
            value='Month',
            clearable=False,
        ),
            html.Label('Select The year'),
            dcc.Dropdown(
            id="year1",
            options=[{"label": x, "value": x} for x in [2018, 2019, 2020, 2021, 2022, 2023]],
            value=2018,
            clearable=False,
        ),

            html.Label('Select The quarter'),
            dcc.Dropdown(
            id="quarter1",
            options=[{"label": i, "value": i} for i in range(1,5)],
            value=1,
            clearable=False,),

            html.Label('Select The type of transaction'),
            dcc.Dropdown(
            id="type1",
            options=[{"label": x, "value": x} for x in ['Recharge & bill payments', 'Peer-to-peer payments','Merchant payments', 'Financial Services','Others']],
            value='Recharge & bill payments',
            clearable=False),
            html.Button("Show Details", id="Show1", n_clicks=0),], style={'width': '20%', 'display': 'inline-block','backgroundColor':'#A66EEE'}),

        html.Div([
            html.H1(children = 'PhonePe Pulse Data Visualization and Exploration',style={'color':'#7F26F0','textAlign':'center'}),
            html.Hr(),
            html.H3("Figures and Charts", style={'textAlign':'center'}),
            # Add your figures and charts here
            dcc.Graph(id="bar-chart2"),
            dcc.Graph(id="bar-chart3"),
        ], style={'width': '80%', 'display': 'inline-block','backgroundColor':"#2F0350"}),

        ], style={'display': 'flex', 'flex-direction': 'row'})]

    return page


def Home_Page():
    page=[ html.Div([
        html.Div(id='col1', style={'width': '70%', 'display': 'inline-block', 'backgroundColor':"Teal"}),
        html.Div(id='col2',children= 'adfjasdkjfa', style={'width': '30%', 'display': 'inline-block', 'backgroundColor':"#2F0350"}),
        ], style={'display': 'flex', 'flex-direction': 'row'})]
    return page

# ---------------------------------------------------/      Explore Data Callback Functions       /---------------------------------------------------------



def transaction_fig1(year, quarter):
    mycursor.execute(f"""SELECT g.State, g.Total_Transaction_Count, g.Total_Transaction_Amount,
                            round((g.Total_Transaction_Amount / g.Total_Transaction_Count),2) as Average_Transaction_Amount
                        FROM (
                            SELECT State, 
                                SUM(Transaction_Count) as Total_Transaction_Count, 
                                SUM(Transaction_Amount) as Total_Transaction_Amount
                            FROM map_transaction  
                            WHERE Year = {year} AND Quarter = {quarter}
                            GROUP BY State
                        ) as g;""")
    data4 = mycursor.fetchall()

    dff = pd.DataFrame(data4, columns=[i[0] for i in mycursor.description])
    dff['State'] = geo_state

    fig = px.choropleth(
        dff,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Total_Transaction_Amount',
        hover_name='State',
        custom_data=['Total_Transaction_Count', 'Total_Transaction_Amount', 'Average_Transaction_Amount'],
        color_continuous_scale='purples')

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Transaction Count = %{customdata[0]}<br>Transaction Amount = %{customdata[1]}<br>Average Transaction Amount = %{customdata[2]}')
    fig.update_layout(
            plot_bgcolor='#10CD04 ',
            paper_bgcolor="#3D2E61",
            font_color='#087FA5',
            font_size=12
    ),
    return fig

def transaction_fig2(year, quarter,transaction_type):
    mycursor.execute(f"""select State, Transaction_Count, Transaction_Type, Transaction_Amount, (Transaction_Amount/Transaction_Count) as Average_Amount
                        from aggregated_transaction 
                        where year={year} and quarter={quarter} and Transaction_Type = '{transaction_type}';""")
    data5 = mycursor.fetchall()
    dff1 = pd.DataFrame(data5, columns=[i[0] for i in mycursor.description])
    dff1['State'] = geo_state

    fig1 = px.choropleth(
        dff1,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_Amount',
        hover_name='State',
        custom_data=['Transaction_Type', 'Transaction_Count', 'Transaction_Amount', 'Average_Amount'],
        color_continuous_scale='rainbow')

    fig1.update_geos(fitbounds="locations", visible=False)
    fig1.update_traces(hovertemplate='<b>%{hovertext}</b><br>Transaction Type = %{customdata[0]}<br>Transaction Count = %{customdata[1]}<br>Transaction Amount = %{customdata[2]}<br>Average Amount = %{customdata[3]}')
    fig1.update_layout(
            plot_bgcolor='#10CD04 ',
            paper_bgcolor="#3D2E65",
            font_color='#0087FF',
            font_size=12
    ),
    return fig1

def transaction_stats(year, quarter):
    mycursor.execute(f"""SELECT g.Transaction_Type, g.Total_Amount, g.Total_Count,  round((g.Total_Amount / g.Total_Count),2) as Average_Transaction
                                FROM (SELECT Transaction_Type, sum(Transaction_Amount)as Total_Amount, sum(Transaction_Count) as Total_Count FROM aggregated_transaction 
                                WHERE Year = {year} AND Quarter = {quarter} GROUP BY Transaction_Type) as g;""")
    data = mycursor.fetchall()
    df1 = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    totalcount = df1['Total_Count'].sum()
    totalamount = df1['Total_Amount'].sum()
    average = df1['Average_Transaction'].mean()

    categories = ([dcc.Markdown(f"#### {i+1}. {df1['Transaction_Type'].iloc[i]} <=>  {Number_Conversion(df1['Total_Amount'].iloc[i])}", style={'color': '#4090F5'}) for i in range(5)])

    statistical_content = [
        html.H3("Transaction", style={'textAlign': 'center', 'color': 'blue', 'font-size': '50px','font-weight': 'bold', 'font-style': 'italic'}), 
        html.Hr(),
        dcc.Markdown('# ***All PhonePe transactions (UPI + Cards + Wallets***)', style={'color': '#FAFAFA'}),
        dcc.Markdown(f"# {totalcount}", style={'color': '#4090F5'}),
        dcc.Markdown('# ***Total payment value***', style={'color': '#FAFAFA'}),
        dcc.Markdown(f'# {Number_Conversion(totalamount)}', style={'color': '#4090F5'}),
        dcc.Markdown('# ***Avg. transaction value***', style={'color': '#FAFAFA'}),
        dcc.Markdown(f'# {round(average)}', style={'color': '#4090F5'}),
        html.Hr(),
        dcc.Markdown('# ***Categories***', style={'color': '#FAFAFA'}),
        ]
    statistical_content.extend(categories)

    return statistical_content


def top10_transaction_state(year, quarter):
    mycursor.execute(f"""SELECT State, Total_Transaction_Count FROM top_transaction_state
                                    WHERE Year = {year} AND Quarter = {quarter}
                                ORDER BY Total_Transaction_Count desc limit 10;""")
    data1 = mycursor.fetchall()
    df2=pd.DataFrame(data1, columns = [i[0] for i in mycursor.description])
    # for i in range(df2.shape[0]):
    details=[dcc.Markdown(f"""### {i + 1}.  {df2['State'].iloc[i].upper()} <=> {Number_Conversion(df2['Total_Transaction_Count'].iloc[i])}""", style={'color': '#4090F5'}) for i in range(df2.shape[0])]
    top=[
    html.H1(f'Top 10 State Transaction Analysis', style={'color': '#FAFAFA'}),]
    top.extend(details)
    return top


def top10_transaction_district(year, quarter):
    mycursor.execute(f"""SELECT top.District, top.Total_Transaction_Count
                        FROM (
                            SELECT District, SUM(Transaction_Count) as Total_Transaction_Count
                            FROM top_transaction_district
                            WHERE Year = {year} AND Quarter = {quarter}
                            GROUP BY District
                        ) as top
                        ORDER BY top.Total_Transaction_Count desc limit 10;""")
    data2 = mycursor.fetchall()
    df3=pd.DataFrame(data2, columns = [i[0] for i in mycursor.description])
    details=[dcc.Markdown(f"""### {i + 1}.  {df3['District'].iloc[i].upper()} <=> {Number_Conversion(df3['Total_Transaction_Count'].iloc[i])}""", style={'color': '#4090F5'}) for i in range(df3.shape[0])]

    top=[
    html.H1(f'Top 10 District Transaction Analysis', style={'color': '#FAFAFA'}),]
    top.extend(details)
    return top

def top10_transaction_pincode(year, quarter):
    mycursor.execute(f"""SELECT Pincode, Transaction_Count
                        FROM top_transaction_pincode
                        WHERE Year = {year} AND Quarter = {quarter}
                        ORDER BY Transaction_Count DESC LIMIT 10;""")
    data3 = mycursor.fetchall()
    df4=pd.DataFrame(data3, columns = [i[0] for i in mycursor.description])
    details=[dcc.Markdown(f"""### {i + 1}.  {df4['Pincode'].iloc[i]} <=> {Number_Conversion(df4['Transaction_Count'].iloc[i])}""", style={'color': '#4090F5'}) for i in range(df4.shape[0])]
    top=[
    html.H1(f'Top 10 Postal Code Transaction Analysis', style={'color': '#FAFAFA'}),]
    top.extend(details)
    return top

def top10_transaction_state_fig(year, quarter):
    mycursor.execute(f"""SELECT State, Total_Transaction_Count FROM top_transaction_state
                                    WHERE Year = {year} AND Quarter = {quarter}
                                ORDER BY Total_Transaction_Count desc limit 10;""")
    data1 = mycursor.fetchall()
    df2=pd.DataFrame(data1, columns = [i[0] for i in mycursor.description])
    bargraph1 = px.bar(df2, x ='State', y = 'Total_Transaction_Count', text = 'Total_Transaction_Count', color='Total_Transaction_Count',
                color_continuous_scale = 'thermal', title = 'Top 10 State Transaction Analysis Chart', height = 600)
    bargraph1.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
    bargraph1.update_layout(
            plot_bgcolor='#B0CAE1',
            paper_bgcolor="#3D2E70",
            font_color='#0087FF',
            font_size=12
    ),
    return bargraph1

def top10_transaction_district_fig(year, quarter):
    mycursor.execute(f"""SELECT top.District, top.Total_Transaction_Count
                        FROM (
                            SELECT District, SUM(Transaction_Count) as Total_Transaction_Count
                            FROM top_transaction_district
                            WHERE Year = {year} AND Quarter = {quarter}
                            GROUP BY District
                        ) as top
                        ORDER BY top.Total_Transaction_Count desc limit 10;""")
    data2 = mycursor.fetchall()
    df3=pd.DataFrame(data2, columns = [i[0] for i in mycursor.description])
    df3['Total_Transaction_Count'] = df3['Total_Transaction_Count'].astype(int)
    bargraph1 = px.bar(df3, x ='District', y = 'Total_Transaction_Count', text = 'Total_Transaction_Count', color='Total_Transaction_Count',
                color_continuous_scale = 'Teal', title = 'Top 10 District Transaction Analysis Chart', height = 600)
    bargraph1.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
    bargraph1.update_layout(
            plot_bgcolor='#B0CAE1',
            paper_bgcolor="#3D2E70",
            font_color='#0087FF',
            font_size=12
    ),
    return bargraph1

def top10_transaction_pincode_fig(year, quarter):
    mycursor.execute(f"""SELECT Pincode, Transaction_Count
                    FROM top_transaction_pincode
                    WHERE Year = {year} AND Quarter = {quarter}
                    ORDER BY Transaction_Count DESC LIMIT 10;""")
    data3 = mycursor.fetchall()
    df4=pd.DataFrame(data3, columns = [i[0] for i in mycursor.description])
    newdf=df4
    newdf['Pincode'] = newdf['Pincode'].astype(str)
    bargraph1 = px.bar(newdf, x ='Pincode', y = 'Transaction_Count', text = 'Transaction_Count', color='Transaction_Count',
                color_continuous_scale = 'thermal', title = 'Top 10 Postal Code Transaction Analysis Chart', height = 600)
    bargraph1.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
    bargraph1.update_layout(
            plot_bgcolor='#B0CAE1',
            paper_bgcolor="#3D2E70",
            font_color='#0087FF',
            font_size=12
    ),
    return bargraph1

#-----------------------------------------------/    User    /-----------------------------------------

def user_fig1(year, quarter):
    mycursor.execute(f"""SELECT State, sum(Registered_User) as Registered_PhonePe_Users, sum(App_Opens) as PhonePe_App_Opens FROM map_user 
                        WHERE Year = {year} AND Quarter = {quarter} GROUP BY State ORDER BY State;""")
    data6 = mycursor.fetchall()

    dff3 = pd.DataFrame(data6, columns = [i[0] for i in mycursor.description])

    dff3['State']=geo_state
    dff3['Registered_PhonePe_Users'] = dff3['Registered_PhonePe_Users'].astype(int)

    fig = px.choropleth(
        dff3,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Registered_PhonePe_Users',
        hover_name='State',
        custom_data=['Registered_PhonePe_Users', 'PhonePe_App_Opens'],
        color_continuous_scale='YlGnBu')

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Registered PhonePe User = %{customdata[0]}<br>PhonePe App Opens = %{customdata[1]}')
    fig.update_layout(
            plot_bgcolor='#10CD04 ',
            paper_bgcolor="#3D2E61",
            font_color='#087FA5',
            font_size=12
    ),
    return fig


def user_fig2(year, quarter):
    mycursor.execute(f"""SELECT State, SUM(User_Count) AS User_Count FROM aggregated_user 
                    WHERE Year = {year} AND Quarter = {quarter} GROUP BY State;""")
    data10 = mycursor.fetchall()

    dff4 = pd.DataFrame(data10, columns = [i[0] for i in mycursor.description])

    dff4['State']=geo_state
    if year < 2022:
        dff4['User_Count'] = dff4['User_Count'].astype(int)
    if year == 2022 and quarter==1:
        dff4['User_Count'] = dff4['User_Count'].astype(int)

    fig1 = px.choropleth(
        dff4,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='User_Count',
        hover_name='State',
        custom_data='User_Count',
        color_continuous_scale='earth')

    fig1.update_geos(fitbounds="locations", visible=False)
    fig1.update_traces(hovertemplate='<b>%{hovertext}</b><br>User_Count = %{customdata[0]}')
    fig1.update_layout(
            plot_bgcolor='#10CD04 ',
            paper_bgcolor="#3D2E65",
            font_color='#0087FF',
            font_size=12
    ),
    return fig1

def user_stats(year, quarter):
# column 3
    mycursor.execute(f"""SELECT State, sum(Registered_User) as Registered_PhonePe_Users, sum(App_Opens) as PhonePe_App_Opens FROM map_user 
                                WHERE Year = {year} AND Quarter = {quarter} GROUP BY State ORDER BY State;""")
    data1 = mycursor.fetchall()
    df5=pd.DataFrame(data1, columns = [i[0] for i in mycursor.description])
    registeredcount=df5['Registered_PhonePe_Users'].sum()
    appopens=df5['PhonePe_App_Opens'].sum()
    mycursor.execute(f"""SELECT g.Brand, g.Total_User_Count, g.User_Precentage
                        FROM (SELECT Brand, sum(User_Count)as Total_User_Count, sum(Percentage) as User_Precentage FROM aggregated_user 
                        WHERE Year = {year} AND Quarter = {quarter} GROUP BY Brand) as g
                        ORDER BY Total_User_Count DESC LIMIT 12;""")
    data2 = mycursor.fetchall()
    brand=pd.DataFrame(data2, columns = [i[0] for i in mycursor.description])
    brand_analysis = ([dcc.Markdown(f"### {i+1}. {brand['Brand'].iloc[i]} <=> {Number_Conversion(brand['Total_User_Count'].iloc[i])}", style={'color': '#4090F5'}) for i in range(brand.shape[0])])

    statistical_content=[
    html.H3("User", style={'textAlign': 'center', 'color': 'blue', 'font-size': '50px','font-weight': 'bold', 'font-style': 'italic'}), 
    html.Hr(),
    dcc.Markdown(f'# ***Registered PhonePe users till {quarter} {year}***',style={'color': '#FAFAFA'}),
    dcc.Markdown(f'# {registeredcount}',style= {'color':'#4090F5'}),
    dcc.Markdown(f'# ***PhonePe app opens in {quarter} {year}***',style={'color': '#FAFAFA'}),
    dcc.Markdown(f'# {Number_Conversion(appopens)}',style= {'color':'#4090F5'}),
    html.Hr(),
    dcc.Markdown('# ***Brand Analysis***',style= {'color':'#FAFAFA'}),
    ]
    statistical_content.extend(brand_analysis)
    return  statistical_content


def top10_user_state(year, quarter):
    mycursor.execute(f"""SELECT State, Total_Registered_Users FROM top_user_state 
                        WHERE Year = {year} AND Quarter = {quarter} ORDER BY Total_Registered_Users DESC LIMIT 10;""")
    data8 = mycursor.fetchall()
    df6 = pd.DataFrame(data8, columns = [i[0] for i in mycursor.description])
    details=[dcc.Markdown(f"""### {i + 1}.  {df6['State'].iloc[i].upper()} <=> {Number_Conversion(df6['Total_Registered_Users'].iloc[i])}""",style={'color': '#4090F5'}) for i in range(df6.shape[0])]
    # details = [
    # html.Div([
    #     html.Span(f"{i + 1}. {df6['State'].iloc[i].upper()}  <=> ", style={'color': 'white'}),
    #     html.Span(Number_Conversion(df6['Total_Registered_Users'].iloc[i]), style={'color': 'blue'})
    # ])
    # for i in range(df6.shape[0])]
    top=[dcc.Markdown('#  ***Top 10 State User Analysis***', style={'color': 'white'})]
    top.extend(details)
    
    return top

def top10_user_district(year, quarter):
    mycursor.execute(f"""SELECT District, sum(Registered_User) as Registered_User FROM top_user_district 
                        WHERE Year = {year} AND Quarter = {quarter} GROUP BY District ORDER BY Registered_User DESC LIMIT 10;""")
    data9 = mycursor.fetchall()

    df7 = pd.DataFrame(data9, columns = [i[0] for i in mycursor.description])
    details=[dcc.Markdown(f"""### {i + 1}.  {df7['District'].iloc[i].upper()} <=> {Number_Conversion(df7['Registered_User'].iloc[i])}""",style={'color': '#4090F5'}) for i in range(df7.shape[0])]
    top=[dcc.Markdown('#  ***Top 10 District User Analysis***', style={'color': 'white'})]
    top.extend(details)  

    return top

def top10_user_pincode(year, quarter):
    mycursor.execute(f"""SELECT Pincode, Registered_User FROM top_user_pincode 
                        WHERE Year = {year} AND Quarter = {quarter} ORDER BY Registered_User DESC LIMIT 10;""")
    data10 = mycursor.fetchall()

    df8 = pd.DataFrame(data10, columns = [i[0] for i in mycursor.description])
    details=[dcc.Markdown(f"""## {i + 1}.  {df8['Pincode'].iloc[i]} <=> {Number_Conversion(df8['Registered_User'].iloc[i])}""",style={'color': '#4090F5'}) for i in range(df8.shape[0])]
    top=[dcc.Markdown('#  ***Top 10 Postal Code User Analysis***', style={'color': 'white'})]
    top.extend(details)

    return top


def top10_user_state_fig(year, quarter):
    mycursor.execute(f"""SELECT State, Total_Registered_Users FROM top_user_state 
                        WHERE Year = {year} AND Quarter = {quarter} ORDER BY Total_Registered_Users ASC LIMIT 10;""")
    data8 = mycursor.fetchall()
    df6 = pd.DataFrame(data8, columns = [i[0] for i in mycursor.description])
    bargraph1 = px.bar(df6, x = 'Total_Registered_Users', y ='State', text = 'Total_Registered_Users', color='Total_Registered_Users',
                        orientation='h', color_continuous_scale = 'thermal', title = 'Top 10 State Registered User Analysis Chart', height = 600)
    bargraph1.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
    bargraph1.update_layout(
            plot_bgcolor='#B0CAE1',
            paper_bgcolor="#3D2E70",
            font_color='#0087FF',
            font_size=12
    ),
    return bargraph1

def top10_user_district_fig(year, quarter):
    mycursor.execute(f"""SELECT District, sum(Registered_User) as Registered_User FROM top_user_district 
                        WHERE Year = {year} AND Quarter = {quarter} GROUP BY District ORDER BY Registered_User ASC LIMIT 10;""")
    data9 = mycursor.fetchall()

    df7 = pd.DataFrame(data9, columns = [i[0] for i in mycursor.description])
    df7['Registered_User'] = df7['Registered_User'].astype(int)
    bargraph1 = px.bar(df7, x = 'Registered_User', y ='District', text = 'Registered_User', color='Registered_User', orientation='h',
                color_continuous_scale = 'Teal', title = 'Top 10 District Registered User Analysis Chart', height = 600)
    bargraph1.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
    bargraph1.update_layout(
            plot_bgcolor='#B0CAE1',
            paper_bgcolor="#3D2E70",
            font_color='#0087FF',
            font_size=12
    ),
    return bargraph1

def top10_user_pincode_fig(year, quarter):
    mycursor.execute(f"""SELECT Pincode, Registered_User FROM top_user_pincode 
                        WHERE Year = {year} AND Quarter = {quarter} ORDER BY Registered_User ASC LIMIT 10;""")
    data10 = mycursor.fetchall()

    df8 = pd.DataFrame(data10, columns = [i[0] for i in mycursor.description])
    # newdf=df8
    # newdf['Pincode'] = newdf['Pincode'].astype(str)
    bargraph1 = px.bar(df8, x = 'Registered_User', y ='Pincode',  text = 'Registered_User', color='Registered_User', orientation='h',
                color_continuous_scale = 'thermal', title = 'Top 10 Postal Code Registered User Analysis Chart', height = 600)
    bargraph1.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
    bargraph1.update_layout(
            plot_bgcolor='#B0CAE1',
            paper_bgcolor="#3D2E70",
            font_color='#0087FF',
            font_size=12
    ),
    return bargraph1



def Day_Analysis(year, quarter, type):
    mycursor.execute(f"""SELECT State, Year, Transaction_Type, SUM(Transaction_Count / 91.25) AS Day_Transaction_Count, SUM(Transaction_Amount / 91.25) AS Day_Transaction_Amount
                        FROM aggregated_transaction WHERE Quarter = {quarter} and year = {year} and Transaction_Type = '{type}'
                        GROUP BY State, Year, Transaction_Type ORDER BY Year, State;""")
    data6 = mycursor.fetchall()

    dff3 = pd.DataFrame(data6, columns = [i[0] for i in mycursor.description])

    dff3['State']=geo_state
    dff3['Day_Transaction_Amount'] = dff3['Day_Transaction_Amount'].astype(int)

    fig = px.choropleth(
        dff3,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Day_Transaction_Amount',
        hover_name='State',
        custom_data=['Day_Transaction_Count', 'Day_Transaction_Amount'],
        color_continuous_scale='Teal')

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Transaction Count Per Day = %{customdata[0]}<br>Transaction Amount Per Day = %{customdata[1]}')
    fig.update_layout(
            plot_bgcolor='#10CD04 ',
            paper_bgcolor="#3D2E61",
            font_color='#087FA5',
            font_size=12
    ),
    return fig

def Month_Analysis(year, quarter, type):
    mycursor.execute(f"""SELECT State, Year, Transaction_Type, SUM(Transaction_Count / 3) AS Month_Transaction_Count, SUM(Transaction_Amount / 3) AS Month_Transaction_Amount
                        FROM aggregated_transaction WHERE Quarter = {quarter} and year = {year} and Transaction_Type = '{type}'
                        GROUP BY State, Year, Transaction_Type ORDER BY Year, State;""")
    data6 = mycursor.fetchall()

    dff3 = pd.DataFrame(data6, columns = [i[0] for i in mycursor.description])

    dff3['State']=geo_state
    dff3['Month_Transaction_Amount'] = dff3['Month_Transaction_Amount'].astype(int)

    fig = px.choropleth(
        dff3,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Month_Transaction_Amount',
        hover_name='State',
        custom_data=['Month_Transaction_Count', 'Month_Transaction_Amount'],
        color_continuous_scale='thermal')

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>Transaction Count Per Month = %{customdata[0]}<br>Transaction Amount Per Month = %{customdata[1]}')
    fig.update_layout(
            plot_bgcolor='#10CD04 ',
            paper_bgcolor="#3D2E61",
            font_color='#087FA5',
            font_size=12
    ),
    return fig

# def Month_Analysis_fig(year, quarter, type):
#     mycursor.execute(f"""SELECT State, Year, Transaction_Type, SUM(Transaction_Count / 3) AS Month_Transaction_Count, SUM(Transaction_Amount / 3) AS Month_Transaction_Amount
#                         FROM aggregated_transaction WHERE Quarter = {quarter} and year = {year} and Transaction_Type = '{type}'
#                         GROUP BY State, Year, Transaction_Type ORDER BY Year, State;""")
#     data = mycursor.fetchall()

#     dff = pd.DataFrame(data, columns = [i[0] for i in mycursor.description])
#     fig_sunburst = px.sunburst(
#     dff,
#     path=["State", "Month_Transaction_Count"],
#     values="Month_Transaction_Amount",
#     hover_data="Month_Transaction_Amount",
#     color="Month_Transaction_Count",
#     color_continuous_scale="RdBu",
#         )
#     fig_sunburst.update_layout(title_text="Sunburst Chart for")
#     return fig_sunburst


def Month_Analysis_barchart(year, quarter, type):
    mycursor.execute(f"""SELECT State, Year, Transaction_Type, SUM(Transaction_Count / 3) AS Month_Transaction_Count, SUM(Transaction_Amount / 3) AS Month_Transaction_Amount
                        FROM aggregated_transaction WHERE Quarter = {quarter} and year = {year} and Transaction_Type = '{type}'
                        GROUP BY State, Year, Transaction_Type ORDER BY Year, State;""")
    data6 = mycursor.fetchall()

    dff3 = pd.DataFrame(data6, columns = [i[0] for i in mycursor.description])
    dff3["Month_Transaction_Count"] = dff3["Month_Transaction_Count"].astype(int)
    bargraph1 = px.bar(dff3, x ='State', y = 'Month_Transaction_Count', text = 'Month_Transaction_Count', color='Month_Transaction_Count',
                color_continuous_scale = 'Teal', title = 'Top 10 State Transaction Analysis Chart', height = 900)
    bargraph1.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
    bargraph1.update_layout(
            plot_bgcolor='#B0CAE1',
            paper_bgcolor="#3D2E70",
            font_color='#0087FF',
            font_size=12
    ),
    return bargraph1

def Day_Analysis_barchart(year, quarter, type):
    mycursor.execute(f"""SELECT State, Year, Transaction_Type, SUM(Transaction_Count / 91.25) AS Day_Transaction_Count, SUM(Transaction_Amount / 91.25) AS Day_Transaction_Amount
                        FROM aggregated_transaction WHERE Quarter = {quarter} and year = {year} and Transaction_Type = '{type}'
                        GROUP BY State, Year, Transaction_Type ORDER BY Year, State;""")
    data6 = mycursor.fetchall()

    dff3 = pd.DataFrame(data6, columns = [i[0] for i in mycursor.description])
    dff3["Day_Transaction_Count"] = dff3["Day_Transaction_Count"].astype(int)
    bargraph1 = px.bar(dff3, x ='State', y = 'Day_Transaction_Count', text = 'Day_Transaction_Count', color='Day_Transaction_Count',
                color_continuous_scale = 'Teal', title = 'Top 10 State Transaction Analysis Chart', height = 900)
    bargraph1.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
    bargraph1.update_layout(
            plot_bgcolor='#B0CAE1',
            paper_bgcolor="#3D2E70",
            font_color='#0087FF',
            font_size=12
    ),
    return bargraph1


def Update_Home_Page():
    content=[
        html.H1("Welcome To PhonePe Pulse Data Extraction"),
        dcc.Markdown(""" In this app, we explore and analyze data from PhonePe Pulse, a powerful data visualization and analytics 
                        platform provided by PhonePe, a leading digital payment service in India. PhonePe Pulse offers comprehensive 
                        insights into digital payment trends, transaction data, user behaviors, and more. This project aims to provide a 
                        brief overview of the capabilities and features of PhonePe Pulse data visualization."""),
        dcc.Markdown("## Introduction to PhonePe Pulse"),
        dcc.Markdown(""" **PhonePe Pulse** is a feature-rich dashboard and data visualization tool that enables businesses and users to gain a deeper 
                     understanding of digital payment trends, transaction data, and consumer behaviors. With PhonePe Pulse, you can unlock valuable 
                     insights and make data-driven decisions. Here are some key aspects of PhonePe Pulse:"""),
        dcc.Markdown(""" - **Transaction Insights:** Explore various transaction types, including UPI payments, digital wallet transactions, and more.
                      Analyze transaction data for specific time periods, regions, and transaction categories."""),
        dcc.Markdown(""" - **Geographical Analysis:** Gain insights into transactions across different Indian states and regions. 
                     Understand transaction volume, values, and trends at a regional level."""),
        dcc.Markdown(" - **User Behavior:** Get a better understanding of user demographics, preferences, and engagement patterns."),
        dcc.Markdown(" - **Trend Analysis:** Track growth trends in different transaction types, identify seasonality, and more."),
        dcc.Markdown(" - **User Engagement:** Learn how and when users engage with the PhonePe app, helping businesses optimize their offerings."),
        dcc.Markdown(" - **Payment Categories:** Explore transaction data related to various payment categories, such as mobile recharges, bill payments, peer-to-peer transfers, and more."),
        dcc.Markdown(" - **Data Export:** Easily export data for further analysis or reporting."),
        dcc.Markdown(" - **Custom Dashboards:** Create custom dashboards and visualizations to meet your specific needs and preferences."),
        dcc.Markdown(" This project aims to showcase the capabilities of PhonePe Pulse and the insights it can offer to businesses and individual users."),
        dcc.Markdown(" This project will be divided into several sections, each focusing on specific aspects of PhonePe Pulse data, analysis, and visualization. Stay tuned as we dive into the world of digital payment insights!")
    ]
    return content