# -*- coding: utf-8 -*-

import json
import mock
import unittest

from src.account.noconoco_weather import NoconocoWeather

json_path = 'test/data/weather_api_yokohama.json'

class NoconocoWeatherTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_weather_message(self):
        bot = NoconocoWeather('/../../../test/conf/config.ini')
        bot.get_weather_info = mock.MagicMock()
        bot.get_weather_info.return_value = json.load(open(json_path))
        message = '横浜の天気をお知らせするしー\n' \
                '今日の天気は「曇り」で最高気温はよくわかんないし\n' \
                '明日の天気は「曇り」で最高気温は27度だし\n' \
                'そんなことより早くあたしを撫でればいいし'
        self.assertEqual(bot.get_weather_message('横浜'), message)

    def test_encode_location(self):
        bot = NoconocoWeather('/../../../test/conf/config.ini')
        self.assertEqual('130010', bot.encode_location('東京'))
        self.assertEqual('140010', bot.encode_location('横浜'))
        self.assertRaises(KeyError, bot.encode_location, 0)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(NoconocoWeatherTest))
    return suite