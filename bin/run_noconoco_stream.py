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

if __name__ == '__main__':
    bot = NoconocoStream()
    bot.stream_user_timeline()