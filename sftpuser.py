#!/usr/bin/python

import os, sys, argparse, crypt, random, string

# args
parser = argparse.ArgumentParser( description="Create a new SFTP user on the system." )
parser.add_argument( "-n", "--name", action="store", dest="name", required=True, help="The name of the new user." )
parser.add_argument( "-d", "--home", action="store", dest="home", required=False, help="User's home directory. The home directory will always be rooted /home/. The arguments passed will be read as '/home/<args>.' If not specified /home/DMS/<user> will be used." )
parser.add_argument( "-p", "--passwd", action="store", dest="passwd", required=False, help="User's password. If not specified a random password will be generated and printed to the terminal." )
parser.add_argument( "-y", action="store_true", dest="yes", required=False, help="Automatically assume yes to prompts." )
parser.add_argument( "-l", "--login", action="store_true", dest="l", required=False, help="Set the default shell to allow login or not (/sbin/nologin vs /bin/bash)" )
parser.add_argument( "--ftp", action="store_true", dest="ftp", required=False, help="Set this user as an SFTP user. Will attempt to auto-adjust permissions on their home directory. Passing this argument and the -d/--home argument has undefined results." )
parser.add_argument( "-vv", action="store_true", dest="vv", required=False, help="Output additional information for copy/pasting to emails." )
args = parser.parse_args()

# passwd generator
rand_str = lambda n: ''.join([random.choice(string.lowercase) for i in xrange(n)])

# name and home
name = args.name
if args.home == None:
    home = "/home/DMS/"+name
else:
    home = "/home/"+args.home

# passwd
if args.passwd == None:
    passwd = rand_str( 16 )
else:
    passwd = args.passwd

# shell
if args.l == True:
    shell = "/bin/bash"
else:
    shell = "/sbin/nologin"

if args.vv == True:
    # CHANGE ME BEFORE RUNNING
    print( "Server Details\nHost: 204.10.x.x\nPort: x\n" )
    sys.exit(1)
# do stuff
print( "Adding new user to the system\nUsername: {0}\nPassword: {1}\nHome Dir: {2}\nSSH: {3}\nFTP: {4}\n".format( name, passwd, home, args.l, args.ftp ) )
i = raw_input( "Confirm [Y/n] " )
if args.yes == True:
    i = 'y'
if i.lower() == 'n':
    print( "Exiting without adding user." )
    sys.exit(0)
else:
    e_passwd = crypt.crypt(passwd,"54")
    #print(  "useradd -p " + e_passwd + " -s " + shell + " -d " + home + " -m " + name )
    os.system( "sudo useradd -p " + e_passwd + " -s " + shell + " -d " + home + " -m -G sftp " + name )
    # chown to DMS:user and set perms
    if args.ftp == True:
        print( "Attempting to set user as FTP user..." )
        # mkdir -p /home/DMS/user/upload
        os.system( "sudo mkdir -p /home/DMS/{0}/upload/".format( name ) )
        # chwon root:DMS /home/DMS/user -R
        ch_str = "sudo chown root:DMS /home/DMS/{0} -R".format( name )
        os.system( ch_str )
        # chown user:DMS /home/DMS/user/upload
        # chmod 755 /home/DMS/user -- chroot jail ...
        ch_str = "sudo chown {0}:DMS /home/DMS/{0}/upload/".format( name )
        os.system( "sudo chmod 755 /home/DMS/{0}".format( name ) )
        ch_str = "sudo chmod 775 /home/DMS/{0}/* -R".format( name ) )
        os.system( ch_str )
    sys.exit(0)
