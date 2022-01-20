#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 12:48:17 2021

@author: Victoria
"""
import json

class City:

    def __init__(self, id, name, state, country, longitude, latitude):
        self.id = id
        self.name = name
        self.state = state
        self.country = country
        self.longitude = float(longitude)
        self.latitude = float(latitude)

    def __str__(self):
        return f'{self.id}:{self.name}:{self.state}:{self.country}:{self.longitude}:{self.latitude}'

class GIS:
    city_list_filename = 'city.list.json'

    f = open(city_list_filename, encoding='UTF-8')
    cities = json.load(f)
    f.close()

    @classmethod
    def get_countries(cls):
        countries = list()
        for c in cls.cities:
            if c['country'] not in countries and c['country'] != '':
                countries.append(c['country'])
        return countries

    @classmethod
    def get_cities_by_country(cls, country):
        city_list_as_dict = dict()
        for c in cls.cities:
            if c['country'] == country:
                city = City(c['id'], c['name'], c['state'], c['country'],
                            c['coord']['lon'], c['coord']['lat'])
                city_list_as_dict[city.name] = city
        return city_list_as_dict

    @classmethod
    def get_us_states(cls):
        states = list()
        for c in cls.cities:
            if c['country'] == 'US' and c['state'] not in states and c['state'] != '':
                states.append(c['state'])
        return states

    @classmethod
    def get_cities_by_us_state(cls, state):
        city_list_as_dict = dict()
        for c in cls.cities:
            if c['country'] == 'US' and c['state'] == state:
                city = City(c['id'], c['name'], c['state'], c['country'],
                            c['coord']['lon'], c['coord']['lat'])
                city_list_as_dict[city.name] = city
        return city_list_as_dict