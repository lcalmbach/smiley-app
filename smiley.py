# download link
# https://data.bs.ch/api/explore/v2.1/catalog/datasets/100268/exports/csv?lang=de&timezone=Europe%2FZurich&use_labels=false&delimiter=%3B&select=zyklus,phase,id_standort,messung_datum,messung_zeit,v_einfahrt,v_ausfahrt,v_delta,geschwindigkeit&where=messung_jahr=2023
import streamlit as st
import os
import numpy as np
import pandas as pd
from enum import Enum
from scipy import stats

from plots import histogram, boxplot, scatter
from texts import INFO, STAT_TEXT
from utils import optimize_dataframe_types

PARQUET_FILE = "./data/100268.parquet"
CSV_FILE = "./data/100268.csv"
CSV_STATIONS_FILE = "./data/100286.csv"
MAX_STATIONS = 20

menu_options = ["Über die App", "Vergleich Geschw. Einfahrt/Ausfahrt", "Statistiken"]
phase_options = ["Betrieb", "Vormessung", "Nachmessung"]
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
plot_options = ["Histogramm", "Boxplot", "XY"]


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

    def perform_paired_t_test(self, data, col_before, col_after):
        st.write(col_before, col_after, data.head(500))
        # Perform the paired t-test
        t_stat, p_value = stats.ttest_rel(data[col_before], data[col_after])

        # Interpret the p-value
        alpha = 0.05
        h0_rejected = p_value < alpha
        return t_stat, p_value, h0_rejected

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
                sel_phase = st.selectbox("Phase", phase_options)
                filtered_data = filtered_data[filtered_data["phase"] == sel_phase]

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
                data["phase"] = data["phase"].astype("category")
                data.to_parquet(PARQUET_FILE)
        data = pd.read_parquet(PARQUET_FILE)
        # memory = data.memory_usage(deep=True).sum()
        # print(f"Memory usage: {memory / 1024 ** 2:.2f} MB")

        stations = pd.read_csv(CSV_STATIONS_FILE, sep=";")
        stations.rename(columns={"idstandort": "id_standort"}, inplace=True)
        stations_with_data = data["id_standort"].unique()
        stations = stations[stations["id_standort"].isin(stations_with_data)]
        return data, stations

    def get_chart(self, df, melted_df: pd.DataFrame, plot: str):
        chart = None
        plot_settings = {"x": "v_einfahrt"}
        if plot == plot_options[0]:
            chart = histogram(melted_df, plot_settings)
        elif plot == plot_options[1]:
            chart = boxplot(melted_df, plot_settings)
        elif plot == plot_options[2]:
            plot_settings = {
                "x": "v_einfahrt",
                "y": "v_ausfahrt",
                "x_title": "V Einfahrt (km/h)",
                "y_title": "V Ausfahrt (km/h))",
            }
            chart = scatter(df, plot_settings)
        return chart

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
                if "plots" in keys:
                    for plot in plot_options:
                        settings[plot] = st.checkbox(plot, value=True)
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
        plots = [x for x in plot_options if settings[x]]

        for station in list(self.filtered_stations["id_standort"])[: MAX_STATIONS + 1]:
            data = self.filtered_data[self.filtered_data["id_standort"] == station]
            melted_df = pd.melt(
                data[["id_standort", "v_einfahrt", "v_ausfahrt"]],
                id_vars=["id_standort"],
                var_name="parameter",
                value_name="value",
            )
            st_name = self.stations[self.stations["id_standort"] == station].iloc[0]
            st.markdown(
                f"{st_name['strname']} {st_name['hausnr']} (id={st_name['id_standort']}) Höchstgeschwindigkeit: {st_name['geschwind']} km/h, {len(data)} Messungen."
            )
            col_index = 0
            cols = st.columns(2 if len(plots) > 1 else 1)
            for plot in plots:
                with cols[col_index]:
                    chart = self.get_chart(data, melted_df, plot)
                    st.plotly_chart(
                        chart,
                        use_container_width=True,
                        sharing="streamlit",
                        theme="streamlit",
                    )
                    col_index = 0 if col_index == 1 else 1

        if len(self.filtered_stations) > MAX_STATIONS:
            st.markdown(
                f"Es werden nur die ersten {MAX_STATIONS} Stationen angezeigt. Bitte filtern Sie die Daten, um die Anzahl Stationen zu reduzieren."
            )

    def info(self):
        st.image("./assets/splash.jpg", width=1000)
        st.markdown(INFO, unsafe_allow_html=True)

    def show_statistics(self):
        def get_text(merged_df):
                betrieb_df = merged_df[merged_df['phase'] == 'Betrieb']
                num_tot = merged_df['anz'].sum()
                num_stations = len(betrieb_df['id_standort'].unique())
                num_reduction_exceedance = len(betrieb_df[betrieb_df['uebertretung_ausfahrt_median'] < betrieb_df['uebertretung_einfahrt_median']])

                text = STAT_TEXT.format(num_tot, num_reduction_exceedance, num_stations, -99, -999)
                return text
        
        def get_settings(fields: list):
            settings = {}
            settings['fields'] = fields
            with st.sidebar.expander("⚙️ Settings", expanded=True):
                flds = st.multiselect("Felder", options=fields, help="Felder, die angezeigt werden sollen. Wenn keine Felder ausgewählt werden, werden alle Felder angezeigt.")
                if len(flds) > 0:
                    settings['fields'] = flds
            return settings

        def get_stats():
            df = self.filtered_data.copy()
            df.drop(columns=["zyklus"], inplace=True)
            df["diff_einfahrt_ausfahrt"] = df["v_einfahrt"] - df["v_ausfahrt"]
            df["uebertretung_einfahrt"] = df["v_einfahrt"] - df["geschwindigkeit"]
            df["uebertretung_ausfahrt"] = df["v_ausfahrt"] - df["geschwindigkeit"]
            df['ist_uebertretung_einfahrt'] = np.where(df['v_einfahrt'] > df['geschwindigkeit'], 1, 0)
            df['ist_uebertretung_ausfahrt'] = np.where(df['v_ausfahrt'] > df['geschwindigkeit'], 1, 0)

            aggregated_df = df.groupby(["id_standort", "phase"]).agg(
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
            aggregated_df['ist_uebertretung_einfahrt_pct'] = aggregated_df['ist_uebertretung_einfahrt_sum'] / aggregated_df['anz'] * 100
            aggregated_df['ist_uebertretung_ausfahrt_pct'] = aggregated_df['ist_uebertretung_ausfahrt_sum'] / aggregated_df['anz'] * 100
            aggregated_df.reset_index(inplace=True)

            return aggregated_df

        filters = ["locations", "velocity", "stations", "weekday-weekend", "day-night"]
        self.filtered_data, self.filtered_stations = self.filter_data(filters)
        stats_df = get_stats()
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
        st.dataframe(merged_df[el_to_remove + settings['fields']], height=600)
        text = get_text(merged_df)
        st.markdown(text)

    def show_gui(self):
        st.sidebar.title("smiley-app-bs 😃 😐 🤬")
        sel_menu = st.sidebar.selectbox("Analyse", menu_options)
        if menu_options.index(sel_menu) == 0:
            self.info()
        elif menu_options.index(sel_menu) == 1:
            self.show_phase_comparison()
        elif menu_options.index(sel_menu) == 2:
            self.show_statistics()
