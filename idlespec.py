
import minqlx

class idlespec(minqlx.Plugin):
    
    def __init__(self):        
        self.add_hook("player_inactivity_kick", self.handle_inactivity_kick)
        
    def handle_inactivity_kick(self, p):
        p.put("spectator")
        return minqlx.RET_STOP_EVENT
