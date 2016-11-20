# pigeon.py
# pigeonbot
import json         # for config files
import irc          # irc class
import breadcrumbs  # functionality modules


# read config file
with open("pigeon.conf") as f:
    conf = json.load(f)


# attempt to establish connection
irc = irc.IRC()
irc.connect(conf["HOST"], conf["PORT"])
irc.intro(conf["NICK"], conf["REALNAME"], conf["NICKPASS"])

#join channel
irc.join(conf["CHAN"])

# main loop
readbuffer = ""
pigeondaem = breadcrumbs.Daemon(irc)
while 1:
    try:
        # append to readbuffer
        readbuffer = readbuffer + irc.recvecho() #irc.recv()
        # look for CR-LF, extract individual commands from bitstream
        if readbuffer.find("\r\n") != -1:
            lines = readbuffer.split("\r\n")

            for l in lines[:-1]:
                r = irc.parse(l)    # parse each line & handle accordingly
                irc.pingpong(r)     # respond to pings while we're at it

                pigeondaem.handle(r)    # hand message over to run things

            readbuffer = lines[-1]

    except KeyboardInterrupt:
        irc.part(conf["CHAN"])
        irc.exit()
        break

    except:
        irc.part(conf["CHAN"], "distressed pigeon noises")
        irc.exit()
        raise


