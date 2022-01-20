#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 13:02:13 2021

@author: victoriaz
"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from open_weather_api import OpenWeather
from city_GIS import City,GIS

states_as_list = GIS.get_us_states()
countries_as_list = GIS.get_countries()

# setup app with stylesheets
app = dash.Dash(__name__)  # , external_stylesheets=[dbc.themes.COSMO])

# Create map template
mapbox_access_token = \
    'pk.eyJ1IjoiYW5hbWluaSIsImEiOiJja2htbGEwdHcwcWZ3MzVvOTR1amNhajM5In0.tmieTIAQdfvwE4m_WUXuCQ'

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=25, r=25, b=25, t=25),
    hovermode='closest',
    title='Weather Map',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        zoom=1,
    ),
)

controls = dbc.Form(
    dbc.Row(
        [
            dbc.Label("Country", width="auto"),
            dbc.Col(
                dcc.Dropdown(
                    options=[{'label': col, 'value': col} for col in countries_as_list],
                    value='',
                    id='country-list',
                    disabled=False
                ),
                className='me-3'
            ),
            dbc.Label("US State", width="auto"),
            dbc.Col(
                dcc.Dropdown(
                    options=[{'label': col, 'value': col} for col in states_as_list],
                    value='',
                    id='state-list',
                    disabled=False
                ),
                className='me-3'
            ),
        ],
        className="g-2",
    )
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H2(), md=3),
                dbc.Col(
                    html.H2('Open Weather Data', className='text-white'), md=9
                )
            ], align='center', className='bg-info'),
        dbc.Row(
            [
                dbc.Col(controls, align='start', md=3),
                dbc.Col(dcc.Graph(id='map'), align='start', md=9),
            ], align='center', className='bg-info',
        ),
    ],
    id='main-container',
    style={'display': 'flex', 'flex-direction': 'column'},
    fluid=True
)


@app.callback(Output('map', 'figure'),
              Input('country-list', 'value'),
              Input('state-list', 'value'),
              State('map', 'relayoutData'))
def make_map(chosen_country, chosen_state, map_layout):
    # get appropriate city weather stations for either a US state or a country
    if chosen_country == 'US' or chosen_country == '' and chosen_state != '':
        city_list_dict = GIS.get_cities_by_us_state(chosen_state)
    else:
        city_list_dict = GIS.get_cities_by_country(chosen_country)

    open_weather = OpenWeather()
    api_total_count, count = 10, 0
    traces = []
    for city in city_list_dict.values():
        count += 1
        temperature = 0 if count > api_total_count \
            else open_weather.execute(str(city.id))
        trace = dict(
            name=city.name,
            type='scattermapbox',
            lon=[city.longitude],
            lat=[city.latitude],
            showlegend=False,
            color=[temperature],
            size=10,
            visible=True,
        )
        traces.append(trace)

    display = dict(data=traces, layout=layout)
    return display


if __name__ == '__main__':
    app.run_server(debug=True)
