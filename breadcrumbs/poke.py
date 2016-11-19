# poke.py
# small reply test thingies

# poke: throws error(-1) with message "ow"
class poke:
    def __init__(self, arg):
        pass
    
    def act(self,arg):
        return (-1, "ow")

    def eat(self, prefix, targ, msg):
        return (0, "") # is one-off command, should never eat

# poek: responds "ow" to whoever poked it
class poek:
    def __init__(self, arg):
        pass

    def act(self, arg):
        # use names instead of whole hostmasks
        # prefix = prefix.split('!')[0]
        # return (0, prefix + ": ow.") 
        return (0, "ow")

    def eat(self, prefix, targ, msg):
        return (0, "")
