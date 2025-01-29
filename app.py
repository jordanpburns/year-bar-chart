from dash import Dash, html, dcc, callback, Output, Input
from datetime import datetime
from load_data import load_data_into_data_frame
import pandas as pd
import plotly.graph_objects as go
from utils import *

#pull data and put into data frame
df = load_data_into_data_frame()

##############################################
# Create App
##############################################
app = Dash()

app.layout = html.Div(
    [
        html.Div('Country'),
        dcc.Dropdown(
            id='country-dropdown',
            options=df['Country'].unique(),
            clearable=True,
            multi=True
        ),
        html.Div('Years'),
        dcc.RangeSlider(
            min=df['Year'].min(),
            max=df['Year'].max(),
            step=1,
            value=[2000, datetime.now().year],
            id='year-range-slider',
            marks={
                i: '{}'.format(i)
                for i in range(
                    round_down_to_nearest_ten(df['Year'].min()),
                    int(df['Year'].max()),
                    10,
                )
            },
            tooltip={'placement': 'bottom', 'always_visible': True},
        ),
        html.Div('Name'),
        dcc.Dropdown(
            id='name-dropdown',
            options=df['Name'],
            clearable=True,
            multi=True
            ),
        html.Div('Population'),
        dcc.RangeSlider(
            min=0,
            max=math.ceil(math.log10(df['Population'].max())),
            value=[4, 5],
            marks={i: '{}'.format(10 ** i) for i in range(math.ceil(math.log10(df['Population'].max())))},
            id='population-range-slider',
            # tooltip={'placement': 'bottom', 'always_visible': True},
        ),
        html.Div("Parking Reform Type"),
        dcc.Dropdown(
            id='parking-reform-type-dropdown',
            options=df['Reform Type'].unique(),
            clearable=True,
            multi=True
        ),
        dcc.Graph(id='graph-content'),
    ]
)

########################################################
# Callbacks to filter data that shows up in bar graph
########################################################
@callback(
    Output('graph-content', 'figure'),
    [Input('country-dropdown', 'value'),
    Input('year-range-slider', 'value'),
    Input('name-dropdown', 'value'),
    Input('population-range-slider', 'value'),
    Input('parking-reform-type-dropdown', 'value')],
)
def update_graph(country, years, name, populations, reform_type):
    print(df['Year'].value_counts())
    """change histogram to reflect the filters that the user has chosen"""
    masked_df = df
    #convert population since we use a log scale for its range slider
    populations = list(map(lambda x: 10**x, populations))

    for filter, column_name in zip(
        [country, years, name, populations, reform_type], 
        ['Country', 'Year', 'Name', 'Population', 'Reform Type']
        ):
        if filter is not None and filter != []:
            #range sliders
            if column_name in ['Year', 'Population']:
                masked_df = masked_df[masked_df[column_name] >= filter[0]]
                masked_df = masked_df[masked_df[column_name] <= filter[1]]
            #drop downs
            else:
                masked_df = masked_df[masked_df[column_name].isin(filter)]
    fig = go.Figure()
    bar_graph_data = masked_df["Year"].value_counts()
    fig.add_trace(
        go.Bar(
            x=bar_graph_data.index,
            y=bar_graph_data.values,
        ),
    )
    fig.update_xaxes(range=[years[0], years[1]])
    fig.update_layout(
        bargap=0.1, 
        xaxis = dict(
            dtick=set_attractive_x_dtick_size(years),
            title= 'Year',
            range=[years[0]-1, years[1]+1],
        ),

        yaxis = {
            'dtick': set_attractive_y_dtick_size(masked_df),
            'title': 'Number of Reforms',
        })
    return fig

if __name__ == '__main__':
    app.run(debug=True)