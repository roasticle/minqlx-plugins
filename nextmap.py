import minqlx
import random

class nextmap(minqlx.Plugin):

    def __init__(self):
        self.add_command("nextmap", self.cmd_nextmap)
        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("game_end", self.handle_game_end)
        self.set_cvar_once("qlx_nextmap_no-repeat", "")

    def cmd_nextmap(self, player, msg, channel):
        nextmap_string = self.get_nextmap()
        if nextmap_string: self.msg("^1Next map: ^2{}".format(nextmap_string))
        else: self.msg("^Next map is not set.")

    def handle_game_end(self, *args, **kwargs):
        nextmap_string = self.get_nextmap()
        if nextmap_string: self.msg("^1Next map: ^2{}".format(nextmap_string))

    def handle_game_start(self, *args, **kwargs):
        if self.get_cvar("qlx_nextmap_no-repeat"):
            #Check if nextmap is the same as the current map, if so, we need to pick a new map from mappool
            nextmap = self.get_nextmap()
            if nextmap == "{} {}".format(self.get_cvar("mapname"), self.get_cvar("g_factory")):
                new_nextmap = self.get_random_map(nextmap)
                self.set_cvar("nextmap", "map {}".format(new_nextmap))

    def get_nextmap(self):
        return self.get_cvar("nextmap").replace("map ", "")

    def get_random_map(self, nextmap):
        mappool = self.plugins['essentials'].mappool
        map_name = random.choice(list(mappool))
        factory = mappool.get(map_name)[0]
        new_nextmap = "{} {}".format(map_name, factory)
        #If new nextmap is the same as the current nextmap, we need to get another random map until we find a different one (the joys of "random"!)
        while new_nextmap == nextmap:
            new_nextmap = self.get_random_map(nextmap)
        return new_nextmap
