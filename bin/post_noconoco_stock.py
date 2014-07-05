# -*- coding: utf-8 -*-

import sys
import os.path
import argparse

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src/account')

from noconoco_stock import NoconocoStock

# args
parser = argparse.ArgumentParser(description='post stock info to twitter')
parser.add_argument('menu')
parser.add_argument('stock', nargs='?')

if __name__ == '__main__':
    args = parser.parse_args()
    bot = NoconocoStock()
    if args.menu == 'post':
        stock_id, stock_name = bot.get_stock_id_name(args.stock)
        message = bot.get_stock_message(stock_id, stock_name)
        bot.post(message)
    elif args.menu == 'reply':
        mentions = bot.get_mentions()
        for mention in mentions:
            message = bot.get_reply_message(mention)
            bot.post(message, mention.id_str)
    elif args.menu == 'stream':
        bot.stream_user_timeline()