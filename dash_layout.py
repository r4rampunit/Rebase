import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import folium
from folium.plugins import HeatMap
import pandas as pd
import plotly.express as px

import gdown

url = 'https://drive.google.com/uc?id=1t0DLRqjqr-xYvTv0UrmryvB73kihIueI'
output = 'pollutant_data.csv'
gdown.download(url, output, quiet=False)
df = pd.read_csv(output)

df = df.dropna(subset=['latitude', 'longitude', 'pollutant_avg'])
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Air Pollution Dashboard", style={'text-align': 'center'}),

    html.Div([
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in df['state'].unique()],
            value='Andhra_Pradesh',
            style={'color': 'white', 'background-color': 'brick', 'width': '200px', 'margin': '0 auto'}
        ),
    ], style={'text-align': 'center', 'padding': '20px'}),

    html.Div([
        html.H2("Pollution Heatmap"),
        html.Iframe(id='folium-map', width='100%', height='400')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

    html.Div([
        html.H2("Dataset of Selected Pollutant"),
        dcc.Graph(id='selected-dataset')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

    html.Div([
        html.H2("Cities with Maximum Pollution"),
        html.Iframe(id='city-map', width='100%', height='400')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

    html.Div([
        html.H2("Table of Data Crucial to Selection"),
        html.Div(id='table-data')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

    html.Div([
        html.H2("Multi Bar Plots"),
        dcc.Graph(id='multi-bar-plots')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

    html.Div([
        html.H2("Value in Red, Blue, and Green"),
        dcc.Graph(id='rbg-plot')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

    html.Div([
        html.H2("Correlation Map"),
        dcc.Graph(id='correlation-map')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

    html.Div([
        html.H2("Pie Chart"),
        dcc.Graph(id='pie-chart')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),

    html.Div([
        html.H2("Bar Plot"),
        dcc.Graph(id='another-bar-plot')
    ], style={'width': '30%', 'float': 'left', 'margin': '10px'}),
])

@app.callback(
    [Output('folium-map', 'srcDoc'),
     Output('selected-dataset', 'figure'),
     Output('city-map', 'srcDoc'),
     Output('table-data', 'children'),
     Output('multi-bar-plots', 'figure'),
     Output('rbg-plot', 'figure'),
     Output('correlation-map', 'figure'),
     Output('pie-chart', 'figure'),
     Output('another-bar-plot', 'figure')],
    Input('state-dropdown', 'value')
)
def update_plots(selected_state):
    filtered_df = df[df['state'] == selected_state]
    state_center = [filtered_df['latitude'].mean(), filtered_df['longitude'].mean()]
    m = folium.Map(location=state_center, zoom_start=8, control_scale=True)
    heat_data = []
    for index, row in filtered_df.iterrows():
        heat_data.append([row['latitude'], row['longitude'], row['pollutant_avg']])  # Append latitude, longitude, and pollutant_avg values to the heat_data list
    HeatMap(heat_data).add_to(m)
    folium_map_html = m._repr_html_()
    fig_dataset = px.scatter(filtered_df, x='longitude', y='latitude', color='city', size='pollutant_avg', hover_data=['city', 'pollutant_avg'])
    fig_dataset.update_layout(title=f'Dataset of Selected Pollutant in {selected_state}')
    city_map = folium.Map(location=state_center, zoom_start=8, control_scale=True)
    for index, row in filtered_df.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']], popup=row['city']).add_to(city_map)
    city_map_html = city_map._repr_html_()
    table_data = html.Table(
        [html.Tr([html.Th(col) for col in filtered_df[['pollutant_min', 'pollutant_max', 'pollutant_avg']].columns])] +
        [html.Tr([html.Td(filtered_df[['pollutant_min', 'pollutant_max', 'pollutant_avg']].head(7).iloc[i][col]) for col in filtered_df[['pollutant_min', 'pollutant_max', 'pollutant_avg']].columns]) for i in range(min(len(filtered_df[['pollutant_min', 'pollutant_max', 'pollutant_avg']].head(7)), 10))]
    )
    fig_multi_bar = px.bar(filtered_df, x='city', y='pollutant_avg', color='pollutant_id', barmode='group')
    rbg_data = {'Max': filtered_df['pollutant_max'].max(),
                'Avg': filtered_df['pollutant_avg'].mean(),
                'Min': filtered_df['pollutant_min'].min()}
    rbg_plot = pd.DataFrame(rbg_data, index=[0]).T.reset_index()
    rbg_plot.columns = ['Type', 'Value']
    fig_rbg = px.bar(rbg_plot, x='Type', y='Value', color='Type', barmode='group')
    fig_rbg.update_traces(marker=dict(color=['red', 'blue', 'green']))
    correlation = filtered_df[['pollutant_min', 'pollutant_max', 'pollutant_avg']].corr()
    fig_correlation = px.imshow(correlation, labels=dict(color="Correlation"), title='Correlation Between Pollutants')
    fig_pie_chart = px.pie(filtered_df, values='pollutant_avg', names='city', title=f'Pollution Distribution in {selected_state}')
    fig_another_bar_plot = px.bar(filtered_df, x='city', y='pollutant_max', color='city', title=f'Max Pollution in Cities of {selected_state}')
    return folium_map_html, fig_dataset, city_map_html, table_data, fig_multi_bar, fig_rbg, fig_correlation, fig_pie_chart, fig_another_bar_plot

if __name__ == '__main__':
    app.run_server(debug=True)
