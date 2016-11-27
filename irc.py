import socket

# some constants
IRC_BUFFER_SIZE = 512
IRC_CRLF = "\r\n"
IRC_ENCODING = "utf-8"

# parsed message class
class Msg:
    def __init__(self, orig = "", targ = "", cmd = "", args = [], trl = ""):
        self.orig = orig
        self.targ = targ
        self.cmd = cmd
        self.args = args
        self.trl = trl

# irc client class
class IRC:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.host = ""
        self.port = 6667
        self.nick = "pigeon"
        self.realname = "pigeonbot"
        self.nickpass = "pfffrbft"

        self.chanlist = []
        self.autochan = []

        self.rbuff = ""
        self.wbuff = ""


    def config(self, conf):
        if "HOST" in conf:
            self.host = conf["HOST"]

        if "PORT" in conf:
            self.port = conf["PORT"]

        if "NICK" in conf:
            self.nick = conf["NICK"]

        if "REALNAME" in conf:
            self.realname = conf["REALNAME"]

        if "NICKPASS" in conf:
            self.nickpass = conf["NICKPASS"]

        if "AUTOJOIN" in conf:
            self.autojoin = conf["AUTOJOIN"]

    def connect(self):
        self.socket.connect((self.host, self.port))


    def recv(self):
        self.rbuff += self.socket.recv(IRC_BUFFER_SIZE).decode(IRC_ENCODING)

    def send(self, msg):
        msg += "\r\n"
        self.wbuff += msg
        self.socket.send(msg.encode(IRC_ENCODING))
            
    def next_msg(self):
        msgbuff = ""
        selfmsg = False
        
        # prioritise sent messages, & drop next line to parse into msgbuff
        if self.wbuff.find(IRC_CRLF) != -1:
            (msgbuff, self.wbuff) = self.wbuff.split(IRC_CRLF, 1)
            selfmsg = True
        else:
            while 1:
                cutoff = self.rbuff.find(IRC_CRLF)
                if cutoff == -1:
                    self.recv()
                else:
                    break
            (msgbuff, self.rbuff) = self.rbuff.split(IRC_CRLF, 1)
            selfmsg = False

        # parse the message.
        msg = Msg()
        
        # prefix and command:
        if msgbuff[0] == ':':
            msgbuff = msgbuff[1:]
            (msg.orig, msg.cmd, msgbuff) = msgbuff.split(None, 2)
        else:
            (msg.cmd, msgbuff) = msgbuff.split(None, 1)
        
        # trailing
        if msgbuff.find(':') != -1:
            (msgbuff, msg.trl) = msgbuff.split(':', 1)

        # arguments
        msg.args = msgbuff.split(None)


        # tag self-originating messages
        if selfmsg:
            msg.orig = self.nick

        # deal only with nicks, remove host bit of prefix
        if msg.orig.find('!') != -1:
            msg.orig = msg.orig.split('!', 1)[0]
        if msg.orig.find('@') != -1:
            msg.orig = msg.orig.split('@', 1)[0]

        if len(msg.args) > 0:
            if msg.args[0][0] == '#'\
            or msg.args[0][0] == '&'\
            or msg.args[0] == self.nick:
                msg.targ = msg.args[0]
                msg.args = msg.args[1:]


        return msg

    def wait_for(self, condition):
        while 1:
            msg = self.next_msg()
            # still respond to pings to prevent timeout
            self.pingpong(msg)
            if condition(msg):
                break

    def intro(self):
        self.send("USER {} {} {} :{}".format(
            self.nick, self.nick, self.nick, self.realname))
        self.send("NICK {}".format(self.nick))

        self.wait_for(lambda m: m.cmd == "001")

    def ns_ident(self, authformat = "PRIVMSG Nickserv :IDENTIFY {}"):
        self.send(authformat.format(self.nickpass));
        self.wait_for(lambda m: ( \
            m.cmd == "MODE" and \
            m.trl[0] == '+' and \
            m.trl.find('r') != -1))

    def join(self, chan):
        self.send("JOIN " + chan)
        self.wait_for(lambda m: m.cmd == "JOIN" and \
                                m.orig == self.nick and \
                                m.trl.lower() == chan.lower())
        self.chanlist.append(chan)

    def auto_join(self):
        for i, chan in enumerate(self.autojoin):
            if chan[0] == '#' or chan[0] == '&':
                self.join(chan)
            else:
                self.send("PRIVMSG {} :.".format(chan))


    def pingpong(self, msg):
        if msg.cmd == "PING":
            self.send("PONG :"+msg.trl)
