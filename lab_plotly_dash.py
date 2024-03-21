#import necessary libraries
import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

spacex_launch_dash = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
spacex_launch_dash.drop("Unnamed: 0", axis = 1, inplace = True)

# Create a dash application

app = dash.Dash(__name__)

# Define the layout

app.layout = html.Div(children=([
    html.H1("SpaceX Launch Records Dashboard",
            style={'textAlign': 'center'
                   }
            ),
    dcc.Dropdown(id="site-dropdown",
                 value='ALL',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 placeholder="Select a site",
                 searchable=True
                 ),
    html.Div([
        dcc.Graph(id='success-pie-chart')
    ]),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0',
                           100: '100',
                           2500: '2500',
                           5000: '5000',
                           7500: '7500'},
                    value=[spacex_launch_dash['Payload Mass (kg)'].min(),
                           spacex_launch_dash['Payload Mass (kg)'].max()]),
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ])
])
)


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(data_frame=spacex_launch_dash,
                     names='Launch Site',
                     values='class',
                     title='Total Success Launches By Site'
                     )
        return fig
    else:
        filtered_df = spacex_launch_dash[spacex_launch_dash['Launch Site'] == entered_site][
            'class'].value_counts().reset_index()
        filtered_df.rename(columns={'index': 'result', 'class': 'count'}, inplace=True)
        fig = px.pie(data_frame=filtered_df,
                     names='result',
                     values='count',
                     title=f'Total Success Launches for site {entered_site}'
                     )
        return fig


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")
               ]
              )
def get_scatter_plot(entered_site, payload_slider_value):
    if entered_site == 'ALL':

        filtered_spacex_launch_dash = spacex_launch_dash[
            (spacex_launch_dash['Payload Mass (kg)'] >= payload_slider_value[0]) &
            (spacex_launch_dash['Payload Mass (kg)'] <= payload_slider_value[1])]

        fig = px.scatter(data_frame=filtered_spacex_launch_dash,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Launch Site',
                         title=f'Correlation between Payload and Sucess by Site')
        return fig

    else:

        filtered_df = spacex_launch_dash[spacex_launch_dash["Launch Site"] == entered_site]

        filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_slider_value[0]) &
                                  (filtered_df['Payload Mass (kg)'] <= payload_slider_value[1])]

        fig = px.scatter(data_frame=filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version',
                         title=f'Total Success Lauches for site {entered_site}'
                         )
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)