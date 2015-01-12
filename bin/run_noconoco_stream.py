# -*- coding: utf-8 -*-

import sys
import os.path
import argparse

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src/account')

from noconoco_stream import NoconocoStream

# args
parser = argparse.ArgumentParser(description='run noconoco bot stream')
parser.add_argument('owner', nargs='?', default='社台レースホース')

if __name__ == '__main__':
    args = parser.parse_args()
    bot = NoconocoStream(args.owner)
    bot.stream_user_timeline()