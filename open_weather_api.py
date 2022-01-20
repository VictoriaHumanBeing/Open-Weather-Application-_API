#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 12:25:18 2021
Victoria
"""

import json
import requests


class OpenWeather():
    """
    documentation = https://openweathermap.org/current
    """
    endpoint_template = 'http://api.openweathermap.org/data/2.5/' + \
                        'weather?id={city name}&appid={API key}&mode={mode}&units={units}'
    api_key = 'Using your API'

    def __init__(self):
        self.endpoint = OpenWeather.endpoint_template.replace('{API key}', OpenWeather.api_key)

    def execute(self, city, mode='json', units='imperial'):
        endpoint = self.endpoint.replace('{city name}', city)
        endpoint = endpoint.replace('{mode}', mode)
        endpoint = endpoint.replace('{units}', units)

        r = requests.get(endpoint)
        if mode == 'json':
            r_as_json = json.loads(r.text)
            # print(json.dumps(r_as_json, indent=2))
            return r_as_json['main']['temp']
        elif mode == 'xml':
            pass
        elif mode == 'html':
            pass
        else:
            print(r.text)


def main():
    open_weather = OpenWeather()
    temp = open_weather.execute('4347392')

    print(temp)


if __name__ == '__main__':
    main()
