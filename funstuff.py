import minqlx
import threading
import time

class funstuff(minqlx.Plugin):

    def __init__(self):
        self.game_ended = False

        self.add_command("gay", self.cmd_gay, 2)
        self.add_command("gayall", self.cmd_gayall, 2)
        self.add_command("straight", self.cmd_straight, 2)
        self.add_command("straightall", self.cmd_straightall, 2)

        self.add_command("kill", self.cmd_kill, 2)
        self.add_command("killall", self.cmd_killall, 2)

        self.add_command("slaphappy", self.cmd_slapvote, 2, usage="<id> <number of slaps> <frequency in seconds> [damage]")
        self.add_command("slaptrigger", self.cmd_slaphappy, 2)

        self.add_command("purgatory", self.cmd_purgatory, 2)
        self.add_command("purgatorytrigger", self.cmd_purgatory_trigger, 2)

        self.add_command("rename", self.cmd_rename, 2)
        self.add_command("renametrigger", self.cmd_rename_trigger, 2)

        self.add_command("hulk", self.cmd_hulk, 2)
        self.add_command("hulktrigger", self.cmd_hulk_trigger, 2)

        self.add_hook("new_game", self.handle_new_game)
        self.add_hook("game_end", self.handle_game_end)

    def handle_new_game(self, *args, **kwargs):
        self.game_ended = False

    def handle_game_end(self, *args, **kwargs):
        self.game_ended = True

    def cmd_hulk(self, player, msg, channel):
        if msg[1] != "everyone":
            try:
                i = int(msg[1])
                target_player = self.player(i)
                if not (0 <= i < 64) or not target_player:
                    raise ValueError
            except ValueError:
                player.tell("Invalid ID.")
                return minqlx.RET_STOP_ALL

        if msg[1] == "everyone":
            first_arg = target_player_string = "everyone"
        else:
            target_player_string = target_player.name
            first_arg = int(msg[1])

        self.callvote('qlx !hulktrigger {}'.format(first_arg), "^2Hulkify ^7{}".format(target_player_string))

    def cmd_hulk_trigger(self, player, msg, channel):
        if msg[1] != "everyone":
            try:
                i = int(msg[1])
                target_player = self.player(i)
                target_name = target_player.name
                if not (0 <= i < 64) or not target_player:
                    raise ValueError
            except ValueError:
                player.tell("Invalid ID.")
                return minqlx.RET_STOP_ALL
        else:
            target_name = "EVERYONE"

        if msg[1] != "everyone":
            self.player(i).health = 32767
            self.player(i).armor = 32767
            self.player(i).powerups(quad=10000, regeneration=1000, battlesuit=1000, haste=1000)
        else:
            for p in self.players():
                self.player(p.id).health = 32767
                self.player(p.id).armor = 32767
                self.player(p.id).powerups(quad=10000, regeneration=1000, battlesuit=1000, haste=1000)

    def cmd_rename(self, player, msg, channel):
        if msg[1] != "everyone":
            try:
                i = int(msg[1])
                target_player = self.player(i)
                if not (0 <= i < 64) or not target_player:
                    raise ValueError
            except ValueError:
                player.tell("Invalid ID.")
                return minqlx.RET_STOP_ALL

        try:
            msg[2]
        except:
            player.tell("Missing name to rename to.")
            return minqlx.RET_STOP_ALL

        if msg[1] == "everyone":
            first_arg = target_player_string = "everyone"
        else:
            target_player_string = target_player.name
            first_arg = int(msg[1])

        self.callvote('qlx !renametrigger {} {}'.format(first_arg, msg[2]), "Rename {} ^7to {}".format(target_player_string, msg[2]))

    def cmd_rename_trigger(self, player, msg, channel):
        if msg[1] != "everyone":
            try:
                i = int(msg[1])
                target_player = self.player(i)
                target_name = target_player.name
                if not (0 <= i < 64) or not target_player:
                    raise ValueError
            except ValueError:
                player.tell("Invalid ID.")
                return minqlx.RET_STOP_ALL
        else:
            target_name = "EVERYONE"

        if msg[1] != "everyone":
            self.player(i).name = msg[2]
        else:
            for p in self.players():
                self.player(p.id).name = msg[2]

    def cmd_purgatory(self, player, msg, channel):
        if msg[1] != "everyone":
            try:
                i = int(msg[1])
                target_player = self.player(i)
                if not (0 <= i < 64) or not target_player:
                    raise ValueError
            except ValueError:
                player.tell("Invalid ID.")
                return minqlx.RET_STOP_ALL

        if msg[1] == "everyone":
            first_arg = target_player_string = "everyone"
        else:
            target_player_string = target_player.name
            first_arg = int(msg[1])

        self.callvote('qlx !purgatorytrigger {}'.format(first_arg), "Send {} to ^1PURGATORY".format(target_player_string))

    def cmd_purgatory_trigger(self, player, msg, channel):
        if msg[1] != "everyone":
            try:
                i = int(msg[1])
                target_player = self.player(i)
                target_name = target_player.name
                if not (0 <= i < 64) or not target_player:
                    raise ValueError
            except ValueError:
                player.tell("Invalid ID.")
                return minqlx.RET_STOP_ALL
        else:
            target_name = "EVERYONE"

        self.center_print("^2SENDING {}^2 TO ^1PURGATORY IN...".format(target_name))

        # Countdown timer
        @minqlx.delay(2)
        @minqlx.thread
        def countdown():
            for index in range(5, 0, -1):
                self.center_print("^1" + str(index) + "..")
                time.sleep(1)
            if msg[1] != "everyone":
                self.player(i).position(x=-10000, y=-10000, z=-10000)
            else:
                for p in self.players():
                    self.player(p.id).position(x=-10000, y=-10000, z=-10000)
        countdown()

    def cmd_gay(self, player, msg, channel):
        self.callvote('qlx !gayall', "make everyone gay")

    def cmd_gayall(self, player, msg, channel):
        for p in self.players():
            p.clan = "^6*GAY*"

    def cmd_straight(self, player, msg, channel):
        self.callvote('qlx !straightall', "make everyone straight")

    def cmd_straightall(self, player, msg, channel):
        for p in self.players():
            p.clan = ""

    def cmd_kill(self, player, msg, channel):
        self.callvote('qlx !killall', "kill everyone")

    def cmd_killall(self, player, msg, channel):
        for p in self.players():
            self.slay(p)

    def cmd_slapvote(self, player, msg, channel):
        if msg[1] != "everyone":
            try:
                i = int(msg[1])
                target_player = self.player(i)
                if not (0 <= i < 64) or not target_player:
                    raise ValueError
            except ValueError:
                player.tell("Invalid ID.")
                return minqlx.RET_STOP_ALL

        try:
            msg[2]
        except:
            #default values
            msg.append(100) #number of slaps
            msg.append(0.25) #slap frequency

        if msg[1] == "everyone":
            first_arg = target_player_string = "everyone"
        else:
            target_player_string = target_player.name
            first_arg = int(msg[1])

        self.callvote('qlx !slaptrigger {} {} {}'.format(first_arg, int(msg[2]), float(msg[3])), "Slaphappy {}".format(target_player_string))

    def cmd_slaphappy(self, player, msg, channel):
        if len(msg) < 4:
            return minqlx.RET_USAGE

        if msg[1] != "everyone":
            try:
                i = int(msg[1])
                target_player = self.player(i)
                target_name = target_player.name
                if not (0 <= i < 64) or not target_player:
                    raise ValueError
            except ValueError:
                player.tell("Invalid ID.")
                return minqlx.RET_STOP_ALL
        else:
            target_name = "EVERYONE"

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

        def do_every(interval, worker_func, iterations=0):
            if not self.game_ended:
                if iterations != 1:
                    threading.Timer(
                        interval,
                        do_every, [interval, worker_func, 0 if iterations == 0 else iterations - 1]
                    ).start()
                worker_func()

        def slapper():
            if target_name != "EVERYONE":
                self.slap(target_player, dmg)
            else:
                for p in self.players():
                    self.slap(p, dmg)

        self.center_print("^2SLAPHAPPY ACTIVATED ON: ^6{}^7 !!! IN...".format(target_name))

        # Countdown timer
        @minqlx.delay(2)
        @minqlx.thread
        def countdown():
            for i in range(5, 0, -1):
                self.center_print("^1" + str(i) + "..")
                time.sleep(1)
            do_every(slap_frequency, slapper, slap_amount)

        countdown()

        return minqlx.RET_STOP_ALL


