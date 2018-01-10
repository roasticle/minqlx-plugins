import minqlx

class ragespec(minqlx.Plugin):

    def __init__(self):
        self.add_command("ragespec", self.cmd_ragespec)

    def cmd_ragespec(self, player, msg, channel):
        if self.game.state == "in_progress" and player.team != "spectator":
            player.put("spectator")
            self.msg("{} ^1ragespecs".format(player.name))
