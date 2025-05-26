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
        page_title="Astro Info",
        page_icon="✨☀️",
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

    
    # Prepare main object for position display
    observer = Master()
    # Place it to default coordinates
    observer.move_head_location(int(latitude), int(longitude))
    # 3 - act if any button pressed
    if compute:
        # refresh place according to the dialog
        observer.move_head_location(int(latitude), int(longitude))
        selected = observe[observe['selected'] == True]['planet'].tolist()
        observer.move_head_direction(*selected)
        observer.frame_the_time()  # relative to now before to deconstruct the actual input
        st.dataframe(observer.time["frame"])
        st.line_chart(observer.time["frame"], x="date_time")
    else:
        st.info(f"{lang['date_actual']}: {current_time} --- {lang['longitude']}: {latitude} / {lang['latitude']}: {longitude}")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2]) # ratios
        with col1:
            st.image("./image/sun4.png")
        with col2:
            st.markdown("# [Sun example](https://svs.gsfc.nasa.gov/5048)")
            st.markdown("- Distance:")
            st.markdown("- Ra/Dec")
            st.markdown("- Lon/lat")
            st.markdown("- Angle")
        col3, col4 = st.columns([1, 2]) # ratios
        with col3:
            st.image("./image/sun1.png")
        with col4:
            st.markdown("# [Moon example](https://svs.gsfc.nasa.gov/5048)")
            st.markdown("- Phase")
            st.markdown("- Distance")
            st.markdown("- Ra/Dec")
            st.markdown("- Lon/lat")
            st.markdown("- Angle")
        

if __name__ == "__main__":
    main()
