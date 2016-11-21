# log.py:
# chatlogging
import datetime

# non-alphanumeric characters to be used in title stripping
NON_ALNUM = "".join(c for c in map(chr, range(256)) if not c.isalnum())

# log
# usage: log [start [title]|end [#]]
class log:
    def __init__(self, cmdorig, rpltarg, argstr):
        self.live_logs = {}
        self.log_index = 0
        
    def logstart(self, logged_ch, title):
        # start new log
        stamp = datetime.datetime.utcnow().isoformat()

        # strip non-alphanumeric chars from title
        ftitle = title
        #ftitle.translate(None, NON_ALNUM)
        ftitle.replace(' ', '_')
        
        if not ftitle:
            ftitle = "untitled"

        # generate filename from timestamp & title
        fname = "{}-{}.log".format(stamp, ftitle)

        logfile = None
        try:
            # open a logfile & write title lines
            logfile = open(fname, 'w')
            logfile.write("chat log of {} starting {}: {}\n".format(logged_ch, stamp, title))

        except:
            return (-1, "failed to open file.")


        # dict indicies are in string format
        # so that user specifications don't need
        # to be converted into int every time
        self.live_logs[str(self.log_index)] = (logged_ch, logfile)
        self.log_index += 1

        return (1, "started writing log to: " + logfile.name)


    def logend(self, targi):
        endli = [] # list of log indicies to end

        if not targi:
            if len(self.live_logs) == 1:
                # if there is only one log open,
                # .log end ends that one.
                endli.append(next(iter(self.live_logs)))

            else:
                # request elaboration
                return (1, "which logfile did you mean? (use \".log list\" to display all logfiles currently open.")

        else:
            # target or targets are specified.
            # try figuring out what they are.
            targi = targi.split()   # list of arguments
            if targi[0] == "all":
                # end everything.
                for i in self.live_logs:
                    endli.append(i)

            else:
                for i in targi:
                    endli.append(i)
                    # append target. Note that i is not necessarily valid -
                    # will be checked in next stage.

        # attempt to delete each target
        ended = {}
        invalid = []
        for i in endli:
            if not i in self.live_logs:
                # attempted to close nonexistent log. ignore.
                invalid.append(i)

            else:
                # record that this is ended.
                ended[i] = self.live_logs[i][1].name
                self.live_logs[i][1].close()
                del self.live_logs[i]

        # report results:
        retstr = "ended log(s): "
        retsig = 1
        for i in sorted(ended):
            retstr += i + ":" + ended[i] + " "
        retstr += "({} total".format(str(len(ended)))

        if len(self.live_logs) == 0:
            retstr += ", all logs ended)"
            retsig = 0  # if all logs are ended, close the task instance.
        else:
            retstr += ")"

        return (retsig, retstr)


    def loglist(self):
        # list all the running logs
        retstr = "logfiles currently being written to: "

        for i in sorted(self.live_logs):
            retstr += "{}: {} (of {}) ".format(i,   # index
                    self.live_logs[i][1].name,      # logfile name
                    self.live_logs[i][0])           # log target

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
            return self.logstart(rpltarg, trailing)

        elif argstr == "end":
            return self.logend(trailing)
        
        elif argstr == "list":
            return self.loglist()

        else:
            # did not recognise command
            # write man page here later and dump it
            return (1, "")


    def eat(self, msgorig, rpltarg, msg):
        for i, f in self.live_logs.items():
            # write only to relevant logs.
            if f[0] == rpltarg:
                if msgorig == "":
                    msgorig = "pigeon(self)"
                # f[0] == rpltarg: sent or recv'd message @ channel
                # msgorig == ""  : sent msg
                try:
                    f[1].write("<{}> {}\n".format(msgorig, msg))
                except:
                    return (-1, "error writing to " + f[1].name)
        # all logs written to, carry on
        return (1, "") 
