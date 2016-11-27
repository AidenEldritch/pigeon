# echo:
# repeats your message at you, unless
# the message is self-originated

class echo:
    def __init__(self, client):
        self.client = client

    def act(self, msg):
        if msg.trl.find(' ') != -1:
            self.client.privmsg(msg.targ, msg.trl.split(None, 1)[1])
        return 0

    def eat(self, msg):
        return 0

