# download link
# https://data.bs.ch/api/explore/v2.1/catalog/datasets/100268/exports/csv?lang=de&timezone=Europe%2FZurich&use_labels=false&delimiter=%3B&select=zyklus,phase,id_standort,messung_datum,messung_zeit,v_einfahrt,v_ausfahrt,v_delta,geschwindigkeit&where=messung_jahr=2023
import streamlit as st
import os
import pandas as pd
from enum import Enum
from scipy import stats

from plots import histogram, boxplot
from texts import INFO
from utils import optimize_dataframe_types

PARQUET_FILE = "./data/100268.parquet"
CSV_FILE = "./data/100268.csv"
CSV_STATIONS_FILE = "./data/100286.csv"
MAX_STATIONS = 10

menu_options = [
    "Über die App",
    "Vergleich Geschw. Einfahrt/Ausfahrt",
]
phase_options = ["Alle", "Vormessung", "Betrieb", "Nachmessung"]
time_options = ["07:00-19:59h", "20:00-06:59h"]
time2_options = dict(zip(range(24), [f"x{x}:00-{x}:59h" for x in range(24)]))
weekday_options = ["Montag-Freitag", "Samstag-Sonntag"]
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
plot_options = ["Histogramm", "Boxplot"]


class Smiley:
    def __init__(self):
        self.data, self.stations = self.get_data()
        self.filtered_stations = pd.DataFrame()
        self.filtered_data = pd.DataFrame()
        self.station_options = dict(
            zip(self.stations["idstandort"], self.stations["strname"])
        )
        self.filtered_data = pd.DataFrame()
        self.filtered_stations = pd.DataFrame()

    def get_stats(self):
        aggregated_df = self.data.groupby(["id_standort", "phase", "zyklus"]).agg(
            {
                "v_einfahrt": [
                    ("median", "median"),
                    ("percentile_85", lambda x: x.quantile(0.85)),
                ],
                "v_ausfahrt": [
                    ("median", "median"),
                    ("percentile_85", lambda x: x.quantile(0.85)),
                ],
            }
        )
        return aggregated_df

    def perform_paired_t_test(data, col_before, col_after):
        # Perform the paired t-test
        t_stat, p_value = stats.ttest_rel(data[col_before], data[col_after])

        # Print the results
        print(f"T-statistic: {t_stat}")
        print(f"P-value: {p_value}")

        # Interpret the p-value
        alpha = 0.05
        if p_value < alpha:
            print("Reject the null hypothesis - suggest the means are different")
        else:
            print(
                "Fail to reject the null hypothesis - suggest the means are not different"
            )

    def filter_data(self, keys: list):
        filtered_data = self.data
        filtered_stations = self.stations

        with st.sidebar.expander("🔎 Filter", expanded=True):
            # station filters
            if "velocity" in keys:
                sel_velocity = st.selectbox(
                    label="Gechwindigkeit",
                    options=velocity_options.keys(),
                    format_func=lambda x: velocity_options[x],
                )
                if sel_velocity > 0:
                    filtered_stations = filtered_stations[
                        filtered_stations["geschwind"] == sel_velocity
                    ]
            if "stations" in keys:
                sel_stations = st.multiselect(
                    "Stationen",
                    options=self.station_options.keys(),
                    format_func=lambda x: self.station_options[x],
                )
                if sel_stations:
                    filtered_stations = self.stations[
                        self.stations["idstandort"].isin(sel_stations)
                    ]
            if len(filtered_stations) < len(self.stations):
                filtered_data = self.data[
                    self.data["id_standort"].isin(
                        filtered_stations["idstandort"].unique()
                    )
                ]
            # measurement filters
            if "phase" in keys:
                sel_phase = st.selectbox("Phase", phase_options)
                if phase_options.index(sel_phase) > 0:
                    filtered_data = filtered_data[
                        self.filtered_data["phase"] == sel_phase
                    ]

        return filtered_data, filtered_stations

    def get_data(self):
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
                data.to_parquet(PARQUET_FILE)
        data = pd.read_parquet(PARQUET_FILE)
        # memory = data.memory_usage(deep=True).sum()
        # print(f"Memory usage: {memory / 1024 ** 2:.2f} MB")

        stations = pd.read_csv(CSV_STATIONS_FILE, sep=";")
        stations_with_data = data["id_standort"].unique()
        stations = stations[stations["idstandort"].isin(stations_with_data)]
        return data, stations

    def get_settings(self, keys: list):
        settings = {}
        with st.sidebar.expander("⚙️ Settings", expanded=True):
            if "plots" in keys:
                for plot in plot_options:
                    settings[plot] = st.checkbox(plot, value=True)
        return settings

    def show_phase_comparison(self):
        filters = ["locations", "velocity", "stations", "phase", "weekday", "day-time"]
        self.filtered_data, self.filtered_stations = self.filter_data(filters)
        settings = self.get_settings(["plots"])
        
        for station in list(self.filtered_stations["idstandort"])[:MAX_STATIONS + 1]:
            st_name = self.stations[self.stations["idstandort"] == station].iloc[0]
            st.markdown(
                f"{st_name['strname']} {st_name['hausnr']} (id={st_name['idstandort']}) Höchstgeschwindigkeit: {st_name['geschwind']} km/h"
            )
            data = self.filtered_data[self.filtered_data["id_standort"] == station]
            melted_df = pd.melt(
                data[["id_standort", "v_einfahrt", "v_ausfahrt"]],
                id_vars=["id_standort"],
                var_name="parameter",
                value_name="value",
            )
            if settings[plot_options[0]] and settings[plot_options[1]]:
                cols = st.columns(2)
                with cols[0]:
                    plot_settings = {"x": "v_einfahrt"}
                    chart = histogram(melted_df, plot_settings)
                    st.plotly_chart(
                        chart,
                        use_container_width=True,
                        sharing="streamlit",
                        theme="streamlit",
                    )

                with cols[1]:
                    plot_settings = {"title": "Vergleich Einfahrt/Ausfahrt"}
                    chart = boxplot(melted_df, plot_settings)
                    st.plotly_chart(
                        chart,
                        use_container_width=True,
                        sharing="streamlit",
                        theme="streamlit",
                    )
            if len(self.filtered_stations) > MAX_STATIONS:
                st.markdown(
                    f"Es werden nur die ersten {MAX_STATIONS} Stationen angezeigt. Bitte filtern Sie die Daten, um die Anzahl Stationen zu reduzieren."
                )
    def info(self):
        st.image("./assets/splash.jpg", width=1000)
        st.markdown(INFO, unsafe_allow_html=True)

    def show_gui(self):
        st.sidebar.title("smiley-app-bs 😃 😐 🤬")
        sel_menu = st.sidebar.selectbox("Analyse", menu_options)
        if menu_options.index(sel_menu) == 0:
            self.info()
        if menu_options.index(sel_menu) == 1:
            self.show_phase_comparison()
