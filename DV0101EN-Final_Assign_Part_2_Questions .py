#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': '...........', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': '.........'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={
                'textAlign': 'left',   # Left alignment
                'color': '#000000',    # Text color
                'fontSize': 24         # Font size
            }),#May include style for title
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type'
            style={'width': '80%','padding': '3px','fontSize': '20px','textAlignLast': 'center'}
    )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': str(year), 'value': year} for year in year_list],
            value='year'
            placeholder='Select a year', 
            style={
            'width': '80%',
            'padding': '3px',
            'fontSize': '20px',
            'textAlignLast': 'center'
        }
        )),
    html.Div([#TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='dropdown-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)

def update_input_container(selected_report):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-year', component_property='value'),
     Input(component_id='dropdown-statistics', component_property='value')]
)


def update_output_container(selected_year, selected_report):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
#TASK 2.5: Creating Graphs

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        # use groupby to create relevant data for plotting
        average_sales = sales_data.groupby('Vehicle_Type')['Number_Sold'].mean().reset_index()                           
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Number_Sold', title='Average Number of Vehicles Sold by Vehicle Type'))
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec= recession_data.groupby('Vehicle_Type')['Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                  values='Expenditure',
                  names='Vehicle_Type',
                  title="Total Expenditure Share by Vehicle Type During Recessions")
)


# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        bar_data = recession_data.groupby('unemployment_rate')['Vehicle_Type'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(bar_data, x='unemployment_rate', y='Vehicle_Type', title="Effect of Unemplyment Rate")
    )

#TASK 2.6: Returning the graphs for display
        return [
    html.Div(className='chart-grid', children=[
        html.Div(className='chart-item', children=[
            html.Div(children=R_chart1, style={'flex': '1'}),
            html.Div(children=R_chart2, style={'flex': '1'}),
        ], style={'display': 'flex'}),
        html.Div(className='chart-item', children=[
            html.Div(children=R_chart3, style={'flex': '1'}),
            html.Div(children=R_chart4, style={'flex': '1'}),
        ], style={'display': 'flex'})
    ])
]
 # Yearly Statistic Repot Plots                             
    elif (input_year and selected_statistics=='...............') :
        yearly_data = data[data['Year'] == ......]
                              
#TASK 2.5: Creating Graphs
                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales"))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(figure=px.line(yas, x='Month', y='Automobile_Sales', title="Monthly Automobile Sales"))

            # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Number_Sold'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Number_Sold',title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))
 
                    # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby('Advertising_Expenditure')['Vehicle_Type'].sum.reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data,
                  values='Advertising_Expenditure',
                  names='Vehicle_Type',
                  title="Total Expenditure Share by Vehicle Type During Recessions"))
#TASK 2.6: Returning the graphs for display
        return [
    html.Div(className='chart-grid', children=[
        html.Div(className='chart-item', children=[
            html.Div(children=R_chart1, style={'flex': '1'}),
            html.Div(children=R_chart2, style={'flex': '1'}),
        ], style={'display': 'flex'}),
        html.Div(className='chart-item', children=[
            html.Div(children=R_chart3, style={'flex': '1'}),
            html.Div(children=R_chart4, style={'flex': '1'}),
        ], style={'display': 'flex'})
    ])
]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

