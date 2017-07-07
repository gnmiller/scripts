#!/usr/bin/python
import sys
import argparse
import random
import numpy as np
from datetime import datetime as dt

random.seed(dt.now())

parser = argparse.ArgumentParser( description="Simple application to roll a n 6-sided dice m times. By default 1 die is rolled 1 time." )
parser.add_argument( '-n', action='store', dest='n', nargs=1, metavar='dice', default=1, help="Number of dice to roll." )
parser.add_argument( '-m', action='store', dest='m', nargs=1, metavar='iterations', default=1, help="Number of times to roll the dice." )
parser.add_argument( '-d', action='store', dest='d', nargs=1, metavar='sides', default=6, help="Number of sides per die." )
parser.add_argument( '-v', action='store_true', dest='v', help="Print additional information after rolling dice such as std_dev, mean, mode, etc" )
parser.add_argument( '-q', action='store_true', dest='q', help="Print only the results as an unordered list. Specifying -v disables -q." )

args = parser.parse_args()
n = int(args.n[0])
m = int(args.m[0])
d = int(args.d[0])
if( args.v == True ):
    verbose = True
else:
    verbose = False;
if( args.q == True ):
    quiet = True
else:
    quiet = False
if( verbose ):
    quiet = False

out = []
if not( quiet ):
    if( m == 1 ):
        print( "Rolling "+str(n)+" "+str(d)+"-sided die "+str(m)+" time(s)." )
    else:
        print( "Rolling "+str(n)+" "+str(d)+"-sided dice "+str(m)+" time(s)." )

for i in range( m ):
    t = []
    for j in range( n ):
        t.append( random.randrange( d ) + 1 ) #returns [0,d) we want [1,d]
    if( verbose ):
        print( '=' * 30 )
        print( "ROLL SET "+str(i+1)+" RESULTS" )
        print( '=' * 30 )
    count = 0
    for val in t:
        count = count+1
        if not( quiet ):
            print( str(count)+". "+str(val) )
    out.append( t )

if( verbose ):
    print( '=' * 30 )
    print( "FINAL RESULTS" )

occur = []
for i in range( d ):
    occur.append( 0 )
master = []
for i in out:
    for j in i:
        occur[j-1] += 1
        master.append( j )

if( verbose ):
    print( '=' * 30 )
    print( "MEAN:    "+str(np.mean( master )) )
    print( "STD_DEV: "+str(np.std( master )) )
    print( "AVG:     "+str(np.average( master )) )

if not( quiet):
    print( '=' * 30 )
    print( "Full result set:" )
print( master )

total = n*m
if( verbose ):
    print( '=' * 30 )
    print( "Occurence Statistics:" )
    for i in range( d ):
        print( str(i+1)+": "+str(occur[i])+" times ("+str((occur[i]/total)*100)+"%)" )
    print( "Total: "+str(total) )
