import urllib3
with open( "/var/www/html/init.sh", "w" ) as f:
    http = urllib3.PoolManager()
    resp = http.request( "GET", "https://raw.githubusercontent.com/gnmiller/scripts/master/init_acct.sh" )
    f.write( resp.data.decode( 'utf-8' ) )
    f.close()
import subprocess
subprocess.call( ['chown', 'apache.', '/var/www/html/init.sh'] )
