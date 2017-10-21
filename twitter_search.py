from twython import Twython
import json
import os
from auth_keys import *

class TwitterSearch():
    def __init__(self):
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        twitter = Twython(APP_KEY, APP_SECRET)
        self.twitter = twitter


    def run_search(self, search, geo=False, result_type='', count=50, mentions=False):
        try:
            query = '{} exclude:retweets exclude:replies'.format(search)

            if geo:
                search_results = self.twitter.search(q=query, count=count, lang="en", is_quote_status=False, geocode=geo, result_type=result_type)
            else:
                search_results = self.twitter.search(q=query, count=count, lang="en", is_quote_status=False)

            list_data = []
            for tweet in search_results['statuses']:
                data = {
                    "name": tweet["user"]["screen_name"],
                    "text": tweet["text"],
                    "created_at": tweet["created_at"],
                    "favorite_count": tweet["favorite_count"],
                    "retweet_count": tweet["retweet_count"],
                    "location": tweet["user"]["location"],
                }
                list_data.append(data)
            return list_data
        except Exception as e:
            return None
