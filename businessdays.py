#!/usr/bin/python3.6
from datetime import date, timedelta as td
from dateutil.parser import parse
import argparse

parser = argparse.ArgumentParser( description="Prints the number of weekdays between two dates. Uses the dateutil library to parse the input. Should be able to accept most standard date formats." )
parser.add_argument( "start", action="store", help="the date to start counting from." )
parser.add_argument( "end", action="store", help="The date to count to." )
parser.add_argument( "-i", "--inverse", action="store_true", help="Perform the inverse action and print the number of weekends" )
args = parser.parse_args()

s = parse( args.start )
e = parse( args.end )
d = int(str(e-s).split(" ")[0])
wd = 0
we = [6,7]
for i in range( 0, d ):
    if not s.isoweekday() in we:
        wd += 1
    s += td( days=1 )
print( wd )
