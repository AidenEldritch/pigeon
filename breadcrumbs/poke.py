# poke.py
# small reply test thingies

# poke: throws error(-1) with message "ow"
class poke:
    def __init__(self, cmdorig, rpltarg, argstr):
        pass
    
    def act(self, cmdorig, rpltarg, argstr):
        return (-1, "ow")

    def eat(self, prefix, targ, msg):
        return (0, "") # is one-off command, should never eat

# poek: responds "ow" to whoever poked it
class poek:
    def __init__(self, cmdorig, rpltarg, argstr):
        pass

    def act(self, cmdorig, rpltarg, argstr):
        # use names instead of whole hostmasks
        # prefix = prefix.split('!')[0]
        # return (0, prefix + ": ow.") 
        return (0, cmdorig + ": ow")

    def eat(self, prefix, targ, msg):
        return (0, "")
