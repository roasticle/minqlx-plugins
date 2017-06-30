import minqlx
import requests
import json
import threading
import socket

class discordbot(minqlx.Plugin):

    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.set_cvar_once("qlx_discord_channel_id", "")
        self.set_cvar_once("qlx_discord_bot_token", "")

        self.server_ip = s.getsockname()[0]
        self.last_message_id = ""
        self.discord_channel_id = self.get_cvar("qlx_discord_channel_id")
        self.discord_bot_token = self.get_cvar("qlx_discord_bot_token")

        self.add_hook("game_end", self.handle_game_end)

        @minqlx.delay(20)
        def stats_timer():
                threading.Timer(180, stats_timer).start()
                self.send_stats()

        if not self.discord_channel_id:
            self.msg("^3You need to set qlx_discord_channel_id.")
            return minqlx.RET_STOP_ALL
        elif not self.discord_bot_token:
            self.msg("^3You need to set qlx_discord_bot_token.")
            return minqlx.RET_STOP_ALL
        else:
            stats_timer()

    @minqlx.thread
    def send_stats(self, end_game = False):

        game_ended_text = ""

        if end_game:
            game_ended_text = " - **Game Ended!**"

        content = "{} - ".format(self.game.hostname)
        content += "**Map:** {} ({}) - ".format(self.game.map_title, self.game.map)
        content += "**Players:** {}\{} ({} bots - {} spec){}\n".format(len(self.teams()['free']), self.game.teamsize, self.bot_count_in_game(), len(self.teams()['spectator']), game_ended_text)
        content += self.player_data()

        #content += " [Join server](steam://connect/{}:{})".format(self.server_ip, self.get_cvar("net_port")) #markdown isnt currently working in discord :|
        content += " steam://connect/{}:{}".format(self.server_ip, self.get_cvar("net_port"))

        if self.last_message_id:
            requests.delete("https://discordapp.com/api/channels/" +  self.discord_channel_id + "/messages/" + self.last_message_id,
                             headers = {'Content-type': 'application/json', 'Authorization': 'Bot ' + self.discord_bot_token})

        last_message = requests.post("https://discordapp.com/api/channels/" +  self.discord_channel_id + "/messages",
                                    data=json.dumps({'content': content}),
                                    headers = {'Content-type': 'application/json', 'Authorization': 'Bot ' + self.discord_bot_token})

        self.last_message_id = json.loads(last_message.text)['id']

    def handle_game_end(self, *args, **kwargs):
        self.send_stats(True)

    def player_data(self, *args, **kwargs):
        player_data = ""
        players_by_score = sorted(self.teams()['free'] + self.teams()['blue'] + self.teams()['red'], key=lambda k: k.score, reverse=True)[:5] #get top 5 players list!

        for p in players_by_score:
            player_time = 0
            if self.game.state == "in_progress":
                player_time = int(p.stats.time / 60000)
            player_data += "**{}**: {} ({}m)- ".format(self.clean_text(p.name), p.score, player_time)

        return player_data

    def bot_count_in_game(self, *args, **kwargs):
        bot_count_in_game = 0

        for p in self.teams()['free'] + self.teams()['blue'] + self.teams()['red']:
            if(str(p.steam_id)[0] == "9"): # a bot
                bot_count_in_game += 1

        if self.human_count_in_game() >= 5: #handles cases when bots haven't been kicked yet when loading new maps
            bot_count_in_game = 0

        return bot_count_in_game

    def human_count_in_game(self, *args, **kwargs):
        human_count_in_game = 0

        for p in self.teams()['free'] + self.teams()['blue'] + self.teams()['red']:
            if(str(p.steam_id)[0] != "9"): # a human!
                human_count_in_game += 1

        return human_count_in_game




