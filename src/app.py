from dash import Dash, html, dcc, callback, Output, Input, State
from dash_extensions import DeferScript
from datetime import datetime
from load_data import load_data_into_data_frame
import pandas as pd
import plotly.graph_objects as go
from utils import *
# pull data and put into data frame
df = load_data_into_data_frame()

##############################################
# Create App
##############################################
app = Dash()
server = app.server

app.layout = html.Div(
    className="main-container",
    children=[
        html.Div(
            className="header",
            children=[
                html.Nav(
                    className="header-control-icons",
                    children=[
                        html.Button(
                            className="header-icon-container",
                            id="filter-button",
                            children=[
                                html.Img(src="assets/icons/sliders-solid.svg")
                                ]
                        ),
                        html.Button(
                            className="header-icon-container",
                            children = [
                                html.Img(src="assets/icons/circle-question-regular.svg")
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className="content",
            children=[
                html.Div(
                    id="filter-container",
                    className="hidden",
                    children=[
                        html.Div(
                            className="filter",
                            children = [
                                html.Div(className="filter-title", children="Country"),
                                dcc.Dropdown(
                                    id="country-dropdown",
                                    options=df["Country"].unique(),
                                    clearable=True,
                                    multi=True,
                                )
                            ]
                        ),
                        html.Div(
                            className="filter",
                            children = [
                                html.Div(className="filter-title", children="Years"),
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
                            ]
                        ),
                        html.Div(
                            className="filter",
                            children = [
                                html.Div(className="filter-title", children="Name"),
                                dcc.Dropdown(
                                    id="name-dropdown", options=df["Name"], clearable=True, multi=True
                                ),
                            ]
                        ),
                        html.Div(
                            className="filter",
                            children = [
                                html.Div(className="filter-title", children="Population"),
                                dcc.RangeSlider(
                                    min=math.floor(math.log10(df["Population"].min())),
                                    max=math.ceil(math.log10(df["Population"].max())),
                                    value=[4, 5],
                                    marks={
                                        i: "{}".format(str(format_number_KM(10**i)))
                                        for i in range(math.floor(math.log10(df["Population"].min())),
                                            math.ceil(math.log10(df["Population"].max())))
                                    },
                                    id="population-range-slider",
                                    tooltip={'placement': 'bottom','transform': 'powerOfTen'},
                                ),
                            ]
                        ),
                        html.Div(
                            className="filter",
                            children = [
                                html.Div(className="filter-title", children="Parking Reform Type"),
                                dcc.Dropdown(
                                    id="parking-reform-type-dropdown",
                                    options=df["Reform Type"].unique(),
                                    clearable=True,
                                    multi=True,
                                ),
                            ]
                        ),
                        html.Div(
                            className="filter",
                            children = [
                                html.Div(className="filter-title", children="Type"),
                                dcc.Dropdown(
                                    id="type-dropdown",
                                    options=df["Type"].unique(),
                                    clearable=True,
                                    multi=True,
                                ),
                            ]
                        ),
                    ]
                ),
                dcc.Graph(
                    id="graph-content",
                    style={
                        "height":"90%"
                    }
                ),
            ]
        ),
    html.Div(
        className="footer",
        children = [
            html.Img(
                className="prn-logo-wide",
                src="assets/icons/prn-logo-wide.png",
                )
            ]
        ),
    ],
)
########################################################
# Callbacks for header buttons
########################################################
@callback(
        Output("filter-container", "className"),
        Input("filter-button", "n_clicks"),
        State("filter-container", "className"),
        prevent_initial_call=True
)
def toggleShowFilter(n_clicks, current_class_name):
    if "hidden" in current_class_name:
        return "flex-column"
    else:
        return "hidden"
    


########################################################
# Callbacks to filter data that shows up in bar graph
########################################################
@callback(
    Output("graph-content", "figure"),
    [
        Input("country-dropdown", "value"),
        Input("year-range-slider", "value"),
        Input("name-dropdown", "value"),
        Input("population-range-slider", "value"),
        Input("parking-reform-type-dropdown", "value"),
        Input("type-dropdown", "value"),
    ],
)
def update_graph(country, years, name, populations, reform_type, type):
    """change histogram to reflect the filters that the user has chosen"""
    masked_df = df
    # convert population since we use a log scale for its range slider
    populations = list(map(lambda x: 10**x, populations))

    for filter, column_name in zip(
        [country, years, name, populations, reform_type, type],
        ["Country", "Year", "Name", "Population", "Reform Type", "Type"],
    ):
        if filter is not None and filter != []:
            # range sliders
            if column_name in ["Year", "Population"]:
                masked_df = masked_df[masked_df[column_name] >= filter[0]]
                masked_df = masked_df[masked_df[column_name] <= filter[1]]
            # drop downs
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
        font=dict(size=24),
        bargap=0.1,
        xaxis=dict(
            dtick=set_attractive_x_dtick_size(years),
            title="Year",
            range=[years[0] - 1, years[1] + 1],
        ),
        yaxis={
            "dtick": set_attractive_y_dtick_size(masked_df),
            "title": "Number of Reforms",
        },
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
