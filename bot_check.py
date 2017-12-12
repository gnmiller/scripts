
with open( "/home/craig-bot/craig-bot/var/bot.pid", "r" ) as pid_file:
    bot_pid = pid_file.readline()

def check_pid( pid ):
    try:
        os.kill( pid, 0 )
    except OSError:
        return False
    else
        return True


