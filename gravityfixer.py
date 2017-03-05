import minqlx

class gravityfixer(minqlx.Plugin):

    def __init__(self):
        self.add_hook("new_game", self.handle_new_game)

    def handle_new_game(self, *args, **kwargs):
        if self.get_cvar("mapname") not in self.get_cvar("qlx_alternateGravityMaps", list):
            self.set_cvar("g_gravity", "800")
