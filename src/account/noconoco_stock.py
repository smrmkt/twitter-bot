# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import datetime
import jsm
from urllib2 import *
import tweepy

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../lib/model')

from account import Account

info_url = 'http://info.finance.yahoo.co.jp/'
stock_url = 'http://stocks.finance.yahoo.co.jp/'

class NoconocoStock:
    def __init__(self, conf_path=None):
        self.__account = Account('noconoco_bot', conf_path)

    def get_info(self):
        return self.__account.info()

    def post(self, message, in_reply_to_status_id=None):
        self.__account.post(message, in_reply_to_status_id)

    def get_mentions(self):
        return self.__account.unread_mention()

    def get_reply_message(self, mention):
        reply_to = '@' + mention.user.screen_name.encode('utf-8')
        target = (mention.text.split(' ')[1]).encode('utf-8')
        stock_id, stock_name = self.get_stock_id_name(target)
        return reply_to + ' ' + self.get_stock_message(stock_id, stock_name)

    def get_stock_message(self, stock_id, stock_name):
        q = jsm.Quotes()
        d = q.get_price(stock_id)
        price = self.get_stock_price(stock_id)
        if d is None or price is None:
            return self.get_error_message(stock_name)
        message = stock_name + '(' + str(stock_id) + ')の株価は' + str(price) + 'だしー\n'\
                  '前日終値は' + str(d.close) + 'で今日の始値は' + str(d.open) +\
                  '，高値は' + str(d.high) + '，安値は' + str(d.low) + 'だしー\n'
        return message + 'そんなことより早くあたしを撫でればいいし' + self.get_datetime()

    def get_stock_id_name(self, target):
        stock_id = self.get_stock_id(target)
        stock_name = self.get_stock_name(target)
        if stock_id is None and stock_name is None:
            return None, None
        elif stock_id is None:
            stock_id = self.get_stock_id(stock_name)
        elif stock_name is None:
            stock_id = int(stock_id)
            stock_name = self.get_stock_name(stock_id)
        return stock_id, stock_name

    def get_stock_price(self, stock_id):
        try:
            url = stock_url + 'stocks/detail/?code=' + str(stock_id)
            soup = BeautifulSoup(urlopen(url))
            res = soup.find_all('td', class_='stoksPrice')
            regex= r'<.+>(.+)<.+>'
            price = re.search(regex, str(res[1])).group(1)
            return int(price.replace(',', ''))
        except:
            return None

    def get_stock_id(self, stock_name):
        try:
            url = info_url + 'search/?query=' + stock_name
            soup = BeautifulSoup(urlopen(url))
            res = soup.find('span', {'class': 'code highlight'})
            regex = r'\[([0-9]+)\]'
            matches = re.search(regex, str(res))
            if matches is not None:
                return int(matches.group(1))
            else:
                return None
        except:
            return None

    def get_stock_name(self, stock_id):
        try:
            url = info_url + 'search/?query=' + str(stock_id)
            soup = BeautifulSoup(urlopen(url))
            title = str(soup.find('title'))
            regex = r'<title>(.+)【[0-9]+】.+</title>'
            return re.search(regex, title).group(1)
        except:
            return None

    def get_error_message(self, target):
        return target + 'とか，そんな銘柄知らないしー' + self.get_datetime()

    def stream_user_timeline(self):
        self.__account.userstream(NoconocoStockStreamListener(bot=self))

    def get_datetime(self):
        d = datetime.datetime.today()
        return ' (' + d.strftime("%H:%M:%S") + ')'

class NoconocoStockStreamListener(tweepy.StreamListener):
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

