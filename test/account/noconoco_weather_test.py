# -*- coding: utf-8 -*-

import json
import mock
import tweepy.models
import unittest

from src.account.noconoco_weather import NoconocoWeather

weather_api_path = 'test/data/weather_api_yokohama.json'
default_message = '横浜の天気をお知らせするしー\n' \
                  '今日の天気は「曇り」で最高気温はよくわかんないし\n' \
                  '明日の天気は「曇り」で最高気温は27度だし\n' \
                  'そんなことより早くあたしを撫でればいいし posted at 22:30:00'
error_message = 'hogeとか，そんな場所知らないしー posted at 22:30:00'

class NoconocoWeatherTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_user(self, text, id_str, screen_name):
        user = tweepy.models.User()
        user.screen_name = screen_name
        mention = tweepy.models.Status()
        mention.text = text.decode('utf-8')
        mention.id_str = id_str
        mention.user = user
        return mention

    def test_get_weather_message(self):
        bot = NoconocoWeather('/../../../test/conf/api_keys.conf')
        bot.get_weather_info = mock.MagicMock()
        bot.get_weather_info.return_value = json.load(open(weather_api_path))
        bot.get_datetime = mock.MagicMock()
        bot.get_datetime.return_value = ' posted at 22:30:00'
        self.assertEqual(bot.get_weather_message('横浜'), default_message)
        self.assertEqual(bot.get_weather_message('hoge'), error_message)

    def test_get_reply_message(self):
        # setup
        bot = NoconocoWeather('/../../../test/conf/api_keys.conf')
        bot.get_weather_info = mock.MagicMock()
        bot.get_weather_info.return_value = json.load(open(weather_api_path))
        bot.get_datetime = mock.MagicMock()
        bot.get_datetime.return_value = ' posted at 22:30:00'
        # valid location '横浜'
        mention = self.create_user('@noco_weather 横浜', '421810126546812930', 'hoge')
        message = '@hoge ' + default_message
        self.assertEqual(bot.get_reply_message(mention), message)
        # # invalid location 'hoge'
        mention = self.create_user('@noco_weather hoge', '421810126546812930', 'hoge')
        message = '@hoge ' + error_message
        self.assertEqual(bot.get_reply_message(mention), message)

    def test_encode_location(self):
        bot = NoconocoWeather('/../../../test/conf/api_keys.conf')
        self.assertEqual('016010', bot.encode_location('札幌'))
        self.assertEqual('130010', bot.encode_location('東京'))
        self.assertEqual('140010', bot.encode_location('横浜'))
        self.assertEqual(None, bot.encode_location(0))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(NoconocoWeatherTest))
    return suite