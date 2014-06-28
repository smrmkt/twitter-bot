# -*- coding: utf-8 -*-

import sys
import os.path
import argparse

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src/account')

from noconoco_weather import NoconocoWeather

# args
parser = argparse.ArgumentParser(description='post weathercast to twitter')
parser.add_argument('menu')
parser.add_argument('location', nargs='?')

if __name__ == '__main__':
    args = parser.parse_args()
    bot = NoconocoWeather()
    if args.menu == 'post':
        message = bot.get_weather_message(args.location)
        bot.post(message)
    elif args.menu == 'reply':
        mentions = bot.get_mentions()
        for mention in mentions:
            message = bot.get_reply_message(mention)
            bot.post(message, mention.id_str)