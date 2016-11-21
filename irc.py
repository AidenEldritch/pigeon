# irc.py:
# irc class for pigeonbot

import socket
import sys

# - - - i r c - c o n s t s - - -
RPL_WELCOME = "001"

class IRC:
    def __init__(self):
        self.socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        
        self.outbuffer = ""     # things sent

        self.incomplete = False # flag on whether the client is
                                # waiting on another half of a msg

    def exit(self):
        self.socket.close()

    def connect(self, host, port):
        self.socket.connect((host, port))

    def send(self, msg, encoding = "utf-8"):
        # wrapper for socket.send, handles encoding
        msg = msg + "\r\n"  # note that this modifies the message
                            # that is returned.
        self.socket.send((msg).encode(encoding))
        #print(msg)
        self.outbuffer += msg
        return msg

    def privmsg(self, targ, msg):
        # wrapper for send to make PRIVMSGs look cleaner

        if not msg:
            return # just to make the logs cleaner

        msg = "PRIVMSG " + targ + " :" + msg
        return self.send(msg)

    def recv(self, l = 1024, encoding = "utf-8"):
        # wrapper for socket.recv, handles decoding
        s = self.socket.recv(l).decode(encoding)
        self.incomplete = (s[-2:] != "\r\n")
        
        return s

    def recvecho(self, l = 1024, encoding = "utf-8"):

        # receive function for use in main loop:
        # also echoes messages it sent itself.
        if (not self.incomplete) and self.outbuffer:
            s = self.outbuffer
            self.outbuffer = ""
            return s

        s = self.socket.recv(l).decode(encoding)
        self.incomplete = (s[-2:] != "\r\n")
        return s




    def parse(self, s):
        # parsing irc message

        p = "" # prefix
        t = "" # trailing params

        # BNF representation of protocol message (RFC 1459):
        # <message>  ::= [':' <prefix> <SPACE> ] <command> <params> <crlf>
        # <prefix>   ::= <servername> | <nick> [ '!' <user> ] [ '@' <host> ]
        # <command>  ::= <letter> { <letter> } | <number> <number> <number>
        # <SPACE>    ::= ' ' { ' ' }
        # <params>   ::= <SPACE> [ ':' <trailing> | <middle> <params> ]


        if not s:
            raise IRCBadMessage("empty line.")

        if s[0] == ':': # obtain prefix if exists
            (p, s) = s[1:].split(None, 1)

        # obtain args & trailing
        if s.find(' :') != -1: # if trailing exists, strip & append to command-arg
            (s, t) = s.split(' :', 1)
            args = s.split()
            args.append(t)

        else:
            args = s.split() # command, followed by all the args

        # extract command
        cmd = args[0]
        args = args[1:]

        # print parsed message for debug purposes
        for i in (p, cmd, args):
            print(i)
        print()

        # return formatted message
        return (p, cmd, args)


    def pingpong(self, r):
        #check if parsed message is a ping, and if it is, pong.
        if r[1] == "PING":
            self.send("PONG :" + r[2][0])

    def waitfor(self, cmd, f = lambda r:True):
        # wait for specific command before proceeding
        # w/ optional conditional testing for params
        readbuffer = ""
        while 1:
            readbuffer = readbuffer + self.recv()
            if readbuffer.find("\r\n") != -1:
                lines = readbuffer.split("\r\n")
                for l in lines[:-1]:
                    r = self.parse(l)

                    # still handle pings
                    self.pingpong(r)

                    # check if event waited for has happened
                    if r[1] == cmd and f(r):
                        return

                readbuffer = lines[-1]


    def intro(self, nick, realname, nickpass):

        self.send("NICK " + nick)
        self.nick = nick # keep this handy
        self.send("USER {} {} {} :{}".format(nick, nick, nick, realname))
        # specification USER uname hostname servname :realname,
        # practically all but uname and realname are ignored

        # wait for welcome message before sending any further commands
        self.waitfor(RPL_WELCOME)

        if not nickpass:
            # do the identify thing
            self.identify(nickpass)
            self.waitfor("MODE", lambda r: r[2][1].find("r") != -1)

    def join(self, chan):
        self.send("JOIN " + chan)

    def part(self, chan, msg="annoying pigeon noises"):
        self.send("PART " + chan + " " + msg)

    def identify(self, nickpass):
        self.send("PRIVMSG NICKSERV IDENTIFY " + nickpass)


