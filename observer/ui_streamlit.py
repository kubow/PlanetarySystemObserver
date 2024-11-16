from context import Master, now, loc_df, planets_df
# from current import Observation, Almanac
# from visual import figure_3d
# from project import Subject
import streamlit as st
from settings import change_language


def main():
    # 1 - initial setting
    lang = change_language(default="cz")
    current_time = now()
    # 2 - set page layout
    st.set_page_config(
        page_title="Astro visualization application",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    sidebar_cont = {
        "position": st.sidebar.container(),
        "timespan": st.sidebar.container(),
        "confirm": st.sidebar.container(),
    }

    with sidebar_cont["position"]:
        with st.expander(lang["position"]):
            latitude = st.number_input(lang["latitude"], min_value=float(-90), max_value=float(90), value=50.08804)
            longitude = st.number_input(lang["longitude"], min_value=float(-180), max_value=float(180), value=14.42076)
            st.map(loc_df(lat=latitude, lon=longitude), color='color')
            # TODO: place picker in editable mode
    with sidebar_cont["timespan"]:
        with st.expander(lang["timespan"]):
            date1 = st.date_input(lang["date_from"], value=current_time)
            date2 = st.date_input(lang["date_to"], value=current_time)
            # TODO: granularity
    with sidebar_cont["confirm"]:
        with st.form(key="confirmation"):
            observe = st.data_editor(
                planets_df(),
                column_config={
                    "planet": st.column_config.CheckboxColumn(
                        "Planet",
                        help="Select **planets** to compute",
                        default=False,
                    )
                },
                disabled=["planets"],
                hide_index=True,
            )
            compute = st.form_submit_button(lang["run"])

    # 3 - act if any button pressed
    if compute:
        observer = Master()
        observer.move_head_location(int(latitude), int(longitude))
        selected = observe[observe['selected'] == True]['planet'].tolist()
        observer.move_head_direction(*selected)
        observer.frame_the_time()  # relative to now before to deconstruct the actual input
        st.dataframe(observer.time["frame"])
        st.line_chart(observer.time["frame"], x="date_time")
    else:
        st.write(f"{lang['longitude']}: {latitude} / {lang['latitude']}: {longitude}")


if __name__ == "__main__":
    main()
