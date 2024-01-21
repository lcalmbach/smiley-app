import streamlit as st
from streamlit_option_menu import option_menu
from smiley import Smiley


__version__ = "0.0.7"
__author__ = "Lukas Calmbach"
__author_email__ = "lcalmbach@gmail.com"
VERSION_DATE = "2023-21-01"
APP_NAME = "smiley-app"
GIT_REPO = "https://github.com/lcalmbach/smiley-app"
SOURCE_URL = "https://data.bs.ch/explore/dataset/100268"

menu_options = [
    "Über die App",
    "Karten",
    "Statistken",
    "Vergleich Ein-/Ausfahrt",
    "Analyse Standort",
]

# https://icons.getbootstrap.com/?q=image
menu_icons = ["house", "map", "table", "graph-up", "geo"]

APP_INFO = f"""<div style="background-color:#34282C; padding: 10px;border-radius: 15px; border:solid 1px white;">
    <small>App von <a href="mailto:{__author_email__}">{__author__}</a><br>
    Version: {__version__} ({VERSION_DATE})<br>
    Quelle: <a href="{SOURCE_URL}">data.bs</a><br>
    <a href="{GIT_REPO}">git-repo</a></small></div>
    """


def get_info(last_date):
    text = f"""<div style="background-color:#34282C; padding: 10px;border-radius: 15px; border:solid 1px white;">
    <small>App von <a href="mailto:{__author_email__}">{__author__}</a><br>
    Version: {__version__} ({VERSION_DATE})<br>
    Quelle: <a href="{SOURCE_URL}">Stadt Zürich Open Data/EWZ</a><br>
    Daten bis: {last_date.strftime('%d.%m.%Y %H:%M')}
    <br><a href="{GIT_REPO}">git-repo</a></small></div>
    """
    return text


def init():
    st.set_page_config(
        page_title="smiley-app-bs",
        page_icon="😃",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def main():
    init()
    if not ("smiley" in st.session_state):
        st.session_state.smiley = Smiley()
    with st.sidebar:
        st.sidebar.title("smiley-app-bs 😃 🤬")
        menu_action = option_menu(
            None,
            menu_options,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
        )
    index = menu_options.index(menu_action)
    st.session_state.smiley.show_gui(index)
    st.sidebar.markdown(APP_INFO, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
