import psycopg2.extras
import pandas as pd
import plotly.express as px
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date, time
import random
from pathlib import Path

DATA_DIR = Path('.').absolute() / 'frontend' / 'data'
ETL_DIR = DATA_DIR / 'etl'
data_detectors = pd.read_csv(ETL_DIR / 'detectors.csv.gz')
data_detectors.id = data_detectors.id.astype(str)

device_edges = pd.read_csv(ETL_DIR /'device_edges.csv.gz')
device_edges.device_id = device_edges.device_id.astype(str)

edges = pd.read_csv(ETL_DIR / 'edges.csv.gz')
nodes = pd.read_csv(ETL_DIR / 'nodes.csv.gz')[['node_id', 'lat', 'lon']]

place_name = "Москва, Россия"
# graph = ox.graph_from_place(place_name, network_type='drive')


def valya(time_from, time_to):

    df = device_edges[device_edges['device_type_id'] == 0]['edge_id']
    data_edge = edges.loc[np.intersect1d(edges.index, df.index)][['edge_id', 'to_node_id', 'from_node_id']]

    def sign_utilis(utilisation_):
        if (utilisation_<=.3):
            return 'green'
        elif (utilisation_<=.7):
            return 'orange'
        else:
            return 'red'

    df_detectors = data_detectors.loc[np.intersect1d(data_detectors.index, df.index)]
    df_detectors = df_detectors[df_detectors['time'] >= time_from]
    df_detectors = df_detectors[df_detectors['time'] <= time_to]

    utilisation = np.random.sample(data_edge.shape[0])
    utilisation = pd.Series(utilisation, name='utilisation', index=data_edge.index)

    data_edge_ = pd.concat([data_edge, utilisation], axis=1)
    data_edge_['utilisation_color'] = data_edge_['utilisation'].apply(sign_utilis)



    points = data_edge_

    tmp = points.merge(nodes, left_on="from_node_id", right_on="node_id", suffixes=('', '_from'), )

    tmp['lat_from'] = tmp['lat']
    tmp['lon_from'] = tmp['lon']
    tmp.drop('node_id', axis=1, inplace=True)

    tmp = tmp.merge(nodes, left_on="to_node_id", right_on="node_id", suffixes=('', '_to'), )
    tmp.drop(['node_id', 'lat', 'lon'], axis=1, inplace=True)
    lines = tmp

    X, Y, col, utilisation_tmp, edge_id = [], [], [], [], []

    for i, row in lines.iterrows():
        edge_id += [row['edge_id']]
        edge_id += [row['edge_id']]
        edge_id += [0]

        X += [row['lat_from']]
        X += [row['lat_to']]

        Y += [row['lon_from']]
        Y += [row['lon_to']]

        X += [None]
        Y += [None]

        if row['utilisation_color']:
            utilisation_tmp += 3 * [row['utilisation']]
            col += 3 * [row['utilisation_color']]
        else:
            utilisation_tmp += 3 * [row['utilisation']]
            col += 3 * ['black']

    Y = pd.Series(Y, name='lon')
    X = pd.Series(X, name='lat')
    col = pd.Series(col, name='color')
    edge_series = pd.Series(edge_id, name='edge_id', dtype=int)
    utilisation_series = pd.Series(utilisation_tmp, name='utilisation', dtype=float)
    data = pd.concat([Y, X, utilisation_series], axis=1)

    fig = px.line_mapbox(data, lat='lat', lon='lon',
                         color=col,
                         hover_name='utilisation',
                         mapbox_style="open-street-map",
                         width=1000,
                         height=800)

    fig.update_layout(showlegend=False)
    fig.show()
    return fig

