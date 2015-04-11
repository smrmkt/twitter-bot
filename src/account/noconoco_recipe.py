# -*- coding: utf-8 -*-

import datetime
import json
import os
import random
import sys
import tweepy
import urllib2

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../lib/model')

from account import Account

api_base_url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20121121'
recipe_categories = {
    "ご飯もの": 14,
    "パスタ": 15,
    "麺・粉物料理": 16,
    "汁物・スープ": 17,
    "鍋料理": 23,
    "人気メニュー": 30,
    "定番の肉料理": 31,
    "定番の魚料理": 32,
    "卵料理": 33,
    "今日の献立": 38
}


class NoconocoRecipe:
    def __init__(self, conf_path=None):
        self.__account = Account('noconoco_bot', conf_path)
        self.__application_id = self.__account.conf.get('rakuten_api', 'application_id')

    def get_info(self):
        return self.__account.info()

    def post(self, message, in_reply_to_status_id=None):
        self.__account.post(message, in_reply_to_status_id)

    def get_mentions(self):
        return self.__account.unread_mention()

    def get_reply_message(self, mention):
        location = (mention.text.split(' ')[1]).encode('utf-8')
        return '@' + mention.user.screen_name.encode('utf-8') +\
               ' ' + self.get_recipe_message(location)

    def get_recipe_message(self):
        recipes = self.get_recipe()
        index = random.randint(0, len(recipes['result'])-1)
        indication = unicode.encode(recipes['result'][index]['recipeIndication'], 'utf-8')
        if indication == '指定なし':
            indication = 'てきとうにがんばるん'
        message = '今日のおすすめの献立は「 {0} 」だしー．{1}でできるから，とっても簡単だしー． {2}{3}'.format(
            unicode.encode(recipes['result'][index]['recipeTitle'], 'utf-8'),
            indication,
            unicode.encode(recipes['result'][index]['recipeUrl'], 'utf-8'),
            self.get_datetime()
        )
        return message

    def get_recipe(self):
        category = self.get_recipe_category()
        url = '{0}?applicationId={1}&categoryId={2}'.format(api_base_url, self.__application_id, category)
        res = urllib2.urlopen(url)
        return json.loads(res.read())

    def get_recipe_category(self):
        index = random.randint(0, len(recipe_categories)-1)
        return recipe_categories.items()[index][1]

    def get_datetime(self):
        d = datetime.datetime.today()
        return ' (' + d.strftime("%H:%M:%S") + ')'

class NoconocoRecipeStreamListener(tweepy.StreamListener):
    def __init__(self, api=None, bot=None):
        self.__bot = bot
        self.api = api or tweepy.API()

    def on_status(self, status):
        if self.is_mention(status):
            message = self.__bot.get_reply_message(status)
            self.__bot.post(message, status.id_str)

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzz...'

    def is_mention(self, status):
        try:
            info = self.__bot.get_info()
            tokens = status.text.split(' ')
            if tokens[0] == '@' + info.screen_name:
                return True
            else:
                return False
        except:
            return False

