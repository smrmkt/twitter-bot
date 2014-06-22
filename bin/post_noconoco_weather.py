# -*- coding: utf-8 -*-

import sys
import os.path
import argparse

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src/account')

from src.account.noconoco_weather import NoconocoWeather

# args
parser = argparse.ArgumentParser(description='post weathercast to twitter')
parser.add_argument('location', nargs='?', default='横浜')

if __name__ == '__main__':
    args = parser.parse_args()
    bot = NoconocoWeather(args.location)
    bot.post(bot.get_weather_message())
