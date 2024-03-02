import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests

# Initialize the Dash app
app = dash.Dash(__name__)

# Define colors
colors = {
    'background': '#f4f4f4',
    'text': '#333333',
}

# Define layout of the dashboard
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1("COVID-19 Dashboard", style={'textAlign': 'center', 'color': colors['text']}),

    # Dropdown to select country
    html.Label('Select Country:'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': 'Global', 'value': 'global'},
            {'label': 'USA', 'value': 'USA'},
            {'label': 'India', 'value': 'India'},
            # Add more countries as needed
        ],
        value='global',  # Default value
        style={'width': '50%'}
    ),

    # Graphs to display COVID-19 statistics
    dcc.Graph(id='confirmed-cases-graph'),
    dcc.Graph(id='recovered-cases-graph'),
    dcc.Graph(id='deaths-graph'),
])

# Callback to update graphs based on country selection
@app.callback(
    Output('confirmed-cases-graph', 'figure'),
    Output('recovered-cases-graph', 'figure'),
    Output('deaths-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_graphs(selected_country):
    if selected_country == 'global':
        url = 'https://api.covid19api.com/summary'
    else:
        url = f'https://api.covid19api.com/total/dayone/country/{selected_country}'

    response = requests.get(url)
    data = response.json()

    if selected_country == 'global':
        global_data = data['Global']
        dates = list(map(lambda x: x['Date'], data['Countries']))
        confirmed_cases = list(map(lambda x: x['TotalConfirmed'], data['Countries']))
        recovered_cases = list(map(lambda x: x['TotalRecovered'], data['Countries']))
        deaths = list(map(lambda x: x['TotalDeaths'], data['Countries']))
    else:
        dates = list(map(lambda x: x['Date'], data))
        confirmed_cases = list(map(lambda x: x['Confirmed'], data))
        recovered_cases = list(map(lambda x: x['Recovered'], data))
        deaths = list(map(lambda x: x['Deaths'], data))

    confirmed_cases_trace = go.Scatter(x=dates, y=confirmed_cases, mode='lines', name='Confirmed Cases')
    recovered_cases_trace = go.Scatter(x=dates, y=recovered_cases, mode='lines', name='Recovered Cases')
    deaths_trace = go.Scatter(x=dates, y=deaths, mode='lines', name='Deaths')

    confirmed_cases_layout = go.Layout(title='Confirmed Cases', xaxis=dict(title='Date'), yaxis=dict(title='Cases'))
    recovered_cases_layout = go.Layout(title='Recovered Cases', xaxis=dict(title='Date'), yaxis=dict(title='Cases'))
    deaths_layout = go.Layout(title='Deaths', xaxis=dict(title='Date'), yaxis=dict(title='Cases'))

    return {'data': [confirmed_cases_trace], 'layout': confirmed_cases_layout}, \
           {'data': [recovered_cases_trace], 'layout': recovered_cases_layout}, \
           {'data': [deaths_trace], 'layout': deaths_layout}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
