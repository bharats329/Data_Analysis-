import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np 

data = pd.read_csv("D:/W.O.R.K/Python/Updated_gps_dataset/Updated_googleplaystore_dataset.csv")
data.sort_values("Android_Ver", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Google Playstore Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="", className="header-emoji"),
                html.H1(
                    children="Google playstore Analytics", className="header-title"
                ),

                html.P(
                    children="Analyze the Google playstore Dataset"
                    " and the number of Installs for different category "
                    " and different genres. ",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Rating", className="menu-title"),
                        dcc.Dropdown(
                            id="Rating1",
                            options=[
                                {"label": Rating, "value": Rating}
                                for Rating in np.sort(data.Rating.unique())
                            ],
                            value="4.1",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                     children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="Type",
                            options=[
                                {"label": Type, "value": Type}
                                for Type in np.sort(data.Type.unique())
                            ],
                            value="Free",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Content_Rating", className="menu-title"),
                        dcc.Dropdown(
                            id="Content_Rating-filter",
                            options=[
                                {"label": Content_Rating, "value": Content_Rating}
                                for Content_Rating in data.Content_Rating.unique()
                            ],
                            value="Teen",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Category", className="menu-title"),
                        dcc.Dropdown(
                            id="Category",
                            options=[
                                {"label": Category, "value": Category}
                                for Category in data.Category.unique()
                            ],
                            value="Teen",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu1",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="Rating", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="installs-category", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="install-android", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]    
)


@app.callback(
    [Output("Rating", "figure"), Output("installs-category", "figure"),Output("install-android", "figure")],
    [
        Input("Rating1", "value"),
        Input("Type", "value"),
        Input("Content_Rating-filter", "value"),
        Input("Category", "value"),
        
    ],
)
def update_charts(Rating, Type, Content_Rating,Category):
    mask = (
        (data.Rating == Rating)
        & (data.Type == Type)
        & (data.Content_Rating == Content_Rating)
        & (data.Category == Category)
        
    )
    filtered_data = data.loc[mask, :]
    Rating_figure = {
        "data": [
            {
                "x": filtered_data["Android_Ver"],
                "y": filtered_data["Installs"],
                "type": "bar",
                "hovertemplate": "M%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Installs for Android Version of Application",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "M", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    installs_category_figure = {
        "data": [
            {
                "x": filtered_data["Current_Ver"],
                "y": filtered_data["Installs"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Analyze data for Current Version and Installs", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    installs_android_figure = {
        "data": [
            {
                "x": filtered_data["Genres"],
                "y": filtered_data["Installs"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {"text": "Analyze Genres for Applications", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return Rating_figure, installs_category_figure, installs_android_figure



if __name__ == "__main__":
    app.run_server(debug=True)