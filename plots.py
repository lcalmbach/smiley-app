import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 600
MONTHS_REV_DICT = {
    "Jan": 1,
    "Feb": 2,
    "Mrz": 3,
    "Apr": 4,
    "Mai": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Okt": 10,
    "Nov": 11,
    "Dez": 12,
}
MONTH_DICT = {
    "Jan": 1,
    "Feb": 2,
    "Mrz": 3,
    "Apr": 4,
    "Mai": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Okt": 10,
    "Nov": 11,
    "Dez": 12,
}


def get_defaults(settings: dict) -> dict:
    if "title" not in settings:
        settings["title"] = ""
    if "width" not in settings:
        settings["width"] = DEFAULT_WIDTH
    if "height" not in settings:
        settings["height"] = DEFAULT_HEIGHT
    return settings


def histogram(df: pd.DataFrame, settings: dict):
    settings = get_defaults(settings)
    fig = px.histogram(
        df,
        x="value",
        color="parameter",
        barmode="overlay",
        nbins=30,
        opacity=0.5,
        labels={"value": "value"},
        title=settings["title"],
    )

    return fig


def boxplot(df, settings: dict):
    settings = get_defaults(settings)
    fig = px.box(df, x="parameter", y="value", title=settings["title"])

    return fig


def scatter(df, settings: dict):
    settings = get_defaults(settings)
    fig = px.scatter(
        df,
        x=settings["x"],
        y=settings["y"],
        title=settings["title"],
        opacity=0.5,
        size_max=1,
        labels={settings["x"]: settings["x_title"], settings["y"]: settings["y_title"]},
    )

    x_range = [
        min(df[settings["x"]].min(), df[settings["y"]].min()),
        max(df[settings["x"]].max(), df[settings["y"]].max()),
    ]
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=x_range,
            mode="lines",
            name="1:1 Linie",
            line=dict(dash="dash", color="red"),
        )
    )
    # fig.data = [fig.data[0], fig.data[1]]
    return fig
