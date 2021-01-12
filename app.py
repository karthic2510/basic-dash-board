### Setting up the data for the dashboard

#Loading required packages
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import os

#loading dataset
data_comp = pd.read_csv('data_comp.csv')

###############################################################################
## BUILDING THE DASH APP

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

active_levels = list(data_comp.Active.unique())
engagement_levels = list(data_comp['Engagement Level'].unique())
levels = ['very low', 'low', 'medium', 'high']
engagement_colors = {'Orange' : 'orange', 'Red' : 'red', 'Yellow': 'yellow', 'Green': 'green'}
active_colors = {'Active' : 'blue', 'Inactive' : 'red'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
sales_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = sales_app.server

sales_app.layout = html.Div([
    html.Div([
        html.H3('Data Filters'),
        dcc.Markdown('''
            ###### Hospital Activity Level
            '''),
        dcc.Dropdown(
            id = 'active_dropdown',
            options = [{'label' : x, 'value' : x} for x in active_levels],
            value = active_levels,
            multi = True,
            clearable = False,
            ),
        dcc.Markdown('''
            ###### Hospital Engagement Level
        '''),
        dcc.Dropdown(
            id = 'engagement_dropdown',
            options = [{'label' : x, 'value' : x} for x in engagement_levels],
            value = engagement_levels,
            multi = True,
            clearable = False,
        ),
        dcc.Markdown(''' ###### '''),
        html.Button(id = 'submit-val', n_clicks = 0, children = 'Submit'),
        dcc.Markdown(''' ###### '''),
        html.Div(id = 'Output-state')
        ]),
    dcc.Tabs(
        id = 'tabs-with-graphs',
        value = 'tab1',
        parent_className = 'custom-tab',
        className = 'custom-tab-container',
        children = [
            dcc.Tab(label = 'Activity', children = [
                html.Div([
                    html.Div(
                        [html.H3('Number of Hospitals by state'),
                        dcc.Graph(id = 'state_active_bar')
                        ], className = 'six columns'
                        ),
                    html.Div(
                        [html.H3('Number of Hospitals by type'),
                        dcc.Graph(id = 'type_active_bar')],
                        className = 'six columns')],
                    className = 'row')
                ]),
            dcc.Tab(label = 'Engagement', children = [
                html.Div([
                    html.Div([
                        html.H3('Distribution of Time per User and Engagement'),
                        dcc.Graph(id = 'time_per_user')],
                        className = 'six columns'
                    ),
                    html.Div([
                        html.H3('Distribution of Time since last login and Engagement'),
                        dcc.Graph(id = 'time-since-login')],
                        className = 'six columns')
                ], className = 'row'),
                html.Div([
                    html.Div([
                        html.H3('Distribution of Active Users and Engagement'),
                        dcc.Graph(id = 'active_user_hist')],
                        className = 'six columns'
                    ),
                    html.Div([
                        html.H3('Distribution of Time notifications and Engagement'),
                        dcc.Graph(id = 'notifications_hist')],
                        className = 'six columns')
                ], className = 'row')
            ])
    ])
])

@sales_app.callback(
    Output('state_active_bar', 'figure'),
    Output('type_active_bar', 'figure'),
    Output('time_per_user', 'figure'),
    Output('time-since-login', 'figure'),
    Output('active_user_hist', 'figure'),
    Output('notifications_hist', 'figure'),
    Input('submit-val', 'n_clicks'),
    State('active_dropdown', 'value'),
    State('engagement_dropdown', 'value')
)
def update_bar_chart(n_clicks, active_level, engagement_level):
    data = data_comp[data_comp['Active'].isin(active_level)]
    data = data[data['Engagement Level'].isin(engagement_level)]
    fig1 = px.histogram(data, x = 'state', color = 'Active',
        barmode = 'group', color_discrete_map = active_colors,
        height = 500,).update_xaxes(categoryorder = 'total descending')
    fig2 = px.histogram(data, x = 'hospital_type', barmode = 'group',
        color_discrete_map = active_colors,
        facet_row = 'firm_type', color = 'Active', height = 500)
    fig3 = px.histogram(data, x = 'Time Per User Level', color = 'Engagement Level',
        color_discrete_map = engagement_colors,
        barmode = 'group', height = 500).update_xaxes(categoryorder = 'array',
        categoryarray = levels)
    linedata = data.groupby(['Engagement Level', 'Login Level']).mean().reset_index()
    fig4 = px.line(linedata, x = 'Login Level', y = 'DAU/MAU',
        color_discrete_map = engagement_colors,
        color = 'Engagement Level', height = 500).update_xaxes(categoryorder = 'array',
        categoryarray = levels)
    fig5 = px.histogram(data, x = 'Active User Level', color = 'Engagement Level',
        color_discrete_map = engagement_colors,
        barmode = 'group', height = 500).update_xaxes(categoryorder = 'array',
        categoryarray = levels)
    fig6 = px.histogram(data, x = 'Notification Level', color = 'Engagement Level',
        color_discrete_map = engagement_colors, barmode = 'group',
        height = 500).update_xaxes(categoryorder = 'array',
        categoryarray = levels)
    return fig1, fig2, fig3, fig4, fig5, fig6

sales_app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    sales_app.run_server(debug=False)
