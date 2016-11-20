# log.py:
# chatlogging
import datetime

# log
# usage: log [start [title]|end [#]]
class log:
    def __init__(self, cmdorig, rpltarg, argstr):
        self.live_logs = []

    def logstart(self, title):
        # start new log
        stamp = datetime.datetime.utcnow().isoformat()

        if not title:
            title = "untitled"

        # generate filename from timestamp & title
        fname = "log-{}-{}".format(stamp, title)

        logfile = None
        try:
            logfile = open(fname, 'w')
        except:
            return (-1, "failed to open file.")

        self.live_logs.append(logfile)
        return (1, "started writing log to: " + logfile.name)

    def logend(self, targi):
        i = 0
        if not targi:
            if len(self.live_logs) == 0:
                return (1, "no open logs")

            elif len(self.live_logs) == 1:
                # if there is only one log open,
                # .log end ends that one.
                pass

            else:
                # request elaboration
                return (1, "which log did you mean? (use \".log list\" to display all logs being written to.)")

        else:
            # a target is specified
            # attempt to parse target as number
            try:
                i = int(targi)
            except:
                # invalid target
                return (1, "invalid file specified")

        # attempt to close i
        if i >= len(self.live_logs):
            # out of range
            return (1, "that log does not exist")
        
        # i is valid, close log file
        fname = self.live_logs[i].name
        self.live_logs[i].close()
        del self.live_logs[i]

        if len(self.live_logs) > 0:
            return (1, "log written to " + fname)
        else:
            return (0, "log written to " + fname + ". all logs closed.")

    def loglist(self):
        # list all the running logs
        retstr = "logs currently being written to: "

        for i, f in enumerate(self.live_logs):
            retstr += str(i) + ":" + f.name + " "

        retstr += "({} total)".format(str(len(self.live_logs)))
        return (1, retstr)


    def act(self, cmdorig, rpltarg, argstr):
        
        # TODO: better arg parsing because if else statements are silly
        # by default, .log just starts a log w/o title.
        if not argstr:
            argstr = "start"

        # trailing is just whatever after the first word
        trailing = ""
        if argstr.find(' ') != -1:
            argstr, trailing = argstr.split(None, 1)

        if argstr == "start":
            return self.logstart(trailing)

        elif argstr == "end":
            return self.logend(trailing)
        
        elif argstr == "list":
            return self.loglist()

        else:
            # did not recognise command
            # write man page here later and dump it
            return (1, "")

    def eat(self, prefix, targ, msg):

        for logfile in self.live_logs:
            try:
                logfile.write(msg+"\n")
            except:
                return (-1, "error writing to " + logfile.name)

        # all logs written to, carry on
        return (1, "") 
