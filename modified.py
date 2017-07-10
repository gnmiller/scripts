#!/usr/bin/python
import argparse
from subprocess import call
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse

parser = argparse.ArgumentParser( description="Uses the system binary find to locate files modified on, before or after a given date. The application will attempt to parse any valid date-string and perform the find for it.\nThe default behavior is to search for files modified on date. The search ignores directories and will only return files.\nNOTE: If is modified at exactly 00:00 on a given date it will NOT be returned in results for that date." )
parser.add_argument( "date", action="store", nargs=1, help="The date to compare modify times against." )
parser.add_argument( "-d", action="store", dest="d", nargs=1, help="Specify a root directory to begin the search from. If not specified '.' is used." )
ex_group = parser.add_mutually_exclusive_group()
ex_group.add_argument( "-b", action="store_true", dest="b", help="Scan for files modified before date." )
ex_group.add_argument( "-a", action="store_true", dest="a", help="Scan for files modified after date." )
args = parser.parse_args()

# set search mode (exact, before, or after)
b = None
if( args.b == True ):
    b = True
if( args.a == True):
    b = False

# check if path was provided
path = None
if( args.d != None ):
    path = args.d[0]
else:
    path = "."

# format date into YYYY-MM-DD
date = parse(args.date[0])
date_str_t = str(date)
date_str = date_str_t[0:10]

# calling find binary
if( b == True ):
    res = call( ["find", "-L", path, "-type", "f", "!", "-newermt", date_str] )
    exit( 0 )
if( b == False):
    res = call( ["find", "-L", path, "-type", "f", "-newermt", date_str] )
    exit( 0 )
if( b == None ):
    # date -> date+1day and formatting
    next_day = date + timedelta(days=1)
    next_day_str_t = str(next_day)
    next_day_str = next_day_str_t[0:10]
    res = call( ["find", "-L", path, "-type", "f", "-newermt", date_str, "!", "-newermt", next_day_str] )
    exit( 0 )
