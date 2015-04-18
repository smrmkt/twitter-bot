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
from noconoco_chat import NoconocoChat
from noconoco_horse import NoconocoHorse
from noconoco_recipe import NoconocoRecipe
from noconoco_stock import NoconocoStock
from noconoco_weather import NoconocoWeather


class NoconocoStream:
    def __init__(self, owner='', conf_path=None):
        self.__account = Account('noconoco_bot', conf_path)
        self.__bots = {
            'chat': NoconocoChat(),
            'horse': NoconocoHorse(owner),
            'recipe': NoconocoRecipe(),
            'stock': NoconocoStock(),
            'weather': NoconocoWeather()
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
        if self.is_mention(status) is False:
            return
        try:
            sent_message = (status.text.split(' ')[1]).encode('utf-8')
            bot = NoconocoBotDiscriminator(self.__bots).discriminate(sent_message)
            bot.reply(status)
        except Exception:
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


class NoconocoBotDiscriminator:
    def __init__(self, bots=None):
        self.__bots = bots

    def discriminate(self, sent_message):
        if self._is_for_horse_bot(sent_message):
            return self.__bots['horse']
        elif self._is_for_recipe_bot(sent_message):
            return self.__bots['recipe']
        elif self._is_for_weather_bot(sent_message):
            return self.__bots['weather']
        elif self._is_for_stock_bot(sent_message):
            return self.__bots['stock']
        else:
            return self.__bots['chat']

    def _is_for_weather_bot(self, sent_message):
        if self.__bots['weather'].encode_location(sent_message) is not None:
            return True
        else:
            return False

    def _is_for_stock_bot(self, sent_message):
        if self.__bots['stock'].get_stock_id(sent_message) is not None:
            return True
        elif self.__bots['stock'].get_stock_name(sent_message) is not None:
            return True
        else:
            return False

    def _is_for_horse_bot(self, sent_message):
        if sent_message.find('出走予定') > -1:
            return True
        else:
            return False

    def _is_for_recipe_bot(self, sent_message):
        if sent_message.find('献立') > -1:
            return True
        else:
            return False





