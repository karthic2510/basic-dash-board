### Setting up the data for the dashboard

#Loading required packages
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

#loading dataset
data = pd.read_excel('Product Scorecard Metrics and ED Visits.xlsx')
hos_data = pd.read_csv('hospital data.csv')

#cleaning dataset
##Creating new variables for active levels
data.loc[(data['Facility Last Login(Days)'] != 0), 'Active'] = 'Active'
data.loc[(data['Facility Last Login(Days)'] == 0), 'Active'] = 'Inactive'
data.loc[ (data['Active Users'] != 0) & (data['Total Users'] != 0),'active_total_ratio'] = data['Active Users'] / data['Total Users']
data.loc[ (data['Active Users'] == 0) | (data['Total Users'] == 0),'active_total_ratio'] = 0
data['Measurement Period'] = (data['Effective End'].dt.day - data['Effective Start'].dt.day)
##Creating index of columns with null values
null_col = hos_data.isnull().sum().sort_values(ascending = False)
null_col = null_col[ null_col > 0]
#Looping through to replace NAs with mean values
null_col = null_col.index
for col in null_col:
    hos_data.loc[:, col].fillna('0', inplace = True)
##Creating index of columns with null values
null_col = data.isnull().sum().sort_values(ascending = False)
null_col = null_col[ null_col > 0]
##Looping through to replace NAs with mean values
null_col = null_col.index
for col in null_col:
    data.loc[:, col].fillna(0, inplace = True)
##Fixing data types
hos_data['staffed_beds'] = hos_data['staffed_beds'].astype(int)
hos_data['number_discharges'] = hos_data['number_discharges'].astype(int)
hos_data['est_ED_visits'] = hos_data['est_ED_visits'].astype(int)
hos_data['average_LOS'] = hos_data['average_LOS'].astype(int)
hos_data['LWBS_rate'] = hos_data['LWBS_rate'].astype(int)
##making sure missing data is captured as missing
for col in ['join_date', 'region', 'geographic_classification', 'hospital_type', 'firm_type']:
    hos_data[col] = hos_data[col].apply(lambda x: 'missing' if x == '0' else x)
##making sure engagement levels are correct
data['Engagement Level'] = data['Engagement Level'].apply(lambda x: 'Red' if x == 0 else x)
##Convering continuous levels into categorical levels for easier visualization
data_login = data.query('''`Facility Last Login(Days)` != 0''')
## creating labels
labels_4b = ['very low', 'low', 'medium', 'high']
labels_3b = ['low', 'medium', 'high']
labels_2b = ['low', 'high']
## converting last login into categorical
data_login['Login Level'], login_bins = pd.qcut(data_login['Facility Last Login(Days)'], q = [0, 0.25, 0.5, 0.75, 1], retbins= True, duplicates='drop', labels = labels_4b)
login_bins = np.concatenate(([-np.inf], login_bins[1:-1], [np.inf]))
#data_login['Login Level'].value_counts()
## converting ratio of days logged in
data_login['Login Ratio Level'], login_ratio_bins = pd.qcut(data_login['Ratio Days Logged In'], q = [0, 0.25, 0.5, 0.75, 1], retbins= True, duplicates='drop', labels = labels_4b)
login_ratio_bins = np.concatenate(([-np.inf], login_ratio_bins[1:-1], [np.inf]))
#data_login['Login Ratio Level'].value_counts()
## converting active to total user Ratiodata_login['Active User Level'], active_ratio_bins = pd.qcut(data_login['active_total_ratio'], q = [0, 0.25, 0.5, 0.75, 1], retbins= True, duplicates='drop', labels = labels_4b)
data_login['Active User Level'], active_ratio_bins = pd.qcut(data_login['active_total_ratio'], q = [0, 0.25, 0.5, 0.75, 1], retbins= True, duplicates='drop', labels = labels_4b)
active_ratio_bins = np.concatenate(([-np.inf], active_ratio_bins[1:-1], [np.inf]))
#data_login['Active User Level'].value_counts()
## converting avg time per User
data_login['Time Per User Level'], time_user_bins = pd.qcut(data_login['Avg Time per User'], q = [0, 0.25, 0.5, 0.75, 1], retbins= True, duplicates='drop', labels = labels_4b)
time_user_bins = np.concatenate(([-np.inf], time_user_bins[1:-1], [np.inf]))
#data_login['Time Per User Level'].value_counts()
## converting number of notifications
data_login['Notification Levels'], notifications_bins = pd.qcut(data_login['Notifications'], q = [0, 0.25, 0.5, 0.75, 1], retbins= True, duplicates='drop', labels = labels_4b)
notification_bins = np.concatenate(([-np.inf], notifications_bins[1:-1], [np.inf]))
#data_login['Notification Levels'].value_counts()
## using data from entries with logins to categorize all entries
data['Notification Level'] = pd.cut(data['Notifications'], bins = notification_bins, labels = labels_4b)
data['Time Per User Level'] = pd.cut(data['Avg Time per User'], bins = time_user_bins, labels = labels_4b)
data['Active User Level'] = pd.cut(data['active_total_ratio'], bins = active_ratio_bins, labels = labels_4b)
data['Login Ratio Level'] = pd.cut(data['Ratio Days Logged In'], bins = login_ratio_bins, labels = labels_4b)
data['Login Level'] = pd.cut(data['Facility Last Login(Days)'], bins = login_bins, labels = labels_4b)
data_nologin = data.query('''`Facility Last Login(Days)` == 0''')
## final dataset for use
data_comp = data[['id', 'Total Users', 'Engagement Level', 'DAU/MAU', 'Active', 'Notification Level', 'Time Per User Level', 'Active User Level', 'Login Ratio Level', 'Login Level']]
data_comp = data_comp.merge(hos_data, on = 'id', how = 'left')
## Creating index of columns with null values
null_col = data_comp.isnull().sum().sort_values(ascending = False)
null_col = null_col[ null_col > 0]
## Looping through to replace NAs with mean values
null_col = null_col.index
for col in null_col:
    data_comp.loc[:, col].fillna(0, inplace = True)
for col in ['state','join_date', 'region', 'geographic_classification', 'hospital_type', 'firm_type']:
    data_comp[col] = data_comp[col].apply(lambda x: 'missing' if x == 0 else x)
data_comp = data_comp.query('''`state` != "missing"''')
data_comp = data_comp.query('''`firm_type` != "missing"''')

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
