############################################################################################################################################
# Aplication is almost entierly based on IBMs' "Build a Dashboard Application with Plotly Dash" instruction                                #
#                                                                                                                                          #
# TODO:                                                                                                                                    #
# TASK 1: Add a Launch Site Drop-down Input Component                                                                                      #
# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown                                              #
# TASK 3: Add a Range Slider to Select Payload                                                                                             #
# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot                                                 #
#                                                                                                                                          #
# # To run via terminal:
# python3.8 -m pip install pandas dash
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
# # python3.8 Dashboard_Application_with_Plotly_Dash.py
############################################################################################################################################




# Importing used librares
# Dashboard Handling
import dash
# import dash_html_components as html
# import dash_core_components as dcc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
# Data Structures Handling
import pandas as pd
# Visualizations
import plotly.express as px

# Loading needed data
spacex_df = pd.read_csv("spacex_launch_dash.csv") # name of variable is ordered by TASK 2
# creating const values that will be needed for TASK 2
min_value, max_value = spacex_df["Payload Mass (kg)"].min(), spacex_df["Payload Mass (kg)"].max()

#Creating Dash
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1( # title
        'SpaceX Lunch Records Dashboard', 
        style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
    ),
    html.Br(), # page break
    dcc.Dropdown( # dropdown / TASK 1
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(), # page break
    html.Br(), # page break
    html.Div( # displaing a pyechart / TASK 2
        dcc.Graph(id='success-pie-chart')
        ),
    html.Br(), # page break
    html.P('Payload range (Kg):'), # slider title / TASK 3
    dcc.RangeSlider( # slider  / TASK 3
        id='payload-slider',
        min=0, max=10000, step=1000,
        value=[min_value, max_value],
    ),
    html.Br(), # page break
    html.Div( # displaing a scatter chart / TASK 4
        dcc.Graph(id='success-payload-scatter-chart')
        ),
])

# TASK 2
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.copy()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Lunches By Site')
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(
            filtered_df[
                filtered_df['Launch Site']==entered_site # selecting only entered_site
                ].groupby('class').count().reset_index(), # counting each element of class
            values='Unnamed: 0', # first column afther grouping
            names='class', 
            title='Total Success Lunches By {}'.format(entered_site)
        )
    return fig

# TASK 4
# add callback decorator
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property="value")
        ])
# Add computation to callback function and return graph
def get_graph(entered_site, entered_payload):
    print(entered_site)
    filtered_df =  spacex_df.copy()
    # Select data only selected by slider
    data_selected_by_slider = filtered_df['Payload Mass (kg)'].between(entered_payload[0], entered_payload[1])
    
    if entered_site == "ALL":
        fig = px.scatter(
            filtered_df[data_selected_by_slider],
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version Category",
            title='Correlation betwen Payload and Success for all Sites')
    else:
        fig = px.scatter(
            filtered_df[(data_selected_by_slider) & (filtered_df['Launch Site']==entered_site)],
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version Category",
            title='Correlation betwen Payload and Success for all Sites')
    
    return fig

if __name__ == '__main__':
    app.run_server()