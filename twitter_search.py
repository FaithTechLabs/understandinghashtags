from twython import Twython
import json
import html
import os
import re
from auth_keys import *
from datetime import datetime, timedelta
from pytz import timezone

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "June",
    "July",
    "Aug",
    "Sept",
    "Oct",
    "Nov",
    "Dec"
]

EMOJI_REGEX = re.compile('\\\\U000\w+')

class TwitterSearch():
    def __init__(self):
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        twitter = Twython(APP_KEY, APP_SECRET)
        self.twitter = twitter
        self.search_results = ""

    def count(self, search, geo=False, result_type='', count=50, mentions=False):
        count = 0
        tz = timezone('EST')
        day = datetime.now() - timedelta(days=1)
        tzoffset = tz.utcoffset(day)
        day = day.replace(tzinfo=tz)
        #day = day.strftime("%Y-%m-%d")
        query = '{} exclude:retweets exclude:replies'.format(search)
        if geo:
            search_results = self.twitter.search(q=query, count=count, lang="en", is_quote_status=False, geocode=geo, result_type=result_type, until=day)
        else:
            search_results = self.twitter.search(q=query, count=count, lang="en", is_quote_status=False, until=day)

        for tweet in search_results['statuses']:
            date = tweet["created_at"]
            date = datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')
            tzoffset = tz.utcoffset(date)
            date = date + tzoffset
            if date >= day:
                count = count + 1

        return count


    def colours(self, search, geo=False, result_type='', count=50, mentions=False):
        count = 0
        #day = day.strftime("%Y-%m-%d")
        colours = {}
        query = '{} exclude:retweets exclude:replies'.format(search)
        if geo:
            search_results = self.twitter.search(q=query, count=count, lang="en", is_quote_status=False, geocode=geo, result_type=result_type)
        else:
            search_results = self.twitter.search(q=query, count=count, lang="en", is_quote_status=False)

        for tweet in search_results['statuses']:
            try:
                colours[tweet["user"]["profile_sidebar_border_color"]] = colours[tweet["user"]["profile_sidebar_border_color"]] + 1
            except:
                colours[tweet["user"]["profile_sidebar_border_color"]] = 1
        return colours

    def run_search(self, search, geo=False, result_type='', count=50, mentions=False):
        query = '{} exclude:retweets exclude:replies'.format(search)

        if geo:
            search_results = self.twitter.search(q=query, count=count, lang="en", is_quote_status=False, geocode=geo, result_type=result_type)
        else:
            search_results = self.twitter.search(q=query, count=count, lang="en", is_quote_status=False)

        self.search_results = search_results
        list_data = []
        for tweet in search_results['statuses']:

            date = tweet["created_at"]
            tz = timezone('EST')
            date = datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')
            tzoffset = tz.utcoffset(date)
            date = date + tzoffset

            data = {
                "name": tweet["user"]["screen_name"],
                "text": tweet["text"],
                "created_at": date,
                "favorite_count": tweet["favorite_count"],
                "retweet_count": tweet["retweet_count"],
                "location": tweet["user"]["location"],
                "date": date.strftime("%b %d"),
                "time": date.strftime("%I:%M %p"),
                "colour": tweet["user"]["profile_sidebar_border_color"]
            }
            list_data.append(data)
        return list_data

    def get_emojis(self):
        data = []
        for tweet in self.search_results['statuses']:
            emojis = EMOJI_REGEX.findall(str(tweet["text"].encode("unicode_escape")))
            if emojis:
                for emoji in emojis:
                    data.append(emoji.encode('utf-8').decode("utf-8"))
        return data
