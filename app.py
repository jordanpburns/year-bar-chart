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
        html.Div("Country"),
        dcc.Dropdown(
            id="country-dropdown",
            options=df["Country"].unique(),
            value="US",
            clearable=True,
        ),
        html.Div("Years"),
        dcc.RangeSlider(
            min=df["Year"].min(),
            max=df["Year"].max(),
            step=1,
            value=[2000, datetime.now().year],
            id="year-range-slider",
            marks={
                i: "{}".format(i)
                for i in range(
                    round_down_to_nearest_ten(df["Year"].min()),
                    int(df["Year"].max()),
                    10,
                )
            },
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        dcc.Graph(id="graph-content"),
    ]
)


########################################################
# Callbacks to filter data that shows up in bar graph
########################################################
@callback(
    Output("graph-content", "figure"),
    [Input("country-dropdown", "value"), Input("year-range-slider", "value")],
)
def update_graph(country, years):
    """change histogram to reflect the filters that the user has chosen"""
    country_mask = df["Country"] == country
    min_year_mask = df["Year"] >= years[0]
    max_year_mask = df["Year"] <= years[1]
    masked_df_years = df[(country_mask) & (min_year_mask) & (max_year_mask)]["Year"]
    
    fig = go.Figure()
    bar_graph_data = masked_df_years.value_counts()
    fig.add_trace(
        go.Bar(
            x=bar_graph_data.index,
            y=bar_graph_data.values,
        ),
    )
    # TODO fix xticks when interval is small so there aren't repeated numbers
    fig.update_xaxes(range=[years[0], years[1]])
    fig.update_layout(
        bargap=0.1, 
        xaxis = dict(
            dtick=set_attractive_x_dtick_size(years),
            title= "Year",
            range=[years[0]-1, years[1]+1],
        ),

        yaxis = {
            "dtick": set_attractive_y_dtick_size(masked_df_years),
            "title": "Number of Reforms",
        })
    return fig

if __name__ == "__main__":
    app.run(debug=True)
