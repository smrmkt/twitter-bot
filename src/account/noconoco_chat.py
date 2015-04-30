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

goodbye_phrases = [
    'じゃあね',
    'じゃね',
    'じゃあの',
    'またね',
    'さよなら',
    'さようなら',
    'おしまい',
    'お終い',
    'おわり',
    '終わり',
    'バイバイ'
]
goodbye_message_limit = 10

class NoconocoChat:
    def __init__(self, conf_path=None):
        self.__account = Account('noconoco_bot', conf_path)
        self.__api_key = self.__account.conf.get('noconoco_chat', 'docomo_api_key')
        self.__context_expire_seconds = self.__account.conf.get('noconoco_chat', 'context_expire_seconds')
        self.__context = ''
        self.__mode = ''
        self.__last_replied = datetime.datetime(1970, 1, 1)

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
        if self.is_goodbye(mention):
            response = 'またねー {0}'.format(self.get_datetime())
        else:
            response = self.get_chat_message(mention)
        return '@{0} {1}'.format(
            mention.user.screen_name.encode('utf-8'),
            response.encode('utf-8'))

    def get_chat_message(self, mention=None):
        url = '{0}?{1}={2}'.format(api_base_url, 'APIKEY', self.__api_key)
        data = self.get_request_data(mention)
        header = {'Content-Type': 'application/json'}
        try:
            req = urllib2.Request(url, data, header)
            res = urllib2.urlopen(req)
            dic = json.loads(res.read())
            if 'context' in dic:
                self.__context = dic['context']
            if 'mode' in dic:
                self.__mode = dic['mode']
            self.__last_replied = datetime.datetime.now()
            return dic['utt']
        except urllib2.HTTPError, e:
            print e
            return '意味わかんないしー {0}'.format(self.get_datetime())

    def get_request_data(self, mention):
        data = {}
        if mention is not None:
            data['utt'] = (mention.text.split(' ')[1]).encode('utf-8')
            data['nickname'] = mention.user.name.encode('utf-8')
        diff = datetime.datetime.now() - self.__last_replied
        if diff.total_seconds() > self.__context_expire_seconds:
            data['context'] = self.__context
            data['mode'] = self.__mode
        return json.dumps(data)

    def is_goodbye(self, mention):
        sent_message = (mention.text.split(' ')[1]).encode('utf-8')
        if len(sent_message) > goodbye_message_limit:
            return False
        for phrase in goodbye_phrases:
            if sent_message.find(phrase) > -1:
                return True
        return False

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

