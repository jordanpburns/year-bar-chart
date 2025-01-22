from dash import Dash, html, dcc, callback, Output, Input
from datetime import datetime
import json
import plotly.express as px
import pandas as pd

# load reform data
data_file = open('./data/core.json')
data = json.load(data_file)

####################################################
# Put data from json file into Pandas DataFrame
####################################################

# I'm organizing the data as one row for each parking minimum removal 
# and parking maximum addition. So there can be mutiple rows per city.

# create lists to hold intermediate data to be added into the dataframe
coord_list = []
country_list = []
name_list = []
pop_list = []
repeal_list = []
state_list = []
type_list = []
removed_minimum_or_added_maximum = []
date_list = []
year_list = []
land_list = []
scope_list = []
status_list = []


# loop through all entries and put data into a list for each column of eventual DataFrame
for entry in data.values():
    place = entry['place']

# create row for each parking minimum removed
    try:
        rm_min = entry['rm_min']
        
        for removed_minimum in rm_min:

            coord_list.append(place['coord'])
            country_list.append(place['country'])
            name_list.append(place['name'])
            pop_list.append(place['pop'])
            repeal_list.append(place['repeal'])
            state_list.append(place['state'])
            type_list.append(place['type'])
            removed_minimum_or_added_maximum.append('Removed Parking Minimum')
            date_list.append(removed_minimum['date'])
            try:
                year_list.append(datetime.strptime(removed_minimum['date'], '%y-%m-%d').year)
            except:
                year_list.append(None)
            land_list.append(removed_minimum['land'])
            scope_list.append(removed_minimum['scope'])
            status_list.append(removed_minimum['status'])
    except:
        pass

# create row for each parking maximum added
    try:
        add_max = entry['add_max']
        
        for added_maximum in add_max:

            coord_list.append(place['coord'])
            country_list.append(place['country'])
            name_list.append(place['name'])
            pop_list.append(place['pop'])
            repeal_list.append(place['repeal'])
            state_list.append(place['state'])
            type_list.append(place['type'])
            removed_minimum_or_added_maximum.append('Added Parking Maximum')
            date_list.append(added_maximum['date'])
            try:
                year_list.append(datetime.strptime(added_maximum['date'], '%Y-%m-%d').year)
            except:
                year_list.append(None)
            land_list.append(added_maximum['land'])
            scope_list.append(added_maximum['scope'])
            status_list.append(added_maximum['status'])
    except:
        pass

# put lists into new dictionary to create DataFrame
data_list_dict = {
    'Coordinates': coord_list, 
    'Country': country_list,
    'Name': name_list,
    'Population': pop_list,
    'Repealed': repeal_list,
    'State': state_list,
    'Type': type_list,
    'Removed Minimum or Added Maximum': removed_minimum_or_added_maximum,
    'Date': date_list,
    'Year': year_list,
    'Land': land_list,
    'Scope': scope_list,
    'Status': status_list,
    }

df = pd.DataFrame(data_list_dict)

##############################################
# Create App
##############################################
app = Dash()

app.layout = html.Div([
    html.Div('Country'),
    dcc.Dropdown(
        id='country-dropdown',
        options=df["Country"].unique(),
        value='US',
        clearable=True,
    ),
    html.Div("Years"),
    dcc.RangeSlider(
        min = df["Year"].min(), 
        max = df["Year"].max(), 
        value=[2000, datetime.now().year], 
        id='year-range-slider',
        marks={i: '{}'.format(i) for i in range(int(df["Year"].min()),int(df["Year"].max()),10)}
    ),
        
    dcc.Graph(id='graph-content')
])


########################################################
# Callbacks to filter data that shows up in bar graph
########################################################
@callback(
        Output('graph-content', 'figure'), 
        [Input('country-dropdown', 'value'),
         Input('year-range-slider', 'value')])
def update_graph(country, years):

    country_mask = df['Country'] == country
    min_year_mask = df['Year'] > years[0]
    max_year_mask = df['Year'] < years[1]
    fig = px.histogram(df[(country_mask) & (min_year_mask) & (max_year_mask)], x="Year")
    fig.update_layout(bargap=0.2)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
