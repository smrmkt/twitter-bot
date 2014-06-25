# -*- coding: utf-8 -*-

import ConfigParser
import os
import twitter
# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'

mention_path = script_path + '/../../backup/last_mention.bak'

class Account:
    def __init__(self, screen_name, conf_path=None):
        # set user screen name
        self.__screen_name = screen_name
        self.__conf_path = '/../../conf/api_keys.conf'

        # initialize API
        conf = ConfigParser.SafeConfigParser()
        if conf_path != None:
            conf.read(os.path.dirname(__file__) + conf_path)
        else:
            conf.read(os.path.dirname(__file__) + self.__conf_path)
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

    def mention(self):
        return self.__api.GetMentions()

    def unread_mention(self):
        last_mention = 0
        if os.path.exists(mention_path):
            last_mention = int(open(mention_path).read().strip())
        mentions = self.__api.GetMentions(since_id=last_mention)
        if len(mentions) > 0:
            last_mention = mentions[-1].id
            with open(mention_path, 'w') as f:
               f.write(str(last_mention))
        return mentions

    def reply(self, message, in_reply_to_user_id):
        self.__api.PostUpdate(message, in_reply_to_user_id)