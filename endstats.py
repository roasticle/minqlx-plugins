import minqlx
import time

class endstats(minqlx.Plugin):

    def __init__(self):
        self.add_hook("stats", self.handle_stats)
        self.add_hook("game_start", self.handle_game_start)
        self.add_hook("game_end", self.handle_game_end)

        self.best_kpm_names = []
        self.best_kpm = 0

        self.best_kd_names = []
        self.best_kd = 0

        self.most_damage_names = []
        self.most_damage = 0

        self.longest_spree_names = []
        self.longest_spree = 0

        self.most_pummels_names = []
        self.most_pummels = 0

        self.most_dmg_taken_names = []
        self.most_dmg_taken = 0

        self.world_death_types = ["UNKNOWN", "WATER", "SLIME", "LAVA", "CRUSH", "FALLING", "TRIGGER_HURT", "HURT"]
        self.world_death_stats = {}
        self.most_world_deaths_names = []
        self.most_world_deaths = 0

    def handle_stats(self, stats):
        if stats['TYPE'] == "PLAYER_DEATH" and self.game.state == "in_progress" and stats['DATA']['MOD'] in self.world_death_types:
            if stats['DATA']['VICTIM']['NAME'] not in self.world_death_stats:
                self.world_death_stats.update({stats['DATA']['VICTIM']['NAME'] : 1})
            else:
                self.world_death_stats[stats['DATA']['VICTIM']['NAME']] += 1

        if stats['TYPE'] == "PLAYER_STATS":
            #these stats come at end of game after MATCH_REPORT for each player
            if stats['DATA']['QUIT'] == 0 and stats['DATA']['WARMUP'] == 0:
                player_name = stats['DATA']['NAME']

                if stats['DATA']['PLAY_TIME'] > 0:
                    player_kpm = stats['DATA']['KILLS'] / (stats['DATA']['PLAY_TIME'] / 60)
                else:
                    player_kpm = 0

                if stats['DATA']['DEATHS'] != 0: #we don't want to divide by 0!
                    player_kd = stats['DATA']['KILLS'] / stats['DATA']['DEATHS']
                else:
                    player_kd = stats['DATA']['KILLS']
                player_dmg = stats['DATA']['DAMAGE']['DEALT']
                
                player_longest_spree = stats['DATA']['MAX_STREAK'] 
                player_pummels = stats['DATA']['WEAPONS']['GAUNTLET']['K']                
                player_dmg_taken = stats['DATA']['DAMAGE']['TAKEN']

                if not self.best_kpm_names:
                    self.best_kpm_names = [player_name]
                    self.best_kpm = player_kpm
                elif player_kpm > self.best_kpm:
                    self.best_kpm_names = [player_name]
                    self.best_kpm = player_kpm
                elif player_kpm == self.best_kpm:
                    self.best_kpm_names.append(player_name)

                if not self.best_kd_names:
                    self.best_kd_names = [player_name]
                    self.best_kd = player_kd
                elif player_kd > self.best_kd:
                    self.best_kd_names = [player_name]
                    self.best_kd = player_kd
                elif player_kd == self.best_kd:
                    self.best_kd_names.append(player_name)

                if not self.most_damage_names:
                    self.most_damage_names = [player_name]
                    self.most_damage = player_dmg
                elif player_dmg > self.most_damage:
                    self.most_damage_names = [player_name]
                    self.most_damage = player_dmg
                elif player_dmg == self.most_damage:
                    self.most_damage_names.append(player_name)
                    
                if not self.longest_spree:
                    self.longest_spree_names = [player_name]
                    self.longest_spree = player_longest_spree
                elif player_longest_spree > self.longest_spree:
                    self.longest_spree_names = [player_name]
                    self.longest_spree = player_longest_spree
                elif player_longest_spree == self.longest_spree:
                    self.longest_spree_names.append(player_name)    

                if not self.most_pummels_names:
                    self.most_pummels_names = [player_name]
                    self.most_pummels = player_pummels
                elif player_pummels > self.most_pummels:
                    self.most_pummels_names = [player_name]
                    self.most_pummels = player_pummels
                elif player_pummels == self.most_pummels:
                    self.most_pummels_names.append(player_name)
                    
                if not self.most_dmg_taken_names:
                    self.most_dmg_taken_names = [player_name]
                    self.most_dmg_taken = player_dmg_taken
                elif player_dmg_taken > self.most_dmg_taken:
                    self.most_dmg_taken_names = [player_name]
                    self.most_dmg_taken = player_dmg_taken
                elif player_dmg_taken == self.most_dmg_taken:
                    self.most_dmg_taken_names.append(player_name)    

    @minqlx.delay(2)
    @minqlx.thread
    def handle_game_end(self, data):
        if not data["ABORTED"]:
            stats_output = "^1KILL MACHINE: "
            for i, player_name in enumerate(self.best_kpm_names):
                stats_output += "^7" + player_name
                if len(self.best_kpm_names) > 1 and len(self.best_kpm_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:0.2f} kills/min".format(self.best_kpm)
            self.msg(stats_output)

            stats_output = "^1BEST COUNTERSTRIKE PLAYER: "
            for i, player_name in enumerate(self.best_kd_names):
                stats_output += "^7" + player_name
                if len(self.best_kd_names) > 1 and len(self.best_kd_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:0.2f} K/D ratio".format(self.best_kd)
            self.msg(stats_output)

            stats_output = "^1DESTRUCTICATOR: "
            for i, player_name in enumerate(self.most_damage_names):
                stats_output += "^7" + player_name
                if len(self.most_damage_names) > 1 and len(self.most_damage_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:,} dmg given".format(self.most_damage)

            self.msg(stats_output)
            time.sleep(3)

            if self.longest_spree > 1:
                stats_output = "^1RAMBO: "
                for i, player_name in enumerate(self.longest_spree_names):
                    stats_output += "^7" + player_name
                    if len(self.longest_spree_names) > 1 and len(self.longest_spree_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {} kill streak".format(self.longest_spree)
                self.msg(stats_output)

            if self.most_pummels > 0:
                stats_output = "^1PUMMEL LORD: "
                for i, player_name in enumerate(self.most_pummels_names):
                    stats_output += "^7" + player_name
                    if len(self.most_pummels_names) > 1 and len(self.most_pummels_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {} pummels".format(self.most_pummels)
                self.msg(stats_output)

            stats_output = "^6BIGGEST PINCUSHION: "
            for i, player_name in enumerate(self.most_dmg_taken_names):
                stats_output += "^7" + player_name
                if len(self.most_dmg_taken_names) > 1 and len(self.most_dmg_taken_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:,} ^6dmg taken".format(self.most_dmg_taken)
            self.msg(stats_output)

            time.sleep(2)

            stats_output = "^6CLUMSIEST FOOL: "
            for name, world_deaths in self.world_death_stats.items():
                if not self.most_world_deaths_names:
                    self.most_world_deaths_names = [name]
                    self.most_world_deaths = world_deaths
                elif player_kpm > self.most_world_deaths:
                    self.most_world_deaths_names = [name]
                    self.most_world_deaths = world_deaths
                elif player_kpm == self.most_world_deaths:
                    self.most_world_deaths_names.append(name)

            if self.most_world_deaths > 0:
                for i, player_name in enumerate(self.most_world_deaths_names):
                    stats_output += "^7" + player_name
                    if len(self.most_world_deaths_names) > 1 and len(self.most_world_deaths_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {:,} deaths by world".format(self.most_world_deaths)
                self.msg(stats_output)

    def handle_game_start(self, data):
        self.best_kpm_names = []
        self.best_kpm = 0

        self.best_kd_names = []
        self.best_kd = 0

        self.most_damage_names = []
        self.most_damage = 0

        self.most_pummels_names = []
        self.most_pummels = 0

        self.most_dmg_taken_names = []
        self.most_dmg_taken = 0

        self.world_death_stats = {}
        self.most_world_deaths_names = []
        self.most_world_deaths = 0
