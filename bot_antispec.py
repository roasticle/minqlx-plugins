import minqlx

class bot_antispec(minqlx.Plugin):
    def __init__(self):
        self.add_hook("player_connect", self.handle_player_connect)

    def handle_player_connect(self, player):
        #Need to delay 2 second to allow bot to connect and go into spec or else a bot setup error or kick loop will occur
        @minqlx.delay(2)
        def delayed_thing():
            if(str(player.steam_id)[0] == "9"): #bot steam id's start with a 9
                for p in self.teams()['spectator']:
                    if player.steam_id == p.steam_id:
                        self.kick(p)
        delayed_thing()
