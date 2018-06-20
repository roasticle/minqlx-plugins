import minqlx

PLAYER_KEY = "minqlx:players:{}"

class qltv(minqlx.Plugin):

    def __init__(self):
        self.spec_index = 0
        self.last_spec_steam_id = None
        self.sorted_players = ""

        self.add_command("qltv", self.cmd_qltv)
        self.add_command("qltvjoin", self.cmd_qltvjoin)

        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("stats", self.handle_stats)

    def handle_game_start(self, data):
        self.spec_index = 0
        self.speccer()

    def handle_stats(self, stats):
        if self.game is not None:
            if self.game.state == "in_progress":
                if stats['TYPE'] == "PLAYER_KILL":
                    if self.game.red_score % 10 == 0:
                        self.speccer()

    @minqlx.delay(1)
    def speccer(self):
        if self.game.state == "in_progress":
            self.sorted_players = sorted(self.players(), key = lambda p: p.stats.score, reverse=True)

            if self.sorted_players[self.spec_index].steam_id == self.last_spec_steam_id:
                if self.spec_index + 1 == 3:
                    self.spec_index = 0
                else:
                    self.spec_index += 1

            for player in self.teams()['spectator']:
                player_spec_setting = self.db.get(PLAYER_KEY.format(player.steam_id) + ":qltv")

                if player_spec_setting:
                    if int(player_spec_setting) == 1:
                        minqlx.client_command(player.id, 'follow ' + str(self.sorted_players[self.spec_index].id))

            self.last_spec_steam_id = self.sorted_players[self.spec_index].steam_id

            if self.spec_index == 2:
                self.spec_index = 0
            else:
                self.spec_index += 1

    def cmd_qltv(self, player, msg, channel):
        current_qltv_setting = self.db.get(PLAYER_KEY.format(player.steam_id) + ":qltv")
        new_qltv_setting = 0

        if current_qltv_setting:
            current_qltv_setting = int(current_qltv_setting)
        else:
            current_qltv_setting = 0

        if current_qltv_setting == 0:
            player.tell('^5***QLTV HAS BEEN ENABLED***')
            new_qltv_setting = 1
        elif current_qltv_setting == 1:
            player.tell('^5***QLTV HAS BEEN DISABLED***')
            new_qltv_setting = 0

        self.db.set(PLAYER_KEY.format(player.steam_id) + ":qltv", new_qltv_setting)

    def cmd_qltvjoin(self, player, msg, channel):
        self.db.set(PLAYER_KEY.format(player.steam_id) + ":qltv", 1)
        minqlx.client_command(player.id, 'follow ' + str(self.sorted_players[self.spec_index].id))


