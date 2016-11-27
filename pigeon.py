import irc
import json

# main program

client = irc.IRC()
print("LOADING CONFIG...")
with open("pigeon.conf") as conffile:
    conf = json.load(conffile)
    client.config(conf)

print("CONNECT...")
client.connect()
print("CONNECTION ESTABLISHED.")

print("SENDING CLIENT INFO...")
client.intro()
print("WELCOME MESSAGE RECEIVED.")

if client.nickpass:
    print("CLAIMING REGISTERED NICK...")
    client.ns_ident()
    print("RECOGNISED.")

print("JOINING CHANNELS...")
client.auto_join()

while 1:
    msg = client.next_msg()
    print("ORIG: {}\nTARG: {}\n CMD: {}\nARGS: {}\n TRL: {}\n".format(
        msg.orig, msg.targ, msg.cmd, msg.args, msg.trl));
    client.pingpong(msg)
