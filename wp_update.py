#!/bin/python3
import argparse, pymysql
from tabulate import tabulate
from getpass import getpass

# default values
def_db="wordpress"
def_host="localhost"
def_user="wordpress"
def_prefix="wp_"

# getting args...
parser = argparse.ArgumentParser( description="Attempt to auto-update a wordpress database to use new URI." )
parser.add_argument( "-d", "--db_name", dest="db", metavar="database", default=def_db, help="The database to modify. Default value: {}".format( def_db ) )
parser.add_argument( "-u", "--user", dest="user", metavar="username", default=def_user, help="The username to login to mysql with. Default value: {}".format( def_user ) )
parser.add_argument( "-p", "--passwd", dest="passwd", metavar="password", help="The user's passwordto login to mysql with. Will be prompted if not supplied." )
parser.add_argument( "-g", "--host", dest="host", metavar="hostname", default=def_host, help="The hostname of the server running mysql. Default value: {}".format( def_host ) )
parser.add_argument( "-t", "--pfix", dest="prefix", metavar="db prefix", default=def_prefix, help="The table prefix used by WordPress. Default value: {}".format( def_prefix ) )
parser.add_argument( "uri", metavar="new-URL", help="The new URI to set the WordPress instance to. http:// Will be auto pre-prended if http:// or https:// are not included. Trailing slashes, eg http://example.com/ will be stripped." )
parser.add_argument( "-y", "--auto", dest="auto", action="store_true", default=False, help="Perform the change in non-interactive mode. If not specified you will be prompted before any changes are applied to the database." )
args = parser.parse_args()
#--------#

# fixing up args
if args.passwd == None:
    no_pass = True
else:
    no_pass = False

if not ( "http://" in args.uri or "https://" in args.uri ):
    temp = "http://{}".format( args.uri )
    args.uri = temp
while args.uri[len(args.uri)-1] == '/':
    args.uri = args.uri[:len(args.uri)-1]

if no_pass:
    passwd = getpass( "Please input the password for {}: ".format( args.user ) )
else:
    passwd = args.passwd
while no_pass:
    if len( passwd ) > 0:
        no_pass = False
    if no_pass:
        passwd = getpass( "Invalid length. Try again.\n" )
#--------#

conn = pymysql.connect( host=args.host, 
                        user=args.user, 
                        password=passwd, 
                        db=args.db, 
                        charset="utf8mb4",
                        cursorclass=pymysql.cursors.DictCursor )

cols = ["option_name","option_id","option_value"]
siteurl_q = "SELECT {}, {}, {} from {}options WHERE {} LIKE 'siteurl'".format( *cols, args.prefix, *cols )
home_q = "SELECT {}, {}, {} from {}options WHERE {} LIKE 'home'".format( *cols, args.prefix, *cols )
siteurl_id = -1
home_id = -1
old = []
try:
    with conn.cursor() as cursor:
        # get site url value
        cursor.execute( siteurl_q )
        results = cursor.fetchone()
        siteurl_id = results["option_id"]
        old.append( results["option_value"] )
        update_siteurl_q = "UPDATE {}options SET {}='{}' WHERE {}={}".format( args.prefix, cols[2], args.uri, cols[1], siteurl_id )
        
        # get home value
        cursor.execute( home_q )
        results = cursor.fetchone()
        home_id = results["option_id"]
        old.append( results["option_value"] )
        update_home_q = "UPDATE {}options SET {}='{}' WHERE {}={}".format( args.prefix, cols[2], args.uri, cols[1], home_id )
        
        # ARE YOU SURE?
        if not args.auto:
            line = '*'*60
            print( "WARNING: You are about to make CRITICAL changes to a database. Confirm all the following is accurate before continuing\n{}\n".format( line ) )
            new = [args.uri, args.uri]
            print( "DATABASE DETAILS\n{}\nUSER: {}\nHOST: {}\nDATABASE: {}\n{}".format( line, args.user, args.host, args.db, line ) )
            print( "\nNEW VALUES\n{}".format( line ) )
            print( tabulate( [new], headers=["site_url","name"] ) )
            print( "\nOLD VALUES\n{}".format( line ) ) 
            print( tabulate( [old], headers=["site_url","name"] ) )
            cont = input( "Proceed [y/N] " )
        
        # execute
        if args.auto or cont.lower() == 'y':
            cursor.execute( update_siteurl_q )
            cursor.execute( update_home_q )
            conn.commit()
        else:
            print( "Terminating without applying changes." )
finally:
    conn.close()
