# -*- coding: utf-8 -*-

import json
import mock
import unittest

from src.account.noconoco_weather import NoconocoWeather

class NoconocoWeatherTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_weather_message(self):
        bot = NoconocoWeather('横浜')
        bot.get_weather_info = mock.MagicMock()
        bot.get_weather_info.return_value = json.load(open('weather_api_yokohama.json'))
        message = '横浜の天気をお知らせするしー\n' \
                '今日の天気は「曇り」で最高気温はよくわかんないし\n' \
                '明日の天気は「曇り」で最高気温は27度だし\n' \
                'そんなことより早くあたしを撫でればいいし'
        self.assertEqual(bot.get_weather_message(), message)
