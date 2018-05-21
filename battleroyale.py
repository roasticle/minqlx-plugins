import minqlx

class battleroyale(minqlx.Plugin):

    def __init__(self):
        self.initial_teamsize = self.get_cvar("teamsize")

        self.add_command("battleroyale", self.cmd_battleroyale)
        self.add_command("startbattleroyale", self.cmd_start_battleroyale, 5)

    def cmd_battleroyale(self, player, msg, channel):
        self.callvote('qlx !startbattleroyale', "^1BATTLEROYALE^7")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_start_battleroyale(self, player, msg, channel):
        self.center_print("^1PREPARE FOR BATTLEROYALE!")
        self.start_br()

    @minqlx.delay(2)
    def start_br(self):
        self.game.abort()

        self.set_cvar("teamsize", len(self.teams()["free"]))
        self.set_cvar("g_startingHealth", 200)
        self.set_cvar("g_startingArmor", 200)

        self.add_hook("stats", self.handle_stats)
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.add_hook("team_switch_attempt", self.handle_team_switch_attempt)
        self.add_hook("game_end", self.handle_game_end)
        self.all_ready()

    @minqlx.delay(2)
    def all_ready(self):
        minqlx.console_command("allready")

    def handle_player_disconnect(self, player):
        if player.team == "free":
            self.reduce_teamsize()

    def handle_stats(self, stats):
        if stats['TYPE'] == "PLAYER_DEATH":
            if self.game.state == "in_progress":
                #if player is bot lookup player by name, otherwise use steam id
                if stats['DATA']['VICTIM']['BOT']:
                    player = self.player(stats['DATA']['VICTIM']['NAME'])
                else:
                    player = self.player(int(stats['DATA']['VICTIM']['STEAM_ID']))

                self.reduce_teamsize()
                player.team = "spectator"

                if len(self.teams()["free"]) == 2:
                    vs_msg = "{} ^1vs ^7{} ^1!".format(self.teams()["free"][0], self.teams()["free"][1])
                    self.center_print(vs_msg)
                    self.msg(vs_msg)

    def handle_team_switch_attempt(self, player, old_team, new_team):
        self.set_cvar("teamsize", len(self.teams()["free"]))

    def handle_game_end(self, data):
        self.msg("^1BATTLEROYALE WINNER!: {}".format(self.teams()["free"][0]))

        self.set_cvar("teamsize", self.initial_teamsize)
        self.set_cvar("g_startingHealth", 100)
        self.set_cvar("g_startingArmor", 0)

        self.remove_hook("stats", self.handle_stats)
        self.remove_hook("player_disconnect", self.handle_player_disconnect)
        self.remove_hook("team_switch_attempt", self.handle_team_switch_attempt)
        self.remove_hook("game_end", self.handle_game_end)

    def reduce_teamsize(self):
        if(int(self.get_cvar("teamsize")) - 1 != 0):
            self.set_cvar("teamsize", int(self.get_cvar("teamsize")) - 1)




