import minqlx

class intermission(minqlx.Plugin):

    def __init__(self):
        self.plugin_updater_url = "https://raw.githubusercontent.com/roasticle/minqlx-plugins/master/intermission.py"
        self.add_hook("game_end", self.handle_game_end)

    def handle_game_end(self, *args, **kwargs):
        self.play_sound(self.get_cvar("qlx_intermissionSound"))