import minqlx

class weaponspawnfixer(minqlx.Plugin):

    def __init__(self):

        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("new_game", self.handle_new_game)

    @minqlx.delay(2)
    def handle_new_game(self, *args, **kwargs):
        minqlx.force_weapon_respawn_time(int(self.get_cvar("g_weaponrespawn")))

    @minqlx.delay(2)
    def handle_game_start(self, *args, **kwargs):
        minqlx.force_weapon_respawn_time(int(self.get_cvar("g_weaponrespawn")))
