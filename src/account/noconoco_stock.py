# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import datetime
import jsm
from lxml import html
from urllib2 import *
import tweepy

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../lib/model')

from account import Account

base_url = 'http://info.finance.yahoo.co.jp/'

class NoconocoStock:
    def __init__(self, conf_path=None):
        self.__account = Account('noco_stock', conf_path)

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
        message = stock_name + 'の株価は' + str(d.close) + 'だしー\n'\
                  '直近営業日の初値は' + str(d.open) + '，高値は' + str(d.high) +\
                  '，安値は' + str(d.low) + '，出来高は' + str(d.volume) + 'だしー\n'
        return message + 'そんなことより早くあたしを撫でればいいし' + self.get_datetime()

    def get_stock_id_name(self, target):
        stock_id = self.get_stock_id(target)
        stock_name = self.get_stock_name(target)
        if stock_id is None and stock_name is None:
            return None, None
        elif stock_id is None:
            stock_id = int(target)
        elif stock_name is None:
            stock_id = int(stock_id)
            stock_name = target
        return stock_id, stock_name

    def get_stock_id(self, name):
        try:
            url = base_url + 'search/?query=' + name
            dom = html.fromstring(urlopen(url).read())
            el = dom.get_element_by_id('tbodyPortfolio')
            text = el[0][0].text_content()
            return re.findall(r'[0-9]+', text)[0]
        except:
            return None

    def get_stock_name(self, id):
        try:
            url = base_url + 'search/?query=' + id
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
        info = self.__bot.get_info()
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

