# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.P("Launch Success Ratio"),
                                dcc.Dropdown(id='site-dropdown', 
                                    options=[{'label': 'All sites', 'value': 'all'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                    value='all',
                                    multi=False,
                                    searchable=True,
                                    placeholder='Select a Launch Site here'),
                                #html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min = 0, max = 10000, step = 1000, value = [min_payload,max_payload] ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
               
# Add computation to callback function and return graph
def get_graph_pie(site_dropdown):
        df_pie =  spacex_df[['Launch Site','class']] 
        if site_dropdown == 'all':
            pie_fig = px.pie(df_pie, values='class', names='Launch Site', title='Total success launch by site')
            
            return pie_fig
                
        else:
            pie_title = f"Success launch rate for {site_dropdown}"
            df_pie1 =  df_pie[df_pie['Launch Site']==site_dropdown]
            df_pie1_LS = df_pie1.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
            pie_fig1 = px.pie(df_pie1_LS, values='class count', names='class', title=pie_title)
            
            return pie_fig1
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")] )
               
# Add computation to callback function and return graph
def get_graph_scatter(site_dropdown,slider_range):
        low = slider_range[0]
        high = slider_range[1]
        slide_df = spacex_df[spacex_df['Payload Mass (kg)'].between(low,high)]
        df_scatter =  slide_df[['Launch Site','class','Payload Mass (kg)', 'Booster Version', 'Booster Version Category']] 
        if site_dropdown == 'all':         
            scatter_fig = px.scatter(df_scatter, x='Payload Mass (kg)', y = 'class', color="Booster Version Category", title='Correlation between Payload Mass and Success for All sites')
        
            return scatter_fig
                
        else:
            scatter_title1 = f"Correlation between Payload mass and success - {site_dropdown}"
            df_scatter1 =  df_scatter[df_scatter['Launch Site']==site_dropdown]
            scatter_fig1 = px.scatter(df_scatter1, x='Payload Mass (kg)', y = 'class', color="Booster Version Category", title=scatter_title1)
            
            return scatter_fig1

# Run the app
if __name__ == '__main__':
    app.run_server()
