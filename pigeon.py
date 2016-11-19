# pigeon.py
# pigeonbot
import irc
import breadcrumbs

# - - - c o n f i g - - -
HOST = "avarice.wa.us.synirc.net"
PORT = 6667
NICK = "pigeon"
REALNAME = "pigeonbot"
NICKPASS = "pe3p3w6ew" # leave blank if unregistered

CHAN = "#site199"

# attempt to establish connection
irc = irc.IRC()
irc.connect(HOST, PORT)
irc.intro(NICK, REALNAME, NICKPASS)

#join channel
irc.join(CHAN)

# main loop
readbuffer = ""
pigeondaem = breadcrumbs.Daemon(irc)
while 1:
    try:
        # append to readbuffer
        readbuffer = readbuffer + irc.recv()
        
        # look for CR-LF, extract individual commands from bitstream
        if readbuffer.find("\r\n") != -1:
            lines = readbuffer.split("\r\n")

            for l in lines[:-1]:
                r = irc.parse(l)    # parse each line & handle accordingly
                irc.pingpong(r)     # respond to pings while we're at it

                pigeondaem.handle(r)    # hand message over to run things

            readbuffer = lines[-1]

    except KeyboardInterrupt:
        irc.part(CHAN)
        irc.exit()
        break

    except:
        irc.part(CHAN, "distressed pigeon noises")
        irc.exit()
        raise


