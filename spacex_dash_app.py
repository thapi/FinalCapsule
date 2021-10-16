from _plotly_utils.basevalidators import DataArrayValidator
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the airline data into pandas dataframe
spacex_df =  pd.read_csv(
                    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')


min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()


# Application layout
app.layout = html.Div(children=[ 
                               html.H1('SpaceX Launch Records Dashboard', 
                                         style={'textAlign': 'Center',
                                                'color': '#503D36',
                                                 'font-size': 24}),
                                html.Div([
                                        html.Div(
                                            [
                                            html.H2('Launch Site:', style={'margin-right': '2em'}),
                                            ]
                                        ),
                                        # TASK2: Add a dropdown
                                        # Enter your code below. Make sure you have correct formatting.
                                        dcc.Dropdown(id='site-dropdown', 
                                        options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC 40', 'value': 'CCAFS LC 40'},
                                        {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'},
                                        {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'},
                                        {'label': 'CCAFS SLC 40', 'value': 'CCAFS SLC 40'}
                                        ],
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True),
                                       # Create an division for adding dropdown helper text for choosing year
                                        html.Div(
                                            [
                                            html.H2('Payload range(Kg):', style={'margin-right': '2em'})
                                            ]
                                        ),
                                        dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000',
                                        },
                                        value=[min_payload, max_payload]) ,
                                        dcc.Graph(id="success-pie-chart"),
                                        dcc.Graph(id='success-payload-scatter-chart'),
                                ]),
                            ])


@app.callback(
                # [

                Output(component_id='success-pie-chart', component_property='figure'),
                # Output(component_id='success-payload-scatter-chart', component_property='figure')
                # ],
                # [
                    Input(component_id='site-dropdown', component_property='value'), 
                #     Input(component_id="payload-slider", component_property="value")
                # ]
                )

def get_pie_chart(site):
    if site == 'ALL':
        fig = px.pie(spacex_df, values = 'class', names='Launch Site', title='title')
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']== site]
        df1=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(df1,values='class count',names='class',title=f"Total Success Launches for site {site}")
        return fig  

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def scatter(site,payload):
    low, high = (payload[0],payload[1])
    mask=spacex_df[spacex_df['Payload Mass (kg)'].between(low,high)]
    if site=='ALL':
        fig=px.scatter(mask,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
        return fig
    else:
        mask_filtered=mask[mask['Launch Site']==site]
        fig=px.scatter(mask_filtered,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload Mass for' + site)
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
                                        