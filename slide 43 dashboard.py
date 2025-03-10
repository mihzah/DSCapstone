# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
print(spacex_df.head(5))
print(spacex_df.dtypes)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
                                    html.H1('SpaceX Launch Records Dashboard - ZM2',
                                            style={'textAlign': 'center', 'color': '#503D36',
                                                'font-size': 40}),
                                    # TASK 1: Add a dropdown list to enable Launch Site selection
                                    # The default select value is for ALL sites
                                    dcc.Dropdown(id='site-dropdown',
                                                        options=[
                                                                {'label':'All','value':'All'},
                                                                {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                                {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                                                {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                                
                                                                ],
                                                        value='All',
                                                        placeholder='Select a Launch Site here',
                                                        searchable=True
                                                        ),
                                    html.Br(),

                                    # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                    # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                    
                                    html.Div(
                                        dcc.Graph(id='success-pie-chart')
                                        ),
                                    html.Br(),

                                    html.P("Payload range (Kg):"),
                                    # TASK 3: Add a slider to select payload range
                                    dcc.RangeSlider(id='id_slider',
                                                    min=min_payload, max=max_payload, step=100,
                                                    
                                                    ),

                                    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                    html.Div(dcc.Graph(id='id_scatter_chart')),
                                    html.Br(),
                                ]
                                )
                                

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    
    filtered_df = spacex_df.copy()
    print(entered_site)
    if entered_site == 'All':        
        
        #pie_data=filtered_df[filtered_df['class']==1]
        pie_data=filtered_df
        print(pie_data.head(5))
        fig = px.pie(pie_data, 
        values='class', 
        names='Launch Site',
        title='total successful launches count for all sites',
        hole=0.3)
        return fig
    else:
    
        pie_data=filtered_df[filtered_df['Launch Site']==entered_site]
        print(pie_data.head(5))
        fig = px.pie(pie_data, 
        values='Flight Number', 
        names='class',
        title=f'total successful launches count for {entered_site}',
        hole=0.3)                
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='id_scatter_chart', component_property='figure'),
              Input(component_id='id_slider', component_property='value'))

def get_scatter(entered_value):
    
    filtered_df = spacex_df.copy()
    print(f'entered value={entered_value}')
    filtered_df=filtered_df[filtered_df['Payload Mass (kg)'].isin(range(entered_value[0],entered_value[1]))]
    scatter_data=filtered_df
    
    fig = px.scatter(scatter_data,x='Payload Mass (kg)',y='class',color='Booster Version Category')
    return fig
    

if __name__ == '__main__':
    #app.run_server(debug=True, port=8050)
    app.run(debug=True, port=8050)
