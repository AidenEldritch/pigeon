# echo.py
# repeats messages sent.

class echo:
    def __init__(self, cmdorig, rpltarg, argstr):
        pass

    def act(self, cmdorig, rpltarg, argstr):
        return (1, argstr)

    def eat(self, prefix, targ, msg):
        return (0, "") # this should never run.
