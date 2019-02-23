import minqlx

class gay(minqlx.Plugin):

    def __init__(self):

        self.add_command("gay", self.cmd_gay)
        self.add_command("gayall", self.cmd_gayall, 5)
        self.add_command("straight", self.cmd_straight)
        self.add_command("straightall", self.cmd_straightall, 5)
        self.add_command("kill", self.cmd_kill)
        self.add_command("killall", self.cmd_killall, 5)

    def cmd_gay(self, player, msg, channel):
        self.callvote('qlx !gayall', "make everyone gay")

    def cmd_gayall(self, player, msg, channel):
        for p in self.players():
            p.clan = "^6*GAY*"
            
    def cmd_straight(self, player, msg, channel):
        self.callvote('qlx !straightall', "make everyone straight")

    def cmd_straightall(self, player, msg, channel):
        for p in self.players():
            p.clan = ""
