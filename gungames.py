import minqlx

class gungames(minqlx.Plugin):

    def __init__(self):
        super().__init__()
        self.add_command("gungames", self.cmd_gungames)
        self.add_command("glovelove", self.cmd_glovelove)
        self.add_command("mgs", self.cmd_mgs)
        self.add_command("shotties", self.cmd_shotties)
        self.add_command("nades", self.cmd_nades)
        self.add_command("rockets", self.cmd_rockets)
        self.add_command("lgs", self.cmd_lgs)
        self.add_command("rails", self.cmd_rails)
        self.add_command("plasmas", self.cmd_plasmas)
        self.add_command("bfgs", self.cmd_bfgs)
        self.add_command("nails", self.cmd_nails)
        self.add_command("mines", self.cmd_mines)
        self.add_command("chainguns", self.cmd_chainguns)

    def cmd_gungames(self, player, msg, channel):
        self.msg("^1Gungames: ^5!glovelove !mgs !shotties !nades !rockets !lgs !rails !plasmas !bfgs !nails !mines !chainguns")

    def cmd_glovelove(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " guantlets-ffa", "guantlet only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_mgs(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " mg-ffa", "mg only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_shotties(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " shotguns-ffa", "shotguns only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_nades(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " nades-ffa", "nades only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_rockets(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " rockets-ffa", "rockets only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_lgs(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " lg-ffa", "lg only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_rails(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " rail-ffa", "rail only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_plasmas(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " plasma-ffa", "plasma only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_bfgs(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " bfg-ffa", "bfg only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_nails(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " nail-ffa", "nailguns only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_mines(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " prox-ffa", "mines only")
        self.msg("{}^7 called a vote.".format(caller.name))

    def cmd_chainguns(self, caller, msg, channel):
        self.callvote("map " + self.get_cvar("mapname") + " chain-ffa", "chainguns only")
        self.msg("{}^7 called a vote.".format(caller.name))
