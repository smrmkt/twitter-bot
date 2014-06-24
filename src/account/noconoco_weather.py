# -*- coding: utf-8 -*-

import json
import os
import urllib2
import sys

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../lib/model')

from account import Account

location_path = 'src/data/livedoor_weather_api.txt'

class NoconocoWeather:
    def __init__(self, location, conf_path=None):
        lines = open(location_path).readlines()
        self.__locations = {k:v for k,v in [line.strip().split(',') for line in lines]}
        self.__account = Account('noconoco-weather', conf_path)
        self.__location = self.encode_location(location)

    def get_info(self):
        return self.__account.info()

    def post(self, message):
        self.__account.post(message)

    def get_weather_message(self):
        info = self.get_weather_info()
        message = (info['location']['city']).encode('utf-8') + 'の天気をお知らせするしー\n'
        for i in range(0, 2):
            date = (info['forecasts'][i]['dateLabel']).encode('utf-8')
            weather = (info['forecasts'][i]['telop']).encode('utf-8')
            temp = info['forecasts'][i]['temperature']['max']
            if temp is not None:
                temp = (temp['celsius']).encode('utf-8') + '度だ'
            else:
                temp = 'よくわかんない'
            message = message + date + 'の天気は「' + weather + '」で最高気温は' + temp + 'し\n'
        return message + 'そんなことより早くあたしを撫でればいいし'

    def get_weather_info(self):
        # yokohama
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' % self.__location
        res = urllib2.urlopen(url)
        return json.loads(res.read())

    def encode_location(self, location):
        if location in self.__locations:
            return self.__locations[location]
        else:
            raise KeyError