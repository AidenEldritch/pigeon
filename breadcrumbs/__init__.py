import datetime

import breadcrumbs.echo
import breadcrumbs.time
import breadcrumbs.poke
import breadcrumbs.log


ACTIVATOR_CHAR = '.'

RET_CONTINUE = 1
RET_CONCLUDE = 0
RET_ERR = -1

class Daemon:
    def __init__(self, irc):
        self.irc = irc  # bound to irc

        # mapping between commands & tasks
        self.task_dict = {
                "echo"  : breadcrumbs.echo.echo,
                "time"  : breadcrumbs.time.time,
                "poke"  : breadcrumbs.poke.poke,
                "poek"  : breadcrumbs.poke.poek,
                "log"   : breadcrumbs.log.log
                }
        # collection of currently running tasks
        self.live_tasks = {} 

    def report(self, ret, rpltarg):
        # report result of task through irc
        # and returns continue flag
        if ret[0] == RET_CONTINUE:
            self.irc.privmsg(rpltarg, ret[1])
            return True

        elif ret[0] == RET_CONCLUDE:
            self.irc.privmsg(rpltarg, ret[1])
            return False

        else:
            # everything else is an error
            self.irc.privmsg(rpltarg, "ERROR: {} ({})".format(ret[1], ret[0]))
            return False


    def handle(self, r):
        
        if r[1] == "PRIVMSG":
            # - - - p r e p r o c e s s i n g - -

            # give things names easier to remember
            (prefix, targ, msg) = (r[0], r[2][0], r[2][1])

            # determine what to reply to, and who sent the message
            rpltarg = targ      # reply target
            cmdorig = prefix    # command origin

            # <nick>['!'<user>]['@'<host>]
            # deal only with nicks - strip anything else
            if cmdorig.find('!') != -1:
                cmdorig = cmdorig.split('!', 1)[0]
            if cmdorig.find('@') != -1:
                cmdorig = cmdorig.split('@', 1)[0]

            # check for target, if target does not have channel prefix char,
            # assume PM and send replys to user.
            if targ[0] != '#' and targ[0] != '&':
                # message wasn't from a channel, PM.
                rpltarg = cmdorig


            # - - - i m p e r a t i v e s - - -

            # listen for activator char prefix & start/end tasks
            if msg[0] == ACTIVATOR_CHAR: 
                cmd = msg[1:].rstrip()   # strip activator sequence & trailing whitespace
                argstr = ""
                if cmd.find(' ') != -1: # isolate the argument string if it exists
                    (cmd, argstr) = cmd.split(None, 1)

                # TODO: autocomplete cmd (binary search thingy)

                # check for relevant command in list
                # & run with given arguments
                if cmd in self.task_dict:   # cmd is a valid command

                    if not cmd in self.live_tasks:
                        # start a new instance of task
                        self.live_tasks[cmd] = self.task_dict[cmd](cmdorig, rpltarg, argstr)

                    # send command to it
                    ret = self.live_tasks[cmd].act(cmdorig, rpltarg, argstr)
                    # task.act(arg) returns a boolean specifying whether
                    # the task should continue to execute.
                    if not self.report(ret, rpltarg):
                        del self.live_tasks[cmd]

                else:
                    # no valid message
                    ret = (0, "")
                    pass # ignore nonexistent commands


            # - - - f u n n e l l i n g - - -

            # feed message through every currently running
            # process & process returns accordingly
            to_kill = []
            for taskname, task in self.live_tasks.items():

                ret = task.eat(prefix, targ, msg) #ret is of format (SIGNAL, MSG)

                if not self.report(ret, rpltarg):
                    to_kill.append(taskname)

            # finally kill everything that's marked ended
            for i in to_kill:
                del self.live_tasks[i]


            # joek                
            if msg == "breadcrumb":
                self.irc.privmsg(rpltarg, ":>")

            if msg == "hoi!":
                self.irc.privmsg(rpltarg, "hoi!")
