import minqlx

PLAYER_KEY = "minqlx:players:{}"

class qltv(minqlx.Plugin):

    def __init__(self):
        self.kill_threshold_hit = 0
        self.last_spec_steam_id = None
        self.sorted_players = ""

        self.add_command("qltv", self.cmd_qltv)

        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("new_game", self.handle_new_game)
        self.add_hook("stats", self.handle_stats)
        self.add_hook("player_connect", self.handle_player_connect)
        self.add_hook("player_disconnect", self.handle_player_disconnect)
        self.add_hook("team_switch_attempt", self.handle_team_switch_attempt)

    def handle_game_start(self, *args, **kwargs):
        self.kill_threshold_hit = 0
        self.speccer()

    def handle_new_game(self):
        self.kill_threshold_hit = 0
        self.speccer()

    def handle_stats(self, stats):
        if self.game is not None:
            if self.game.state == "in_progress":
                if stats['TYPE'] == "PLAYER_KILL":
                    if self.game.red_score % 10 == 0 and self.kill_threshold_hit != self.game.red_score:
                        self.kill_threshold_hit = self.game.red_score
                        self.speccer()

    @minqlx.delay(3)
    def speccer(self):
        self.sorted_players = sorted(self.teams()['free'], key = lambda p: p.stats.score, reverse=True)

        for player in self.teams()['spectator']:
            self.check_and_spec(player)

        if self.sorted_players:    
            self.last_spec_steam_id = self.sorted_players[0].steam_id

    def check_and_spec(self, player):
        player_spec_setting = self.db.get(PLAYER_KEY.format(player.steam_id) + ":qltv")

        if player_spec_setting:
            if int(player_spec_setting) == 1 and self.sorted_players:
                minqlx.client_command(player.id, 'follow ' + str(self.sorted_players[0].id))

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
        self.check_and_spec(player)

    @minqlx.delay(3)
    def handle_player_connect(self, player):
        self.check_and_spec(player)

    def handle_player_disconnect(self, player, reason):
        self.speccer()

    def handle_team_switch_attempt(self, player, old_team, new_team):
        if player.steam_id == self.last_spec_steam_id and new_team == "spectator":
            self.speccer()
