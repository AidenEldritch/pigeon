# log:
# logs things said in channel

import datetime

LOG_TIMESTAMP_FORMAT = "%y-%m-%d.%H:%M:%S.%f"#"%Y-%m-%d.%H:%M:%S.%f"

class log:
    def __init__(self, client):
        self.client = client
        self.chans = {}
        # self.chans structure:
        # {
        #   "chan" : {
        #               "next" : i,
        #               "logs" : {
        #                   id1 : file1
        #                   id2 : file2
        #                   }
        # }

    # starts a log for channel or PM targ.
    # TODO: actually care about the title.
    def logstart(self, targ, title):
        # start a log with targ(chan or user).
        timestamp = datetime.datetime.utcnow()\
                    .strftime(LOG_TIMESTAMP_FORMAT)
        # append title if it's nonempty
        if title:
            title = "(" + title + ")"

        # open file object
        logfile = open(
                "{}.{}.log".format(targ, timestamp),
                "w")

        # add logfile to stupidly elaborate structure
        # of currently opened logs
        if not targ in self.chans:
            self.chans[targ] = { "next" : 0, "logs": {} }

        self.chans[targ]["logs"][str(self.chans[targ]["next"])] = logfile
        self.chans[targ]["next"] += 1

        # announce the new log
        print(self.chans[targ])
        self.client.privmsg(targ, "log of {} started at {}".format(
            targ, logfile.name))


    # sends a ist of all active logs of the current chan
    def loglist(self, targ):
        if targ in self.chans:
            logliststr = "currently active logs of " + targ + ":"

            sortedi = list(self.chans[targ]["logs"].keys())
            sortedi.sort()

            for i in sortedi:
                logliststr += " [{}: {}]".format(
                        i, self.chans[targ]["logs"][i].name)
            
            logliststr += " ({} total)".format(len(self.chans[targ]["logs"]))

            self.client.privmsg(targ, logliststr)
        else:
            self.client.privmsg(targ, "no active logs of " + targ + " currently exist")


    # end logs in a fashion as specified by the string arg:
    # - if empty, do the most reasonable thing
    # - if nonempty, attempt to parse as a space-delimited
    #   series of logs to end, end each existent one, and
    #   report results.
    def logend(self, targ, arg):

        # return if there is nothing to close
        if not targ in self.chans:
            self.client.privmsg(targ,
                    "no active logs of {} currently exist".format(targ))
            return

        # generate list of attempts from argument provided.
        if arg == "all" or len(self.chans[targ]["logs"]) == 1:
            # close everything.
            l = list(self.chans[targ]["logs"].keys())
            l.sort()

        elif arg:
            # list provided.
            l = arg.split(None)
        
        else:
            # ambiguous, return.
            self.client.privmsg(targ, "which log do you wish to close? Use '.log list' to view a list of all currently active logs.")
            return

        # start closing the logs.
        logendstr = "ended: "
        killcount = 0

        # attempt to end each log.
        for ki in l:
            if ki in self.chans[targ]["logs"]:
                f = self.chans[targ]["logs"][ki]
                f.close()

                logendstr += " [{}: {}]".format(ki, f.name)

                del self.chans[targ]["logs"][ki]
                killcount += 1

        logendstr += " ({} total".format(killcount)
        
        if len(self.chans[targ]["logs"]) > 0:
            logendstr += ")"
        else:
            # no more logs left in this channel
            del self.chans[targ]
            logendstr += ", all logs of {} ended)".format(targ)

        # announce results
        self.client.privmsg(targ, logendstr)



    def act(self, msg):
        s = msg.trl.split(None, 2)
        # assume user wants to start log
        # if no action provided.
        if len(s) == 1:
            s.append("start")
        # always have a third argument
        if len(s) == 2:
            s.append("")

        # possible commands:
        if s[1].lower() == "start":
            self.logstart(msg.targ, s[2])
            return 1

        if s[1].lower() == "list":
            self.loglist(msg.targ)
            return 1

        if s[1].lower() == "end":
            self.logend(msg.targ, s[2])

        # if there's nothing left, end the log task
        if len(self.chans) > 0:
            return 1
        else:
            return 0
            
        # no commands matched, carry on
        return 1


    def eat(self, msg):
        if msg.targ in self.chans:
            for i, f in self.chans[msg.targ]["logs"].items():
                f.write("{}: {}\n".format(msg.orig, msg.trl))
        return 1

