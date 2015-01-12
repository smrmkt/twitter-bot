# -*- coding: utf-8 -*-

import datetime
import os
import sys
import tweepy

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path)
sys.path.append(script_path + '/../lib/model')

from account import Account
from noconoco_horse import NoconocoHorse
from noconoco_stock import NoconocoStock
from noconoco_weather import NoconocoWeather
from time import sleep

class NoconocoStream:
    def __init__(self, owner='', conf_path=None):
        self.__account = Account('noconoco_bot', conf_path)
        self.__bots = {
            'stock': NoconocoStock(),
            'weather': NoconocoWeather(),
            'horse': NoconocoHorse(owner)
        }

    def get_info(self):
        return self.__account.info()

    def post(self, message, in_reply_to_status_id=None):
        self.__account.post(message, in_reply_to_status_id)

    def get_mentions(self):
        return self.__account.unread_mention()

    def stream_user_timeline(self):
        self.__account.userstream(
            NoconocoStreamListener(account=self, bots=self.__bots))

    def get_error_message(self, target):
        return target + 'とか，そんな言葉知らないしー' + self.get_datetime()

    def get_datetime(self):
        d = datetime.datetime.today()
        return ' (' + d.strftime("%H:%M:%S") + ')'

class NoconocoStreamListener(tweepy.StreamListener):
    def __init__(self, api=None, account=None, bots=None):
        self.api = api or tweepy.API()
        self.__account = account
        self.__bots = bots

    def on_status(self, status):
        if self.is_mention(status):
            weather_bot = self.__bots['weather']
            stock_bot = self.__bots['stock']
            horse_bot = self.__bots['horse']
            try:
                reply_to = '@' + status.user.screen_name.encode('utf-8')
                target = (status.text.split(' ')[1]).encode('utf-8')
                if weather_bot.encode_location(target) is not None:
                    message = weather_bot.get_reply_message(status)
                    self.__account.post(message, status.id_str)
                elif stock_bot.get_stock_id(target) is not None or \
                     stock_bot.get_stock_name(target) is not None:
                    message = stock_bot.get_reply_message(status)
                    self.__account.post(message, status.id_str)
                elif target.find('出走予定') > -1:
                    message = horse_bot.get_wait_message(status)
                    self.__account.post(message, status.id_str)
                    messages = horse_bot.get_reply_messages(status)
                    for message in messages:
                        self.__account.post(message, status.id_str)
                        sleep(1)
                else:
                    message = reply_to + ' ' + self.__account.get_error_message(target)
                    self.__account.post(message, status.id_str)
            except:
                message = self.__account.get_error_message('？？？')
                self.__account.post(message, status.id_str)


    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzz...'

    def is_mention(self, status):
        try:
            info = self.__account.get_info()
            tokens = status.text.split(' ')
            print info.screen_name
            print tokens
            print tokens[0]
            if tokens[0] == '@' + info.screen_name:
                return True
            else:
                return False
        except:
            return False

