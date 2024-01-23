# download link
# https://data.bs.ch/api/explore/v2.1/catalog/datasets/100268/exports/csv?lang=de&timezone=Europe%2FZurich&use_labels=false&delimiter=%3B&select=zyklus,phase,id_standort,messung_datum,messung_zeit,v_einfahrt,v_ausfahrt,v_delta,geschwindigkeit&where=messung_jahr=2023

import streamlit as st
import os
import numpy as np
import pandas as pd
from enum import Enum
from scipy import stats
from streamlit_folium import folium_static
import logging
import time

from plots import histogram, boxplot, scatter, get_map, line_chart
from texts import (
    INFO,
    STAT_TEXT,
    STAT_COLUMNS_DESCRIPTION,
    STAT_TABLE_INFO,
    H0_RESULT_ALL,
    H0_RESULT_EXC,
    H0_RESULT_EXC_EXPECTED1,
    H0_RESULT_EXC_EXPECTED2,
)
from utils import optimize_dataframe_types, enum2dict

MARKER_COLOR = "red"
PARQUET_FILE = "./data/100268.parquet"
CSV_FILE = "./data/100268.csv"
CSV_STATIONS_FILE = "./data/100286.csv"
MAX_STATIONS = 10

menu_options = [
    "Über die App",
    "Vergleich Geschw. Einfahrt/Ausfahrt",
    "Statistiken",
    "Karte",
    # "kumulatives Liniendiagramm",
]

time_options = ["07:00-19:59h", "20:00-06:59h"]
time2_options = dict(zip(range(24), [f"x{x}:00-{x}:59h" for x in range(24)]))
weekday_options = ["Alle", "Montag-Freitag", "Samstag-Sonntag"]
velocity_options = {
    -1: "Alle",
    20: "20 km/h",
    30: "30 km/h",
    40: "40 km/h",
    50: "50 km/h",
}
weekday2_options = {
    0: "Montag",
    1: "Dienstag",
    2: "Mittwoch",
    3: "Donnerstag",
    4: "Freitag",
    5: "Samstag",
    6: "Sonntag",
}
month_options = range(1, 13)
plot_options = ["Histogramm", "Boxplot", "XY", "Kumulatives Liniendiagramm"]
stats_parameter_options = {
    "v_einfahrt_median": "Geschw. Einfahrt (median)",
    "v_einfahrt_percentile_85": "Geschw. Einfahrt (85-Perz.)",
    "v_ausfahrt_median": "Geschw. Ausfahrt (median)",
    "v_ausfahrt_percentile_85": "Geschw. Ausfahrt (85-Perz.)",
    "diff_einfahrt_ausfahrt_median": "Differenz Ausfahrt-Einfahrt (median)",
    "diff_einfahrt_ausfahrt_percentile_85": "Differenz Ausfahrt-Einfahrt (85-Perz.)",
    "uebertretung_einfahrt_median": "Übertretung Einfahrt (median)",
    "uebertretung_einfahrt_percentile_85": "Übertretung Einfahrt (85-Perz.)",
    "uebertretung_ausfahrt_median": "Übertretung Ausfahrt (median)",
    "uebertretung_ausfahrt_percentile_85": "Übertretung Ausfahrt (85-Perz.)",
    "ist_uebertretung_einfahrt_sum": "Anzahl Übertretungen Einfahrt",
    "ist_uebertretung_ausfahrt_sum": "Anzahl Übertretungen Ausfahrt",
    "ist_uebertretung_einfahrt_pct": "Prozent Übertretungen Einfahrt",
    "ist_uebertretung_ausfahrt_pct": "Prozent Übertretungen Ausfahrt",
}


class Phase(Enum):
    Alle = "Wähle eine Phase"
    VORMESSUNG = "Vormessung"
    BETRIEB = "Betrieb"
    NACHMESSUNG = "Nachmessung"
    NACHENDE = "Nach Ende"


class Smiley:
    def __init__(self):
        self.data, self.stations = self.get_data()
        self.filtered_stations = pd.DataFrame()
        self.filtered_data = pd.DataFrame()
        self.station_options = dict(
            zip(self.stations["id_standort"], self.stations["strname"])
        )
        self.filtered_data = pd.DataFrame()
        self.filtered_stations = pd.DataFrame()

    def wilcoxon_test(self, data, col_before, col_after):
        # Perform the paired t-test
        # LC: seems better to use non parametric test since data is often not normally distributed
        # t_stat, p_value = stats.ttest_rel(data[col_before], data[col_after])
        w_stat, p_value = stats.wilcoxon(data[col_before], data[col_after])
        alpha = 0.05
        h0_rejected = p_value < alpha
        return w_stat, p_value, h0_rejected

    def filter_data(self, keys: list):
        filtered_data = self.data
        filtered_stations = self.stations

        with st.sidebar.expander("🔎 Filter", expanded=True):
            # station filters
            if "velocity" in keys:
                sel_velocity = st.selectbox(
                    label="Höchstgeschwindigkeit",
                    options=velocity_options.keys(),
                    format_func=lambda x: velocity_options[x],
                )
                if sel_velocity > 0:
                    filtered_stations = filtered_stations[
                        filtered_stations["geschwind"] == sel_velocity
                    ]
            if "station" in keys:
                sel_station = st.selectbox(
                    "Standort",
                    options=self.station_options.keys(),
                    format_func=lambda x: self.station_options[x],
                )
                filtered_stations = filtered_stations[
                    filtered_stations["id_standort"] == sel_station
                ]
            if "stations" in keys:
                sel_stations = st.multiselect(
                    "Standorte",
                    options=self.station_options.keys(),
                    format_func=lambda x: self.station_options[x],
                    default=filtered_stations["id_standort"].iloc[0],
                    help="wähle ein oder mehrere Standorte, die angezeigt werden sollen. Wenn keine Standorte ausgewählt werden, werden alle Standorte angezeigt.",
                )
                if sel_stations:
                    filtered_stations = filtered_stations[
                        filtered_stations["id_standort"].isin(sel_stations)
                    ]
            if len(filtered_stations) < len(self.stations):
                filtered_data = self.data[
                    self.data["id_standort"].isin(
                        filtered_stations["id_standort"].unique()
                    )
                ]
            # measurement filters
            if "phase" in keys:
                sel_phase = st.selectbox("Phase", [member.value for member in Phase], index=2)
                if sel_phase != Phase.Alle.value:
                    filtered_data = filtered_data[filtered_data["phase"] == sel_phase]
            if "weekday-weekend" in keys:
                sel_weekday = st.selectbox("Wochentag", weekday_options)
                if sel_weekday == weekday_options[1]:
                    filtered_data = filtered_data[
                        filtered_data["messung_datum"].dt.weekday < 5
                    ]
                elif sel_weekday == weekday_options[2]:
                    filtered_data = filtered_data[
                        filtered_data["messung_datum"].dt.weekday >= 5
                    ]
        return filtered_data, filtered_stations

    def get_data(self):
        def remove_outliers(df: pd.DataFrame):
            """
            Remove outliers from a DataFrame based on the 'v_einfahrt' column.

            Args:
                df (pd.DataFrame): The input DataFrame.

            Returns:
                pd.DataFrame: The cleaned DataFrame with outliers removed.
            """
            cleaned_df = pd.DataFrame()
            df["v_max"] = df[["v_einfahrt", "v_ausfahrt"]].max(axis=1)
            for station in df["id_standort"].unique():
                data = df[df["id_standort"] == station]
                data = data[np.abs(stats.zscore(data["v_max"])) < 3]
                cleaned_df = pd.concat([cleaned_df, data])
            st.info(f"{len(df)-len(cleaned_df)} rows removed.")
            return cleaned_df

        if not os.path.exists(PARQUET_FILE):
            with st.spinner("Daten werden geladen..."):
                data = pd.read_csv(CSV_FILE, sep=";")
                data["messung_datum"] = pd.to_datetime(
                    data["messung_datum"], errors="coerce"
                )
                data["wochentag"] = pd.to_datetime(data["messung_datum"]).dt.dayofweek
                data["stunde"] = data["messung_zeit"][:2]
                fields = [
                    "zyklus",
                    "phase",
                    "id_standort",
                    "messung_datum",
                    "messung_zeit",
                    "v_einfahrt",
                    "v_ausfahrt",
                    "geschwindigkeit",
                ]
                data = data[fields]
                data = optimize_dataframe_types(data)
                data["phase"] = data["phase"].astype("category")
                data = remove_outliers(data)
                data.to_parquet(PARQUET_FILE)
        data = pd.read_parquet(PARQUET_FILE)
        data = data[data["phase"] != Phase.NACHENDE.value]
        # memory = data.memory_usage(deep=True).sum()
        # print(f"Memory usage: {memory / 1024 ** 2:.2f} MB")

        stations = pd.read_csv(CSV_STATIONS_FILE, sep=";")
        stations[["lat", "lon"]] = stations["geo_point_2d"].str.split(",", expand=True)
        stations["lat"] = stations["lat"].astype(float)
        stations["lon"] = stations["lon"].astype(float)
        stations = stations.drop(columns=["geo_point_2d", "geo_shape"])
        stations.rename(columns={"idstandort": "id_standort"}, inplace=True)
        stations_with_data = data["id_standort"].unique()
        stations = stations[stations["id_standort"].isin(stations_with_data)]
        return data, stations

    def get_chart(self, df, melted_df: pd.DataFrame, velocity: float, plot: str):
        chart = None
        if plot == plot_options[0]:
            plot_settings = {
                "x": "Geschwindigkeit",
                "color": "Messung",
                "v_line": {"x": velocity},
                "y_title": "Anzahl Messungen",
                "x_title": "Geschwindigkeit (km/h)",
            }
            chart = histogram(melted_df, plot_settings)
        elif plot == plot_options[1]:
            plot_settings = {
                "x": "Messung",
                "y": "Geschwindigkeit",
                "h_line": {"y": velocity},
            }
            chart = boxplot(melted_df, plot_settings)
        elif plot == plot_options[2]:
            plot_settings = {
                "x": "v_einfahrt",
                "y": "v_ausfahrt",
                "x_title": "V Einfahrt (km/h)",
                "y_title": "V Ausfahrt (km/h))",
            }
            df_xy = df[["v_einfahrt", "v_ausfahrt"]].copy()
            df_xy.drop_duplicates(inplace=True)
            chart = scatter(df_xy, plot_settings)
        elif plot == plot_options[3]:
            lst_e = df["v_einfahrt"].sort_values().tolist()
            lst_a = df["v_ausfahrt"].sort_values().tolist()
            lst_length = len(lst_e)
            lst_e_pct = [(i + 1) / lst_length * 100 for i in range(lst_length)]
            lst_length = len(lst_a)
            lst_a_pct = [(i + 1) / lst_length * 100 for i in range(lst_length)]
            df_pct = pd.DataFrame(
                {"messung": ["Einfahrt"] * len(lst_e), "pct": lst_e_pct, "v": lst_e}
            )
            df_pct = pd.concat(
                [
                    df_pct,
                    pd.DataFrame(
                        {
                            "messung": ["Ausfahrt"] * len(lst_a),
                            "pct": lst_a_pct,
                            "v": lst_a,
                        }
                    ),
                ]
            )
            df_pct = df_pct.groupby(["messung", "v"])["pct"].max().reset_index()
            plot_settings = {
                "x": "pct",
                "y": "v",
                "x_title": "Prozent",
                "y_title": "Geschwindigkeit (km/h)",
                "color": "messung",
                "h_line": {"y": velocity},
            }
            chart = line_chart(df_pct, plot_settings)
        return chart

    def show_plots(self, data, plots: list, station: dict):
        melted_df = pd.melt(
            data[["id_standort", "v_einfahrt", "v_ausfahrt"]],
            id_vars=["id_standort"],
            var_name="Messung",
            value_name="Geschwindigkeit",
        )
        col_index = 0
        col_num = 2 if len(plots) > 1 else 1
        cols = st.columns(col_num)
        for plot in plots:
            with cols[col_index]:
                chart = self.get_chart(data, melted_df, station["geschwind"], plot)
                st.plotly_chart(
                    chart,
                    use_container_width=True,
                    sharing="streamlit",
                    theme="streamlit",
                )
                col_index = 0 if col_index == 1 else 1

    def show_phase_comparison(self):
        """
        Displays the phase comparison for selected stations.

        This method filters the data based on selected filters, retrieves the settings for plots,
        and then displays the phase comparison for each station.

        Parameters:
        None

        Returns:
        None
        """

        def get_settings(keys: list):
            settings = {}
            with st.sidebar.expander("⚙️ Settings", expanded=True):
                plot1 = st.selectbox("Graphik links", options=plot_options)
                plot2_options = ['Wähle eine Grafik'] + [x for x in plot_options if x != plot1]
                plot2 = st.selectbox("Graphik rechts", options=plot2_options, index = 1)
                settings['plots'] = [plot1, plot2] if plot2_options.index(plot2) > 0 else [plot1]
            return settings

        filters = [
            "locations",
            "velocity",
            "stations",
            "phase",
            "weekday-weekend",
            "day-night",
        ]
        self.filtered_data, self.filtered_stations = self.filter_data(filters)
        settings = get_settings(["plots"])

        for station in list(self.filtered_stations["id_standort"])[: MAX_STATIONS + 1]:
            data = self.filtered_data[self.filtered_data["id_standort"] == station]
            station = self.stations[self.stations["id_standort"] == station].iloc[0]
            measurements = f"{len(self.filtered_data):,}".replace(",", "'")
            st.markdown(
                f"{station['strname']} {station['hausnr']} (id={station['id_standort']}) Höchstgeschwindigkeit: {station['geschwind']} km/h, {measurements} Messungen."
            )
            self.show_plots(data, settings['plots'], station)

        text = "Die gepunktete Linie in den Grafiken zeigt die erlaubte Höchstgeschwindigkeit am Standort an."
        if len(self.filtered_stations) > MAX_STATIONS:
            text += f" Es werden nur die ersten {MAX_STATIONS} Standorte angezeigt. Bitte filtere die Daten mit der Standorte Auswahlliste in der Navigationsleiste, um die gewünschten Standorte zu zeigen."
        st.markdown(text)

    def info(self):
        st.image("./assets/splash.jpg", width=1000)
        cols = st.columns([1, 4, 1])
        with cols[1]:
            st.markdown(INFO, unsafe_allow_html=True)

    def get_stats_table(self, df, aggregation_fields):
        df.drop(columns=["zyklus"], inplace=True)
        df["diff_einfahrt_ausfahrt"] = df["v_einfahrt"] - df["v_ausfahrt"]
        df["uebertretung_einfahrt"] = df["v_einfahrt"] - df["geschwindigkeit"]
        df["uebertretung_ausfahrt"] = df["v_ausfahrt"] - df["geschwindigkeit"]
        df["ist_uebertretung_einfahrt"] = np.where(
            df["v_einfahrt"] > df["geschwindigkeit"], 1, 0
        )
        df["ist_uebertretung_ausfahrt"] = np.where(
            df["v_ausfahrt"] > df["geschwindigkeit"], 1, 0
        )

        aggregated_df = df.groupby(aggregation_fields).agg(
            {
                "v_einfahrt": [
                    ("median", "median"),
                    ("percentile_85", lambda x: x.quantile(0.85)),
                    ("count", "count"),
                ],
                "v_ausfahrt": [
                    ("median", "median"),
                    ("percentile_85", lambda x: x.quantile(0.85)),
                ],
                "diff_einfahrt_ausfahrt": [
                    ("median", "median"),
                    ("percentile_85", lambda x: x.quantile(0.85)),
                ],
                "uebertretung_einfahrt": [
                    ("median", "median"),
                    ("percentile_85", lambda x: x.quantile(0.85)),
                ],
                "uebertretung_ausfahrt": [
                    ("median", "median"),
                    ("percentile_85", lambda x: x.quantile(0.85)),
                ],
                "ist_uebertretung_einfahrt": [
                    ("sum", "sum"),
                ],
                "ist_uebertretung_ausfahrt": [
                    ("sum", "sum"),
                ],
            }
        )
        # convert multiindex to single index
        aggregated_df.columns = ["_".join(x) for x in aggregated_df.columns.ravel()]
        aggregated_df.rename(columns={"v_einfahrt_count": "anz"}, inplace=True)
        aggregated_df["ist_uebertretung_einfahrt_pct"] = (
            aggregated_df["ist_uebertretung_einfahrt_sum"] / aggregated_df["anz"] * 100
        )
        aggregated_df["ist_uebertretung_ausfahrt_pct"] = (
            aggregated_df["ist_uebertretung_ausfahrt_sum"] / aggregated_df["anz"] * 100
        )
        aggregated_df.reset_index(inplace=True)
        aggregated_df.dropna(subset=["v_einfahrt_median"], inplace=True)
        return aggregated_df

    def get_kennzahlen_stations(self, df: pd.DataFrame):
        result = {}
        result["num_measurement"] = df["anz"].sum()
        result["num_stations"] = len(df["id_standort"].unique())
        result["mean_exeedance_median"] = df["uebertretung_einfahrt_median"].mean()
        result["mean_exeedance_p85"] = df["uebertretung_einfahrt_percentile_85"].mean()
        result["num_reduction_median"] = len(
            df[df["v_einfahrt_median"] > df["v_ausfahrt_median"]]
        )
        result["pct_reduction_median"] = (
            result["num_reduction_median"] / result["num_stations"] * 100
        )
        result["num_reduction_p85"] = len(
            df[df["v_einfahrt_median"] > df["v_ausfahrt_median"]]
        )
        result["pct_reduction_p85"] = (
            result["num_reduction_p85"] / result["num_stations"] * 100
        )
        result["delta_median"] = (
            df["v_einfahrt_median"] - df["v_ausfahrt_median"]
        ).mean()
        result["delta_p85"] = (
            df["v_einfahrt_percentile_85"] - df["v_ausfahrt_percentile_85"]
        ).mean()
        result["num_exceedance_decrease"] = len(
            df[
                df["ist_uebertretung_einfahrt_sum"]
                > df["ist_uebertretung_ausfahrt_sum"]
            ]
        )
        result["pct_exceedance_decrease"] = (
            result["num_exceedance_decrease"] / result["num_stations"] * 100
        )
        return result

    def get_kennzahlen(self, df: pd.DataFrame):
        result = {}
        result["num_measurement"] = df["id_standort"].count()
        result["num_stations"] = len(df["id_standort"].unique())
        result["mean_exeedance_in"] = (df["v_einfahrt"] - df["geschwindigkeit"]).mean()
        result["mean_exeedance_out"] = (df["v_einfahrt"] - df["geschwindigkeit"]).mean()

        return result

    def show_statistics(self):
        def get_phase_text(summary_dict: dict, phase: str):
            text = STAT_TEXT.format(
                phase,
                f"{summary_dict['num_measurement']:,}".replace(",", "'"),
                summary_dict["num_reduction_median"],
                summary_dict["num_stations"],
                f"{summary_dict['pct_reduction_median']: .1f}",
                f"{summary_dict['delta_p85'] : .1f}",
                summary_dict["num_reduction_median"],
                f"{summary_dict['pct_reduction_median']: .1f}",
                summary_dict["num_exceedance_decrease"],
                f"{summary_dict['pct_exceedance_decrease']: .1f}",
            )
            return text

        def get_summmary_table(data: dict):
            df = pd.DataFrame.from_dict(data, orient="index").transpose()
            df.index.name = "parameter"
            df.reset_index(inplace=True)
            return df

        def get_text(df):
            summary_dict = {}
            filtered_df = df[df["phase"] == Phase.VORMESSUNG.value]
            summary_dict[Phase.VORMESSUNG.value] = self.get_kennzahlen_stations(
                filtered_df
            )
            text = (
                get_phase_text(
                    summary_dict[Phase.VORMESSUNG.value], Phase.VORMESSUNG.value
                )
                + "\n"
            )
            filtered_df = df[df["phase"] == Phase.BETRIEB.value]
            summary_dict[Phase.BETRIEB.value] = self.get_kennzahlen_stations(
                filtered_df
            )
            text += (
                get_phase_text(summary_dict[Phase.BETRIEB.value], Phase.BETRIEB.value)
                + "\n"
            )
            filtered_df = df[df["phase"] == Phase.NACHMESSUNG.value]
            summary_dict[Phase.NACHMESSUNG.value] = self.get_kennzahlen_stations(
                filtered_df
            )
            text += (
                get_phase_text(
                    summary_dict[Phase.NACHMESSUNG.value], Phase.NACHMESSUNG.value
                )
                + "\n"
            )
            return text, summary_dict

        def get_settings(fields: list):
            settings = {}
            settings["fields"] = fields
            with st.sidebar.expander("⚙️ Settings", expanded=True):
                flds = st.multiselect(
                    "Felder",
                    options=fields,
                    help="Felder, die angezeigt werden sollen. Wenn keine Felder ausgewählt werden, werden alle Felder angezeigt.",
                )
                if len(flds) > 0:
                    settings["fields"] = flds
            return settings

        filters = ["locations", "velocity", "stations", "weekday-weekend", "day-night"]
        self.filtered_data, self.filtered_stations = self.filter_data(filters)
        stats_df = self.get_stats_table(
            self.filtered_data.copy(), ["id_standort", "phase"]
        )
        merged_df = pd.merge(stats_df, self.stations, on="id_standort", how="inner")
        fields = [
            "id_standort",
            "strname",
            "hausnr",
            "geschwind",
            "phase",
            "anz",
            "v_einfahrt_median",
            "v_einfahrt_percentile_85",
            "v_ausfahrt_median",
            "v_ausfahrt_percentile_85",
            "uebertretung_einfahrt_median",
            "uebertretung_ausfahrt_median",
            "uebertretung_einfahrt_percentile_85",
            "uebertretung_ausfahrt_percentile_85",
            "ist_uebertretung_einfahrt_sum",
            "ist_uebertretung_ausfahrt_sum",
            "ist_uebertretung_einfahrt_pct",
            "ist_uebertretung_ausfahrt_pct",
        ]
        merged_df = merged_df[fields]
        el_to_remove = [
            "id_standort",
            "strname",
            "hausnr",
            "geschwind",
            "phase",
        ]
        fields = [x for x in fields if x not in el_to_remove]
        settings = get_settings(fields)

        st.markdown(f"### {len(merged_df['id_standort'].unique())} Standorte")
        tabs = st.tabs(
            [
                "Beschreibung Erwartungen",
                "Auswertung",
                "Beschreibung Resultate",
                "Kennzahlen",
                "Beschreibung Spalten",
            ]
        )
        all_results_dict = {}
        with tabs[0]:
            st.markdown(STAT_TABLE_INFO)
        with tabs[1]:
            st.dataframe(
                merged_df[el_to_remove + settings["fields"]],
                height=600,
                hide_index=True,
            )
        with tabs[2]:
            text, all_results_dict = get_text(merged_df)
            st.markdown(text)
        with tabs[3]:
            st.dataframe(get_summmary_table(all_results_dict), hide_index=True)
        with tabs[4]:
            st.markdown(STAT_COLUMNS_DESCRIPTION)

    def show_map(self):
        def format_marker(df: pd.DataFrame, par: str):
            df["marker_color"] = MARKER_COLOR
            min_size = 3
            max_size = 50
            min_val = df[par].min()
            max_val = df[par].max()
            df["marker_size"] = ((df[par] - min_val) / (max_val - min_val)) * (
                max_size - min_size
            ) + min_size
            return df

        def get_settings(settings: dict):
            with st.sidebar.expander("⚙️ Settings", expanded=True):
                settings["parameter"] = st.selectbox(
                    "Parameter",
                    options=stats_parameter_options.keys(),
                    format_func=lambda x: stats_parameter_options[x],
                    help="Parameter, der auf der Karte mit proportionaler Grösse angezeigt werden soll.",
                )
            return settings

        tooltip_list = [
            {"label": "Standort", "field": "id_standort"},
            {"label": "Strasse", "field": "strname"},
            {"label": "Hausnummer", "field": "hausnr"},
            {"label": "Höchstgeschwindigkeit", "field": "geschwind"},
        ] + [
            {"label": label, "field": parameter}
            for parameter, label in stats_parameter_options.items()
        ]
        settings = {
            "lat": "lat",
            "lon": "lon",
            "zoom": 14,
            "marker_color_col": "marker_color",
            "marker_size_col": "marker_size",
            "tooltip": tooltip_list,
        }
        settings = get_settings(settings)
        filters = [
            "locations",
            "velocity",
            "stations",
            "phase",
            "weekday-weekend",
            "day-night",
        ]
        self.filtered_data, self.filtered_stations = self.filter_data(filters)
        phases = self.filtered_data["phase"].unique()
        aggregation_fields = (
            ["id_standort"] if len(phases) > 1 else ["id_standort", "phase"]
        )
        aggregated_df = self.get_stats_table(
            self.filtered_data.copy(), aggregation_fields
        )
        merged_df = pd.merge(
            aggregated_df, self.stations, on="id_standort", how="inner"
        )
        merged_df = format_marker(merged_df, settings["parameter"])

        fig = get_map(merged_df, settings)
        st.markdown(f"### {len(self.filtered_stations)} Smiley-Standorte")
        st.markdown(
            f"Grösse der Symbole ist proportional zu Parameter ***{settings['parameter']}***."
        )
        folium_static(fig, width=1000, height=800)
        st.download_button(
            label="Download Daten",
            data=merged_df.to_csv(index=False),
            file_name="smiley.csv",
            mime="text/csv",
        )

    def show_station_analysis(self):
        def show_kennzahlen(kennzahlen: pd.DataFrame):
            kennzahlen = pd.concat(
                [kennzahlen, self.get_stats_table(data, ["id_standort", "phase"])]
            )
            if phase == Phase.NACHMESSUNG.value:
                kennzahlen.drop(columns=["id_standort"], inplace=True)
                kennzahlen.columns = [
                    "Phase",
                    "Geschw. Einfahrt (km/h, Median)",
                    "Geschw. Einfahrt (km/h, P85)",
                    "Anzahl Messungen",
                    "Geschw. Ausfahrt (km/h, median)",
                    "Geschw. Ausfahrt (km/h, P85)",
                    "Differenz Ausfahrt-Einfahrt (km/h, Median)",
                    "Differenz Ausfahrt-Einfahrt (km/h, P85)",
                    "Übertretung Einfahrt (km/h, Median)",
                    "Übertretung Einfahrt (km/h, P85)",
                    "Übertretung Ausfahrt (km/h, Median)",
                    "Übertretung Ausfahrt (km/h, P85)",
                    "Anzahl Übertretungen Einfahrt",
                    "Anzahl Übertretungen Ausfahrt",
                    "Prozent Übertretungen Einfahrt",
                    "Prozent Übertretungen Ausfahrt",
                ]
                melted_df = kennzahlen.melt(
                    id_vars=["Phase"], var_name="Kennzahl", value_name="Wert"
                )
                final_df = melted_df.pivot(
                    index="Kennzahl", columns="Phase", values="Wert"
                ).reset_index()
                st.dataframe(final_df, hide_index=True, height=600)
                st.download_button(
                    label="Daten herunterladen",
                    data=final_df.to_csv(index=False),
                    file_name=f"standort_{row['id_standort']}.csv",
                    mime="text/csv",
                )
                st.markdown(
                    "Negative Übertretungsgeschwindigkeiten bedeuten, dass die Geschwindigkeit unter der Höchstgeschwindigkeit liegt."
                )

        def execute_h0_test(data: pd.DataFrame):
            st.markdown(f"#### {phase}")
            mean_einfahrt = data["v_einfahrt"].mean()
            mean_ausfahrt = data["v_ausfahrt"].mean()
            t_stat, p_value, h0_rejected = self.wilcoxon_test(
                data, "v_einfahrt", "v_ausfahrt"
            )
            adj = "höher" if mean_einfahrt < mean_ausfahrt else "tiefer"
            result = "abgelehnt" if h0_rejected else "angenommen"
            result_long = (
                f"ist die Ausfahrtsgeschwindigkeit signifikant {adj}"
                if h0_rejected
                else f"ist die {adj}e Ausfahrtsgeschwindigkeit nicht signifikant."
            )
            st.markdown(
                H0_RESULT_ALL.format(
                    phase, mean_ausfahrt - mean_einfahrt, adj, result, result_long
                )
            )

            data = data[data["v_einfahrt"] > data["geschwindigkeit"]]
            mean_einfahrt = data["v_einfahrt"].mean()
            mean_ausfahrt = data["v_ausfahrt"].mean()
            t_stat, p_value, h0_rejected = self.wilcoxon_test(
                data, "v_einfahrt", "v_ausfahrt"
            )
            expected = (
                H0_RESULT_EXC_EXPECTED1
                if phase == Phase.BETRIEB.value
                else H0_RESULT_EXC_EXPECTED2
            )
            adj = "höher" if mean_einfahrt < mean_ausfahrt else "tiefer"
            result = "abgelehnt" if h0_rejected else "angenommen"
            result_long = (
                f"ist die Ausfahrtsgeschwindigkeit signifikant {adj}"
                if h0_rejected
                else f"ist die {adj}e Ausfahrtsgeschwindigkeit nicht signifikant."
            )
            st.markdown(
                H0_RESULT_EXC.format(
                    expected,
                    mean_ausfahrt - mean_einfahrt,
                    adj,
                    result,
                    result_long,
                )
            )

        filters = [
            "station",
        ]
        self.filtered_data, self.filtered_stations = self.filter_data(filters)
        row = self.filtered_stations.iloc[0]
        title = f"### {row['strname']} {row['hausnr']} (id={row['id_standort']}) Höchstgeschwindigkeit: {row['geschwind']} km/h"
        st.markdown(title)
        tabs = st.tabs(["Plots", "Kennzahlen", "Signifikanztest"])
        kennzahlen = pd.DataFrame()
        for phase in ["Vormessung", "Betrieb", "Nachmessung"]:
            data = self.filtered_data[self.filtered_data["phase"] == phase]
            with tabs[0]:
                st.markdown(f"#### {phase}")
                self.show_plots(data, plot_options, row)
            with tabs[1]:
                show_kennzahlen(kennzahlen)
            with tabs[2]:
                execute_h0_test(data)

    def show_gui(self, sel_menu):
        if sel_menu == 0:
            self.info()
        elif sel_menu == 1:
            self.show_map()
        elif sel_menu == 2:
            self.show_statistics()
        elif sel_menu == 3:
            self.show_phase_comparison()
        elif sel_menu == 4:
            self.show_station_analysis()
