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
target_list_url = 'http://db.netkeiba.com/?pid=horse_list'
sports_navi_url = 'http://keiba.yahoo.co.jp'
kanas = ['a', 'k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w']

class NoconocoHorse:
    def __init__(self, owner, conf_path=None):
        self.__account = Account('noconoco_bot', conf_path)
        self.__targets = self.get_target_list(owner)

    def get_info(self):
        return self.__account.info()

    def post(self, message, in_reply_to_status_id=None):
        self.__account.post(message, in_reply_to_status_id)

    def get_mentions(self):
        return self.__account.unread_mention()

    def get_wait_message(self, mention):
        reply_to = '@{0} '.format(mention.user.screen_name.encode('utf-8'))
        return '{0} 調べるからちょっと待ってて欲しいのー{1}'.format(
            reply_to,
            self.get_datetime()
        )

    def get_reply_messages(self, mention):
        reply_to = '@{0} '.format(mention.user.screen_name.encode('utf-8'))
        return self.create_messages(reply_to)

    def post_messages(self):
        for message in self.create_messages():
            self.post(message)
            sleep(wait_time)

    def create_messages(self, reply_to=''):
        messages = []
        for starter, day in self.get_starters().items():
            message = '{0}よくわかんないけど，{1}のレースに{2}が出走するみたいだしー{3}'.format(
                reply_to,
                day,
                str(starter.encode('utf-8')),
                self.get_datetime(),
            )
            messages.append(message)
        return messages

    def get_target_list(self, owner, n_of_list=100):
        url = '{0}&owner={1}&list={2}'.format(
            target_list_url,
            urllib.quote(unicode(owner, 'utf-8').encode('euc-jp')),
            n_of_list
        )
        res = urllib.urlopen(url)
        soup = BeautifulSoup(res.read().decode('euc-jp'))
        return [e.text for e in soup.find_all('td', {'class': 'bml txt_l'})]

    def get_race_days(self):
        res = urllib.urlopen(sports_navi_url)
        soup = BeautifulSoup(res.read())
        race_days = {}
        for day in soup.find_all('td', {'class': 'fntS txC'}):
            for link in day.find_all('a'):
                path = link.get('href')
                if 'horse' in path:
                    day = re.search(r'[0-9]+', path).group()
                    day = '{0}月{1}日'.format(day[4:6], day[6:8])
                    race_days[day] = link.get('href')
        return race_days

    def get_starters(self):
        starters = {}
        for day, path in self.get_race_days().items():
            for kana in kanas:
                url = '{0}{1}&kana={2}'.format(
                    sports_navi_url,
                    path,
                    kana
                )
                res = urllib.urlopen(url)
                soup = BeautifulSoup(res.read())
                horses = [e.text for e in soup.find_all('a') if '/directory/horse/' in e.get('href')]
                targets = [t for t in self.__targets if t in horses]
                for t in targets:
                    starters[t] = day
                sleep(wait_time)
        return starters

    def get_datetime(self):
        d = datetime.datetime.today()
        return ' (' + d.strftime("%H:%M:%S") + ')'
