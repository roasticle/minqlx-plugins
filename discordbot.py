import minqlx
import time

class endstats(minqlx.Plugin):

    def __init__(self):
        self.add_hook("stats", self.handle_stats)
        self.add_hook("game_end", self.handle_game_end)

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

    def handle_stats(self, stats):
        if stats['TYPE'] == "PLAYER_STATS": #these stats come at end of game after MATCH_REPORT
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

                player_pummels = stats['DATA']['WEAPONS']['GAUNTLET']['K']
                player_dmg = stats['DATA']['DAMAGE']['DEALT']
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

    @minqlx.delay(1)
    @minqlx.thread
    def handle_game_end(self, *args, **kwargs):
        if self.most_damage: #avoids stats on aborts (picked arbitrary stat)
            stats_output = "^1MOST KILLS/MIN: "
            for i, player_name in enumerate(self.best_kpm_names):
                stats_output += "^7" + player_name
                if len(self.best_kpm_names) > 1 and len(self.best_kpm_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:0.2f}".format(self.best_kpm)
            self.msg(stats_output)

            stats_output = "^1BEST K/D RATIO: "
            for i, player_name in enumerate(self.best_kd_names):
                stats_output += "^7" + player_name
                if len(self.best_kd_names) > 1 and len(self.best_kd_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:0.2f}".format(self.best_kd)
            self.msg(stats_output)

            stats_output = "^1MOST DAMAGE: "
            for i, player_name in enumerate(self.most_damage_names):
                stats_output += "^7" + player_name
                if len(self.most_damage_names) > 1 and len(self.most_damage_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:,}".format(self.most_damage)

            self.msg(stats_output)
            time.sleep(3)

            if self.most_pummels > 0:
                stats_output = "^1MOST PUMMELS: "
                for i, player_name in enumerate(self.most_pummels_names):
                    stats_output += "^7" + player_name
                    if len(self.most_pummels_names) > 1 and len(self.most_pummels_names) - 1 != i:
                        stats_output += ", "
                stats_output += "^2 - {}".format(self.most_pummels)
                self.msg(stats_output)

            stats_output = "^6BIGGEST PINCUSHION: "
            for i, player_name in enumerate(self.most_dmg_taken_names):
                stats_output += "^7" + player_name
                if len(self.most_dmg_taken_names) > 1 and len(self.most_dmg_taken_names) - 1 != i:
                    stats_output += ", "
            stats_output += "^2 - {:,} ^6dmg taken".format(self.most_dmg_taken)

            self.msg(stats_output)

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
