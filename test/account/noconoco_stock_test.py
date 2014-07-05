# -*- coding: utf-8 -*-

import json
import mock
import os
import sys
import tweepy.models
import unittest

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../../src/account')

from noconoco_stock import NoconocoStock

class NoconocoStockTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_stock_id(self):
        bot = NoconocoStock('/../../../test/conf/api_keys.conf')
        self.assertEqual('7203', bot.get_stock_id('トヨタ'))
        self.assertEqual('6902', bot.get_stock_id('デンソー'))
        self.assertEqual(None, bot.get_stock_id('hoge'))

    def test_get_stock_name(self):
        bot = NoconocoStock('/../../../test/conf/api_keys.conf')
        self.assertEqual('トヨタ自動車(株)', bot.get_stock_name('7203'))
        self.assertEqual('日本電信電話(株)', bot.get_stock_name('9432'))
        self.assertEqual(None, bot.get_stock_id('hoge'))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(NoconocoStockTest))
    return suite