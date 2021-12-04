import streamlit as st
import numpy as np
import pandas as pd
import datetime


def show_districts():

    fh = st.sidebar.selectbox('Выберете район',
        ('Выбрать',
         "Залупинский район",
         'Пупинский район')
                              )


def widgets():
    from datetime import datetime
    current_time = datetime.now().time()
    x = st.sidebar.slider('Время', value=current_time)


def paint_map():
    pass


def paint_district_map():
    pass


def show_state():
    state = st.sidebar.selectbox("Выберете состояние датчиков",
                         ("Выбрать", "Рабочие", "Порой дают сбой", "Не работают"))


def show_all_cameras():
    pass


def main():

    add_selectbox = st.sidebar.selectbox(
        "Выберете что хотите посмотреть",
        ("Выбрать", "Мониторинг оборудования", "Мониторинг загруженности городских дорог",
         "Мониторинг загруженности межрайоных дорог"))
    if add_selectbox == 'Мониторинг оборудования':
        show_districts()
        show_state()

    if add_selectbox == "Мониторинг загруженности городских дорог":
        show_districts()
        widgets()

    if add_selectbox == "Мониторинг загруженности межрайоных дорог":
        pass
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])
    st.map(map_data)

main()


