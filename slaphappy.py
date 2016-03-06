import minqlx
import threading
import time

class slaphappy(minqlx.Plugin):

    def __init__(self):
        self.add_command("slaphappy", self.cmd_slaphappy, 2, usage="<id> <number of slaps> <frequency in seconds> [damage]")

    def cmd_slaphappy(self, player, msg, channel):
        def do_every(interval, worker_func, iterations=0):
            if iterations != 1:
                threading.Timer(
                    interval,
                    do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
                ).start()
            worker_func()

        if len(msg) < 4:
            return minqlx.RET_USAGE

        try:
            i = int(msg[1])
            target_player = self.player(i)
            if not (0 <= i < 64) or not target_player:
                raise ValueError
        except ValueError:
            player.tell("Invalid ID.")
            return minqlx.RET_STOP_ALL

        try:
            slap_amount = int(msg[2])
            if not slap_amount or slap_amount < 1:
                raise ValueError
        except ValueError:
            player.tell("Invalid number of slaps.")
            return minqlx.RET_STOP_ALL

        try:
            slap_frequency = float(msg[3])
            if not slap_frequency or slap_frequency <= 0:
                raise ValueError
        except ValueError:
            player.tell("Invalid slap frequency.")
            return minqlx.RET_STOP_ALL

        if len(msg) > 4:
            try:
                dmg = int(msg[4])
            except ValueError:
                player.tell("Invalid damage value.")
                return minqlx.RET_STOP_ALL
        else:
            dmg = 0

        def slapper():
            self.slap(target_player, dmg)

        channel.reply("^2SLAPHAPPY ACTIVATED ON: ^6{}^7 !!! IN...".format(target_player.name))

        #Countdown timer
        @minqlx.thread
        def countdown():
            for i in range(5, 0, -1):
                channel.reply("^1" + str(i) + "..")
                time.sleep(1)
            do_every(slap_frequency, slapper, slap_amount)

        countdown()

        return minqlx.RET_STOP_ALL