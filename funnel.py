# funnel:
# irc message handling thingy

class Funnel:
    def __init__(self, client, taskmap = None):

        # bound to client:
        self.client = client
        self.ACTIVATOR_CHAR = "."

        # taskmap is a dict(str, task)
        if taskmap == None:
            self.taskmap = {}
        else:
            self.taskmap = taskmap

        # tasks that can possibly be called
        self.tasknames = list(self.taskmap.keys())
        self.tasknames.sort()
        
        # currently running
        self.livetasks = {}
        

    def handle(self, msg):
        # only handle PRIVMSGs for now
        if msg.cmd != "PRIVMSG":
            return
        
        # usual messages
        to_kill = []
        for c, task in self.livetasks.items():
            if not task.eat(msg):
                to_kill.append(c)

        # kill all kill-queued tasks
        for i, c in enumerate(to_kill):
            del self.livetasks[cmd]
            print(" - ENDED TASK " + cmd)

        # ACTIVATOR_CHAR starts a command
        if msg.trl[0] == self.ACTIVATOR_CHAR:

            cmd = msg.trl.split(' ', 1)[0][1:].lower()
            
            if (cmd in self.tasknames):
                if not (cmd in self.livetasks):
                    self.livetasks[cmd] = self.taskmap[cmd](self.client)
                    print(" - STARTED TASK " + cmd)

                if not self.livetasks[cmd].act(msg):
                    del self.livetasks[cmd]
                    print(" - ENDED TASK " + cmd)


