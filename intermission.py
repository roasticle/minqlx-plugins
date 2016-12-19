import minqlx

class intermission(minqlx.Plugin):

    def __init__(self):
        self.add_hook("game_end", self.handle_game_end)

    def handle_game_end(self, *args, **kwargs):
        self.play_sound(self.get_cvar("qlx_intermissionSound"))
