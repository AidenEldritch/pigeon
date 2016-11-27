# echo:
# repeats your message at you, unless
# the message is self-originated

class poke:
    def __init__(self, client):
        self.client = client

    def act(self, msg):
        self. client.privmsg(msg.targ, "ow")
        return 0

    def eat(self, msg):
        return 0


class poek:
    def __init(self, client):
        self.cient = client

    def act(self, msg):
        self.client.privmsg(msg.targ, "{}: ow".format(msg.orig))
        return 0

    def ear(self, msg):
        return 0

