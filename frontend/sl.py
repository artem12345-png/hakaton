import streamlit as st
import numpy as np
import pandas as pd
import datetime
from db import all_regions, get_region
from test_map import show_all_camers


def show_districts():

    ds = st.sidebar.selectbox('Выберете район',
                              [*all_regions()])
    r = get_region(ds)
    return r


def widgets():
    from datetime import datetime

    time_to = '2021-11-29 18:30:00.000000'

    date_time_obj = datetime.strptime(time_to, '%Y-%m-%d %H:%M:%S.%f')
    x = st.sidebar.slider('Время', value=date_time_obj.time())

    return x


def paint_map():
    pass


def paint_district_map():
    pass


def all_cameras(ds):
    r = show_all_camers(int(ds))
    st.plotly_chart(r)


def main():

    add_selectbox = st.sidebar.selectbox(
        "Выберете что хотите посмотреть",
        ("Выбрать", "Мониторинг оборудования", "Мониторинг загруженности городских дорог"))
    if add_selectbox == 'Выбрать':
        pass

    if add_selectbox == 'Мониторинг оборудования':
        ds = show_districts()
        all_cameras(ds)

    if add_selectbox == "Мониторинг загруженности городских дорог":
        ds = show_districts()
        dt = widgets()
        from data import valya
        time_from = '2021-11-29 18:00:00.000000'
        time_to = '2021-11-29 18:30:00.000000'
        st.plotly_chart(valya(time_from, time_to))


main()


