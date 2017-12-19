import minqlx

class roasted(minqlx.Plugin):

    def __init__(self):
        self.yes_votes = 0

        self.add_command("centerprint", self.cmd_centerprint, 2)
        self.add_command("jihad", self.cmd_jihad)
        self.add_command("models", self.cmd_models)
        self.add_command("customsounds", self.cmd_custom_sounds)
        self.add_command("kickbots", self.cmd_kickbots)
        self.add_command("addbots", self.cmd_addbots)
        self.add_command("customvote", self.cmd_custom_vote, 5)

        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("new_game", self.handle_new_game)
        self.add_hook("vote", self.handle_vote)
        self.add_hook("vote_ended", self.handle_vote_ended)
        self.add_hook("team_switch_attempt", self.handle_team_switch_attempt)
        self.add_hook("player_disconnect", self.handle_player_disconnect)

    #CMD TRIGGERS

    def cmd_centerprint(self, player, msg, channel):
        message_string = ""
        for i in range(1, len(msg)): message_string += str(msg[i]) + " "
        self.center_print(message_string)

    def cmd_jihad(self, player, msg, channel):
        self.msg("^1Allah's Commands: ^2!elo !elos !weather !alias !motd !nextmap !info !victorysongs !victorysong")
        self.msg("^2!kickbots !addbots !sounds !currentmap !gungames !customsounds !listmaps !models !stats")

    def cmd_models(self, player, msg, channel):
        self.msg("^1Available models - ^3Type /model modelname in console!: ^2sonic tis supermario supermario/luigi snoopy neo mrburns clippy bender alig legoman marvin spongebob pilsbury")

    def cmd_custom_sounds(self, player, msg, channel):
        self.msg("^1Custom sounds: ^2!crash !elmo !shiet doh inconceivable !choppa !illbeback !inigo !hasta !leeroy !chicken !duke [optional sound] !burns !alrighty !giggity !meal")

    def cmd_kickbots(self, caller, msg, channel):
        if self.game.type != "Duel":
            if self.human_count_in_game() >= 5:
                self.msg("^1There are no bots currently!")
            else:
                self.callvote('bot_minplayers 1', "kick bots")
                self.msg("{}^7 called a vote.".format(caller.name))
                if(self.human_count_in_game() == 1): self.force_vote(True)
                else: self.msg("NOTE: ^1YOU STILL NEED TO PRESS ^7F1 IF YOU CALLED THIS VOTE!!!")

    def cmd_addbots(self, caller, msg, channel):
        if self.game.type != "Duel":
            if self.human_count_in_game() >= 5:
                self.msg("^1Players must be less than 5 to add bots!")
            else:
                self.callvote('bot_minplayers 5', "add bots")
                self.msg("{}^7 called a vote.".format(caller.name))
                if(self.human_count_in_game() == 1): self.force_vote(True)
                else: self.msg("NOTE: ^1YOU STILL NEED TO PRESS ^7F1 IF YOU CALLED THIS VOTE!!!")

    def cmd_custom_vote(self, caller, msg, channel):
        vote_question, vote_passed_message = " ".join(msg[1:]).split(',')
        self.callvote('qlx !centerprint {}'.format("^5VOTE PASSED! ^6" + vote_passed_message.upper()), vote_question)
        self.msg("{}^7 called a vote.".format(caller.name))

    #HOOK HANDLES

    def handle_new_game(self, *args, **kwargs):
        #WeaponSpawnFixer warmup load
        minqlx.force_weapon_respawn_time(int(self.get_cvar("g_weaponrespawn")))
        @minqlx.delay(2)
        def delayed_thing():
            minqlx.force_weapon_respawn_time(int(self.get_cvar("g_weaponrespawn")))
            if self.game.type not in ["Duel", "Instagib"]:
                self.delayed_bot_reset()
        delayed_thing()
        self.map_reset_check()

    def handle_game_start(self, *args, **kwargs):
        #WeaponSpawnFixer game start
        minqlx.force_weapon_respawn_time(int(self.get_cvar("g_weaponrespawn")))
        @minqlx.delay(2)
        def delayed_thing():
            minqlx.force_weapon_respawn_time(int(self.get_cvar("g_weaponrespawn")))
        delayed_thing()

    def handle_vote(self, player, yes):
        if yes:
            self.yes_votes += 1
            if self.yes_votes / self.human_count_in_game() > 0.5:
                self.force_vote(True)
    
    def handle_vote_ended(self, *args, **kwargs):
        self.yes_votes = 0

    def handle_team_switch_attempt(self, player, old_team, new_team):
        if self.game.type not in ["Duel", "Instagib"]:
            self.delayed_bot_reset()
        self.map_reset_check()

    def handle_player_disconnect(self, player, reason):
        if self.game.type not in ["Duel", "Instagib"]:
            self.delayed_bot_reset()
        self.map_reset_check()

    #delayed because of team switch not being instant
    @minqlx.delay(1)
    def delayed_bot_reset(self):
        if self.human_count_in_game() <= 1:
            self.set_cvar("bot_minplayers", 5)

    #UTILITY FUNCTIONS

    @minqlx.delay(1)
    def map_reset_check(self):
        if self.human_count_in_game() == 0 and self.game.map != "xmasasylum": #change to bloodrun if not on bloodrun and no human players in-game
            self.change_map("xmasasylum", self.game.factory)

    def human_count(self, *args, **kwargs):
        human_count = 0

        for p in self.players():
            if(str(p.steam_id)[0] != "9"): #not a bot
                human_count += 1

        return human_count

    #needs delay or else gets count before team/spec change
    def human_count_in_game(self, *args, **kwargs):
        human_count_in_game = 0

        for p in self.teams()['free']:
            if(str(p.steam_id)[0] != "9"): #not a bot
                human_count_in_game += 1

        return human_count_in_game
