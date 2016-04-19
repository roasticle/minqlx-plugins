import minqlx
import time

class bot_antispec(minqlx.Plugin):
    def __init__(self):
        super().__init__()
        self.add_hook("player_connect", self.handle_player_connect, priority=minqlx.PRI_LOWEST)

    @minqlx.thread
    def handle_player_connect(self, player):
        if(str(player.steam_id)[0] == "9"):
            time.sleep(5)
            for p in self.teams()['spectator']:
                if(str(p.steam_id)[0] == "9"):
                    self.kick(p)

