# echo.py
# repeats messages sent.

class echo:
    def __init__(self, cmdorig, rpltarg, argstr):
        pass

    def act(self, cmdorig, rpltarg, argstr):
        if argstr[:5] == ".echo":
            return (0, "congrats u are v clever")
        elif argstr[0] == ".":
            return (0, "")

        return (0, argstr)

    def eat(self, msgorig, rpltarg, msg):
        return (0, "") # this should never run.
