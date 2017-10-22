from twython import Twython
import json
import os
from auth_keys import *
from datetime import datetime

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
                # Sun Oct 22 01:12:40 +0000 2017
                date = tweet["created_at"]
                date = datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')
                print(type(date))
                print(type(date.month))
                month = MONTHS[date.month - 1]
                day = date.day
                year = date.year
                hour = date.hour
                minutes = date.minute
                ampm = 'am'
                if hour == 0:
                    hour = 12
                elif hour > 12:
                    hour = hour - 12
                    ampm = 'pm'
                # dateString = '' + month + ' ' + day + ', ' + year
                # timeString = hour + ':' + minutes + ampm
                data = {
                    "name": tweet["user"]["screen_name"],
                    "text": tweet["text"],
                    "created_at": tweet["created_at"],
                    "favorite_count": tweet["favorite_count"],
                    "retweet_count": tweet["retweet_count"],
                    "location": tweet["user"]["location"],
                    # "date": dateString,
                    # "time": timeString
                    # Date values
                    "day": day,
                    "month": month,
                    "year": year,
                    # Time values
                    "hour": hour,
                    "minutes": minutes,
                    "ampm": ampm
                }
                list_data.append(data)
            return list_data
        except Exception as e:
            return None
