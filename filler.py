#!/usr/bin/python
import argparse
import sys
import os.path

parser = argparse.ArgumentParser( description="Fill a file with n integers [0-n). A line break will be written at the end of the file." )
parser.add_argument( 'num', action='store', nargs=1, help='Max integer to generate.' )
parser.add_argument( '-n', action='store', dest='lb', nargs='?', default=80, help='How many characters to insert before inserting a line break.' )
parser.add_argument( '-o', action='store', dest='output', nargs='?', default='stdout', help='Specify an output file instead of stdout. The file will be truncated.' )
parser.add_argument( '-c',  action='store', dest='comma', nargs='?', default='', help='Specify a delimiter.' )
args = parser.parse_args()
lim = int(args.num[0])
try:
    dlim
except NameError:
    dlim = ','
if type( args.lb ) is not int:
    lb = int(args.lb)
else:
    lb = args.lb
if( args.output == 'stdout' ):
    outfile = sys.stdout
else:
    outfile = open( args.output, 'w+' )
c = 0
for i in range( lim ):
    c += len( str( i ) )
    if( i == lim-1 ):
        outfile.write( str(i)+'\n' )
        break
    outfile.write( str(i)+dlim )
    if( c%lb == 0 ):
        outfile.write( '\n' )
