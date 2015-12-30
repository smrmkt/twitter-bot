#! /usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import datetime
import os
import re
import sys
from time import sleep
import urllib
import tweepy

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../lib/model')

from account import Account

wait_time = 1
search_url = 'http://db.netkeiba.com/?pid=horse_list'
horse_profile_url = 'http://db.netkeiba.com/horse/'

class NoconocoHorseProfile:
    def __init__(self, conf_path=None):
        self.__account = Account('noconoco_bot', conf_path)

    def get_info(self):
        return self.__account.info()

    def post(self, message, in_reply_to_status_id=None):
        self.__account.post(message, in_reply_to_status_id)

    def reply(self, mention):
        message = self.get_wait_message(mention)
        self.__account.post(message, mention.id_str)
        messages = self.get_reply_messages(mention)
        for message in messages:
            self.__account.post(message, mention.id_str)
            sleep(1)

    def get_mentions(self):
        return self.__account.unread_mention()

    def get_reply_message(self, mention):
        reply_to = '@' + mention.user.screen_name.encode('utf-8')
        target = (mention.text.split(' ')[1]).encode('utf-8')
        return '{0} {1}'.format(reply_to, self.get_horse_message(target))

    def get_horse_message(self, target):
        horse_id = self.get_horse_id(target)
        if horse_id == None:
            return '「{0}」なんて名前の馬はいないみたいだしー'. format(target, self.get_datetime())
        else:
            return '「{0}」って馬のデータはこれだよー > {1}/{2}/ {3}'.format(
                target,
                horse_profile_url,
                horse_id,
                self.get_datetime()
            )

    def get_horse_id(self, target):
        url = '{0}&pid=horse_list&word={1}'.format(
            search_url,
            urllib.quote(unicode(target, 'utf-8').encode('euc-jp'))
        )
        res = urllib.urlopen(url)
        soup = BeautifulSoup(res.read().decode('euc-jp'))
        elements = soup.find_all('input', {'name': 'id'})
        if len(elements) != 1:
            return None
        return horse_profile_url, elements[0].get('value')

    def get_datetime(self):
        d = datetime.datetime.today()
        return ' (' + d.strftime("%H:%M:%S") + ')'
