import streamlit as st
import numpy as np
import pandas as pd
import datetime


def show_districts():

    ds = st.sidebar.selectbox('Выберете район',
                              ("Выбрать",
                               "Залупинский район",
                                'Пупинский район'))
    return ds


def widgets():
    from datetime import datetime
    current_time = datetime.now().time()
    x = st.sidebar.slider('Время', value=current_time)

    return x


def paint_map():
    pass


def paint_district_map():
    pass


def show_state():
    state = st.sidebar.selectbox("Выберете состояние датчиков",
                         ("Выбрать", "Рабочие", "Не корректно", "Не работают"))
    return state


def connect(ds=None, state=None, date=None):
    pass


def show_all_cameras():
    pass


def main():
    [theme]
    primaryColor = "#c855f16"
    backgroundColor = "#091c35"
    secondaryBackgroundColor = "#F0F2F6"
    textColor = "#ffffff"
    font = "sans serif"

    add_selectbox = st.sidebar.selectbox(
        "Выберете что хотите посмотреть",
        ("Выбрать", "Мониторинг оборудования", "Мониторинг загруженности городских дорог",
         "Мониторинг загруженности межрайоных дорог"))
    if add_selectbox == 'Мониторинг оборудования':
        ds = show_districts()
        state = show_state()
        if ds != 'Выбрать' and state != 'Выбрать':
            connect(ds=ds, state=state)
        elif ds == 'Выбрать':
            st.sidebar.title("Выберете район")
        elif state == 'Выбрать':
            st.sidebar.title("Выберете состояние")

    if add_selectbox == "Мониторинг загруженности городских дорог":
        ds = show_districts()
        dt = widgets()
        if ds != 'Выбрать' and dt != 'Выбрать':
            connect(ds=ds, date=dt)
        elif ds == 'Выбрать':
            st.sidebar.title("Выберете район")
        elif dt == 'Выбрать':
            st.sidebar.title("Выберете время")

    if add_selectbox == "Мониторинг загруженности межрайоных дорог":
        pass
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])
    st.map(map_data)


main()


