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
state_levels = list(data_comp['state'].unique())
levels = ['very low', 'low', 'medium', 'high']
engagement_colors = {'Orange' : 'orange', 'Red' : 'red', 'Yellow': 'yellow', 'Green': 'green'}
active_colors = {'Active' : 'blue', 'Inactive' : 'red'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
sales_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = sales_app.server

sales_app.layout = html.Div([
    html.Div([
        html.H1('Basic Sales Dashboard'),
        dcc.Markdown('''
            The following dashboard is a simple, basic dashboard I created for a fun data visualization assignment. The full visualization assignment had more parts to it, and a deeper dive into the data.
            This dashboard gives you the basics of how to approach the fundamental business questions while trying to analyse user activity.
            The two tabs below are the first half of a dashboard meant for an account manager to understand what is happening with his accounts.
        '''),
        html.H3('Filters'),
        dcc.Markdown('''
            Use the filters below the refine the data being shown in the graphs below.
            ###### Hospital Activity Level
            This dropdown helps the user filter only those accounts which are active or inactive in the past 30 days.
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
            The data provided had each account categorized into 1 of 4 engagement levels based on internal metrics. This filter helps the user dive into a specific engagement level.
        '''),
        dcc.Dropdown(
            id = 'engagement_dropdown',
            options = [{'label' : x, 'value' : x} for x in engagement_levels],
            value = engagement_levels,
            multi = True,
            clearable = False,
        ),
        dcc.Markdown('''
            ###### Account State
            State in which the account exists.
        '''),
        dcc.Dropdown(
            id = 'state_dropdown',
            options = [{'label' : x, 'value' : x} for x in state_levels],
            value = state_levels,
            multi = True,
            clearable = False,
        ),
        dcc.Markdown(''' ###### '''),
        html.Button(id = 'submit-val', n_clicks = 0, children = 'Submit'),
        dcc.Markdown('''
            ######
            The user begins with an overview of active and inactive accounts across different states and different account types.
            This would help them identify where they need to focus more.
            For example, if they feel there is a high percentage of inactive accounts, they can dive into the state with the highest number of such accounts.
         '''),
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
                        [html.H3('Accounts by State'),
                        dcc.Markdown('''
                            This graph visualizes the number of active/inactive accounts in each state that the user oversees.
                            For example, none of the accounts in UTAH is active. This is worth exploring further.
                        '''),
                        dcc.Graph(id = 'state_active_bar')
                        ], className = 'six columns'
                        ),
                    html.Div(
                        [html.H3('Accounts by Type'),
                        dcc.Markdown('''
                            This graph visualizes the number of active/inactive accounts by type of account.
                            Often, sales associates group accounts by their size/type. This would help them identify which type to build new strategies for.
                            For example, Should we continue spending on reaching out to Children's Hospitals?
                        '''),
                        dcc.Graph(id = 'type_active_bar')],
                        className = 'six columns')],
                    className = 'row')
                ]),
            dcc.Tab(label = 'Engagement', children = [
                html.Div([dcc.Markdown('''
                    #### 
                    These graphs visualizes the number of accounts with varying levels of activity (based on different measures) by the average user across engagement levels.
                    The goal is to identify accounts with low engagement (a red or an orange), which are still engaging at a high rate based on a single metric.
                    Are these potential low-hanging fruits?
                    ####
                ''')]),
                html.Div([
                    html.Div([
                        html.H3('Distribution of Time Spent per User across Accounts'),
                        dcc.Graph(id = 'time_per_user')],
                        className = 'six columns'
                    ),
                    html.Div([
                        html.H3('Distribution of Time since last login across Accounts'),
                        dcc.Graph(id = 'time-since-login')],
                        className = 'six columns')
                ], className = 'row'),
                html.Div([
                    html.Div([
                        html.H3('Distribution of Active Users across Accounts'),
                        dcc.Graph(id = 'active_user_hist')],
                        className = 'six columns'
                    ),
                    html.Div([
                        html.H3('Distribution of Notifications across Accounts'),
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
    State('engagement_dropdown', 'value'),
    State('state_dropdown', 'value')
)
def update_bar_chart(n_clicks, active_level, engagement_level, state_level):
    data = data_comp[data_comp['Active'].isin(active_level)]
    data = data[data['Engagement Level'].isin(engagement_level)]
    data = data[data['state'].isin(state_level)]
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
