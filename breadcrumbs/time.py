# time.py
# timeteller
import datetime

# time:
# currently a placeholder for testing multiple handlers.
# TODO: actually write this to be something reasonable
class time:
    def __init__(self, cmdorig, rpltarg, argstr):
        pass

    def act(self, cmdorig, rpltarg, argstr):
        timestr = datetime.datetime.utcnow().isoformat() + " (UTC)"
        return (0, timestr)

    def eat(self, msgorig, rpltarg, msg):
        return (0, "")
