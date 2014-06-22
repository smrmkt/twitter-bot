# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

sys.path.append('./src/account')
sys.path.append('./test/account')

setup(
    name = 'Twitter-bot',
    version = '0.1',
    description='Twitter bot script test code for travis ci',
    packages = find_packages(),
    test_suite = 'noconoco_weather_test.suite'
)