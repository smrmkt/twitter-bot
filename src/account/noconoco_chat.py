# -*- coding: utf-8 -*-

import datetime
import json
import os
import sys
import tweepy
import urllib2

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../lib/model')

from account import Account

api_base_url = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue'

class NoconocoChat:
    def __init__(self, conf_path=None):
        self.__account = Account('noconoco_bot', conf_path)
        self.__api_key = self.__account.conf.get('docomo_api', 'api_key')
        self.__context = None

    def get_info(self):
        return self.__account.info()

    def post(self, message, in_reply_to_status_id=None):
        self.__account.post(message, in_reply_to_status_id)

    def reply(self, mention):
        message = self.get_reply_message(mention)
        self.__account.post(message, mention.id_str)

    def get_mentions(self):
        return self.__account.unread_mention()

    def get_reply_message(self, mention):
        response = self.get_chat_message(mention)
        return '@{0} {1}'.format(
            mention.user.screen_name.encode('utf-8'),
            unicode.encode(response))

    def get_chat_message(self, mention=None):
        url = '{0}?{1}={2}'.format(api_base_url, 'APIKEY', self.__api_key)
        data = self.get_request_data(mention)
        header = {'Content-Type': 'application/json'}
        try:
            req = urllib2.Request(url, data, header)
            res = urllib2.urlopen(req)
            dic = json.loads(res.read())
            return dic['utt']
        except urllib2.HTTPError, e:
            return '意味わかんないしー {0}'.format(self.get_datetime())

    def get_request_data(self, mention):
        data = {}
        if mention is not None:
            data['utt'] = (mention.text.split(' ')[1]).encode('utf-8')
            data['nickname'] = mention.user.name.encode('utf-8')
        if self.__context is not None:
            data['context'] = self.__context
        return json.dumps(data)

    def get_datetime(self):
        d = datetime.datetime.today()
        return ' (' + d.strftime("%H:%M:%S") + ')'


class NoconocoChatStreamListener(tweepy.StreamListener):
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

