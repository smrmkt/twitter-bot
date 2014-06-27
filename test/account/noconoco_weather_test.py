# -*- coding: utf-8 -*-

import json
import mock
import twitter
import unittest

from src.account.noconoco_weather import NoconocoWeather

weather_api_path = 'test/data/weather_api_yokohama.json'
mention_path = 'test/data/noconoco_weather_mention.json'
default_message = '横浜の天気をお知らせするしー\n' \
                  '今日の天気は「曇り」で最高気温はよくわかんないし\n' \
                  '明日の天気は「曇り」で最高気温は27度だし\n' \
                  'そんなことより早くあたしを撫でればいいし'

class NoconocoWeatherTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_weather_message(self):
        bot = NoconocoWeather('/../../../test/conf/api_keys.conf')
        bot.get_weather_info = mock.MagicMock()
        bot.get_weather_info.return_value = json.load(open(weather_api_path))
        self.assertEqual(bot.get_weather_message('横浜'), default_message)

    def test_get_reply_message(self):
        bot = NoconocoWeather('/../../../test/conf/api_keys.conf')
        bot.get_weather_info = mock.MagicMock()
        bot.get_weather_info.return_value = json.load(open(weather_api_path))
        data = json.loads(open(mention_path).read())
        mention = twitter.Status.NewFromJsonDict(data)
        message = '@hoge ' + default_message
        self.assertEqual(bot.get_reply_message(mention), message)

    def test_encode_location(self):
        bot = NoconocoWeather('/../../../test/conf/api_keys.conf')
        self.assertEqual('130010', bot.encode_location('東京'))
        self.assertEqual('140010', bot.encode_location('横浜'))
        self.assertRaises(KeyError, bot.encode_location, 0)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(NoconocoWeatherTest))
    return suite