# -*- coding: utf-8 -*-

import ConfigParser
import os
import twitter

class Account:
    def __init__(self, screen_name):
        # set user screen name
        self.__screen_name = screen_name

        # initialize API
        conf = ConfigParser.SafeConfigParser()
        conf.read(os.path.dirname(__file__) + '/../../conf/config.ini')
        self.__api = twitter.Api(
            consumer_key=conf.get(screen_name, 'consumer_key'),
            consumer_secret=conf.get(screen_name, 'consumer_secret'),
            access_token_key=conf.get(screen_name, 'access_token_key'),
            access_token_secret=conf.get(screen_name, 'access_token_secret')
        )

    def info(self):
        return self.__api.GetUser(screen_name=self.__screen_name)

    def tl(self):
        return self.__api.GetUserTimeline(self.__screen_name)

    def post(self, message):
        self.__api.PostUpdate(message)
