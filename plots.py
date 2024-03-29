import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import folium


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


def line_chart(df: pd.DataFrame, settings: dict):
    fig = go.Figure()
    for color in df[settings["color"]].unique():
        color_df = df[df[settings["color"]] == color]
        fig.add_trace(
            go.Scatter(
                x=color_df[settings["x"]],
                y=color_df[settings["y"]],
                mode="lines",
                name=color,
            )
        )
    if "h_line" in settings:
        fig.add_shape(
            type="line",
            x0=0,
            y0=settings["h_line"]["y"],
            x1=1,
            y1=settings["h_line"]["y"],
            line=dict(color="Red", width=3, dash="dot"),
            xref="paper",
            yref="y",
        )

    fig.update_layout(
        xaxis_title=settings["x_title"],
        yaxis_title=settings["y_title"],
    )
    return fig


def get_map(df: pd.DataFrame, settings: dict):
    m = folium.Map(
        location=[df[settings["lat"]].mean(), df[settings["lon"]].mean()],
        zoom_start=settings["zoom"],
    )
    for i, row in df.iterrows():
        tooltip = ""
        for tt in settings["tooltip"]:
            tooltip += f"{tt['label']}: {row[tt['field']]}<br>"
        print(row[settings["marker_color_col"]])
        folium.Circle(
            location=[row["lat"], row["lon"]],
            radius=row[settings["marker_size_col"]],
            color=row[settings["marker_color_col"]],
            fill=True,
            fill_color=row[settings["marker_color_col"]],
            tooltip=tooltip,
        ).add_to(m)
    return m


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
        x=settings["x"],
        color=settings["color"],
        barmode="overlay",
        nbins=50,
        opacity=0.5,
        labels={settings["x"]: settings["color"]},
        title=settings["title"],
    )
    fig.update_layout(xaxis_title=settings["x_title"], yaxis_title=settings["y_title"])

    if "v_line" in settings:
        fig.add_shape(
            type="line",
            x0=settings["v_line"]["x"],
            y0=0,
            x1=settings["v_line"]["x"],
            y1=1,
            line=dict(color="Red", width=3, dash="dot"),
            xref="x",
            yref="paper",
        )
    return fig


def boxplot(df, settings: dict):
    settings = get_defaults(settings)
    fig = px.box(df, x=settings["x"], y=settings["y"], title=settings["title"])
    if "h_line" in settings:
        fig.add_shape(
            type="line",
            x0=0,
            y0=settings["h_line"]["y"],
            x1=1,
            y1=settings["h_line"]["y"],
            line=dict(color="Red", width=3, dash="dot"),
            xref="paper",
            yref="y",
        )

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
    return fig
