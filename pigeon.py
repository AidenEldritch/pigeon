import sys
import irc
import funnel
from breadcrumbs import echo
from breadcrumbs import poke
from breadcrumbs import log
# main program

print("STARTING CLIENT...")
client = irc.IRC()

print("LOADING CONFIG...")
client.fconfig("pigeon.conf")

print("ATTEMPTING TO ESTABLISH CONNECTION...")
client.connect()

print("SENDING CLIENT INFO...")
client.intro()

if client.nickpass:
    print("CLAIMING REGISTERED NICK...")
    client.ns_ident()

print("JOINING CHANNELS...")
client.auto_join()

print("STARTING FUNNEL(MSG HANDLER)...")
funnel = funnel.Funnel(client, {
    "echo"  : echo.echo,
    "poke"  : poke.poke,
    "poek"  : poke.poek,
    "log"   : log.log
    });

print("ENTERING LISTEN LOOP...")
while 1:

    try:
        msg = client.next_msg()
        irc.print_msg(msg)

        client.pingpong(msg)

        # joek
        if msg.trl == "breadcrumb":
            client.privmsg(msg.targ, ":>")
        if msg.trl == "borkcrumb":
            raise ValueError("borked")

        funnel.handle(msg)

    except KeyboardInterrupt:
        client.graceful_exit(client.partmsg)
        sys.exit(0)

    except:
        client.graceful_exit(client.borkmsg)
        raise
