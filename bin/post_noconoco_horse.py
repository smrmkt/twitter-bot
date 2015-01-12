#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os.path
import argparse

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src/account')

from noconoco_horse import NoconocoHorse

# args
parser = argparse.ArgumentParser(description='post horse info to twitter')
parser.add_argument('menu')
parser.add_argument('owner', nargs='?')

if __name__ == '__main__':
    args = parser.parse_args()
    bot = NoconocoHorse(args.owner)
    if args.menu == 'post':
        bot.post_messages()
