# -*- coding: utf-8 -*-

import ConfigParser
import os
import tweepy

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'

class Account:
    def __init__(self, screen_name, conf_path=None, mention_path=None):
        # set user screen name
        self.__screen_name = screen_name
        self.__conf_path = '/../../conf/api_keys.conf'
        if conf_path is not None:
            self.__conf_path = conf_path
        self.__backup_dir = script_path + '/../../backup/' + screen_name
        self.__mention_path = self.__backup_dir + 'last_mention.bak'
        if mention_path is not None:
            self.__mention_path = mention_path

        # initialize python-twitter api
        conf = ConfigParser.SafeConfigParser()
        conf.read(os.path.dirname(__file__) + self.__conf_path)
        auth = tweepy.OAuthHandler(
            conf.get(screen_name, 'consumer_key'),
            conf.get(screen_name, 'consumer_secret'))
        auth.set_access_token(
            conf.get(screen_name, 'access_token_key'),
            conf.get(screen_name, 'access_token_secret'))
        self.__api = tweepy.API(auth)

    def info(self):
        return self.__api.get_user(screen_name=self.__screen_name)

    def tl(self):
        return self.__api.user_timeline(self.__screen_name)

    def post(self, message, in_reply_to_status_id=None):
        if in_reply_to_status_id is None:
            self.__api.update_status(message)
        else:
            self.__api.update_status(message, in_reply_to_status_id)

    def mention(self):
        return self.__api.mentions_timeline()

    def unread_mention(self):
        last_mention = 0
        if os.path.isfile(self.__mention_path):
            last_mention = int(open(self.__mention_path).read().strip())
        elif not os.path.isdir(self.__backup_dir):
            os.mkdir(self.__backup_dir)
        mentions = self.__api.mentions_timeline(since_id=last_mention)
        if len(mentions) > 0:
            last_mention = mentions[-1].id
            with open(self.__mention_path, 'w') as f:
               f.write(str(last_mention))
        return mentions
