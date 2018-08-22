#!/usr/bin/env python3
# light weight script to pull dates out of a specific user's tweets
# goal was to push dates from a "schedule" tweet out to gcal but has been abandoned

# init environment
import sys, os
env_name = "drd-schedule"
path = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.insert( 0, "{}/{}".format( path, env_name ) )

# imports
import json, datetime, tweepy, pytz
from dateutil import parser

# settings
path = os.path.dirname(os.path.realpath(__file__))
with open( path+'/settings.json' ) as f:
    settings = json.load( f )

__MY_TZ = settings["app"]["tz"]
__THEIR_TZ = "America/Los_Angeles"
__USER = settings["app"]["user"]

config = { "consumer_key":settings["twitter"]["consumer_key"],
        "consumer_secret":settings["twitter"]["consumer_secret"], 
        "access_token_key":settings["twitter"]["access_token"], 
        "access_token_secret":settings["twitter"]["access_token_secret"] 
        }
auth = tweepy.OAuthHandler( config["consumer_key"], config["consumer_secret"] )
auth.set_access_token( config["access_token_key"], config["access_token_secret"] )

t = tweepy.API( auth )

res = t.user_timeline( __USER, count=20 )
week = { "Monday":"", "Tuesday":"", "Wednesday":"", "Thursday":"", "Friday":"" }
tweet_txt = []
for s in res:
    if "stream schedule" in s.text.lower():
        tweet_txt = s.text.split( "\n" )
print( tweet_txt )

def __localized( d, tz ):
    """Parse a string into a TZ aware datetime. TZ in string is ingored and set to tz"""
    if type( d ) is not type( datetime.datetime.now() ):
        __d = parser.parse( d )
    else:
        __d = d
    timezone = pytz.timezone( tz )
    return timezone.localize( __d )

def __adjust_date( d ):
    """If the date is next weeks, slide it back to this weeks"""
    n = datetime.datetime.now()
    n = __localized( n, __MY_TZ )
    n = n + datetime.timedelta( days=(7-n.isoweekday()) )
    if d > n and d.date != n.date:
        d = d - datetime.timedelta( days=7 )
    return d

for d in tweet_txt:
    if "mon" in d.lower():
        week["Monday"] = __adjust_date(__localized( d, __THEIR_TZ ))
    elif "tue" in d.lower():
        week["Tuesday"] = __adjust_date(__localized( d, __THEIR_TZ ))
    elif "wed" in d.lower():
        week["Wednesday"] = __adjust_date(__localized( d, __THEIR_TZ ))
    elif "thu" in d.lower():
        week["Thursday"] = __adjust_date(__localized( d, __THEIR_TZ ))
    elif "fri" in d.lower():
        week["Friday"] = __adjust_date(__localized( d[:d.find("PDT")], __THEIR_TZ ))
    else:
        continue
for d in week:
    print( "{} :: {}".format( d, week[d] ))
