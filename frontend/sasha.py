import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, date, time
import random
import warnings
import folium

warnings.filterwarnings('ignore')
data_detectors = pd.read_csv('detectors.csv')
device_edges = pd.read_csv('device_edges.csv')
edges_info = pd.read_csv('edges_info.csv')

df = device_edges[device_edges['device_type_id'] == 0]['edge_id']
data_edge = edges_info.loc[np.intersect1d(edges_info.index, df.index)][['edge_id','to_node_id','from_node_id']]


def sign_utilis(utilisation):
    if (utilisation<=.3):
        return 'green'
    if (utilisation<=.6):
        return 'orange'
    else:
        return 'red'

df_detectors = data_detectors.loc[np.intersect1d(data_detectors.index, df.index)]
time = data_detectors['time'][9]
colors = df_detectors[df_detectors['time']==time]['utilisation'].apply(sign_utilis)
index_colors = colors.index

df_detectors = data_detectors.loc[np.intersect1d(data_detectors.index, df.index)]
data_other = df_detectors[df_detectors['time']==time][['occ', 'speed', 'volume']]

place_name = "Москва, Россия"
graph = ox.graph_from_place(place_name, network_type='drive')

def parse_nodes(nodes):
    dict_major = {}
    node_id = 0
    for i in range(len(graph.nodes.keys())):
        dict_xy = {}
        node_id = nodes[i][0]
        dict_xy.update({'y': nodes[i][1].get('y'), 'x' : nodes[i][1].get('x')})
        dict_major.update({node_id:dict_xy})
    return dict_major

dict_nodes = parse_nodes(nodes)
index = data_edge.index

points = data_edge[['from_node_id', 'to_node_id']]


X, Y, col, occ, dia = [], [], [], [], []
j=0
for i in range(data_edge.shape[0]):
    X+=[dict_nodes.get(points['from_node_id'][index[i]]).get('x')]
    X+=[dict_nodes.get(points['to_node_id'][index[i]]).get('x')]
    Y+=[dict_nodes.get(points['from_node_id'][index[i]]).get('y')]
    Y+=[dict_nodes.get(points['to_node_id'][index[i]]).get('y')]
    if (index_colors[j]==index[i]) and (j<763):
        col+=3*[colors[index_colors[j]]]
        occ+=3*[data_other['occ'][index_colors[j]]]
#         occ+=[data_other['speed'][index_colors[j]]]
#         occ += [data_other['volume'][index_colors[j]]]
#         dia+= 3*[1]
        j+=1
    else:
        col+=3*['black']
        occ+=3*[None]
#         dia+=3*[None]
    X+=[None]
    Y+=[None]
Y = pd.Series(Y,name='lat')
X = pd.Series(X, name='lon')
col = pd.Series(col, name='colors')
# occ = pd.Series(occ, name='occ')
# speed = pd.Series(speed,name='speed')
# volume=pd.Series(volume, name='volume')
# info = pd.Series(info, name='info')
data = pd.concat([Y,X], axis=1)
other = pd.Series(occ, name='info')

m = folium.Map(location=[45.5236, -122.6750])
ox.plot_graph_folium(graph,m)


fig = px.line_mapbox(lat=data['lat'], lon=data['lon'],color=col,text=occ,
                     mapbox_style="open-street-map", zoom=1)





