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
        self.set_cvar_once("qlx_discord_chat_channel_id", "")
        self.set_cvar_once("qlx_discord_bot_token", "")

        self.server_ip = s.getsockname()[0]
        self.last_message_id = ""
        self.last_polled_message_id = ""
        self.discord_channel_id = self.get_cvar("qlx_discord_channel_id")
        self.discord_chat_channel_id = self.get_cvar("qlx_discord_chat_channel_id")
        self.discord_bot_token = self.get_cvar("qlx_discord_bot_token")

        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("chat", self.handle_chat)

        if self.discord_chat_channel_id:
            def poll_discord_messages_timer():
                threading.Timer(1, poll_discord_messages_timer).start()
                self.poll_discord_messages()
            poll_discord_messages_timer()

        @minqlx.delay(20)
        def stats_timer():
            threading.Timer(180, stats_timer).start()
            self.send_stats()

        if not self.discord_channel_id:
            self.msg("^3You need to set qlx_discord_channel_id.")
        elif not self.discord_bot_token:
            self.msg("^3You need to set qlx_discord_bot_token.")
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
        content += " steam://connect/{}:{}".format(self.server_ip, self.get_cvar("net_port"))

        #handle last message deletion
        #if not self.last_message_id:
        last_50_messages = requests.get("https://discordapp.com/api/channels/" +  self.discord_channel_id + "/messages",
                                        headers = {'Content-type': 'application/json', 'Authorization': 'Bot ' + self.discord_bot_token})
        last_50_messages = json.loads(last_50_messages.text)

        for message in last_50_messages:
            if self.game.hostname in message["content"]:
                self.last_message_id = message["id"]

        if self.last_message_id:
            requests.delete("https://discordapp.com/api/channels/" +  self.discord_channel_id + "/messages/" + self.last_message_id,
                             headers = {'Content-type': 'application/json', 'Authorization': 'Bot ' + self.discord_bot_token})

        last_message = requests.post("https://discordapp.com/api/channels/" +  self.discord_channel_id + "/messages",
                                    data=json.dumps({'content': content}),
                                    headers = {'Content-type': 'application/json', 'Authorization': 'Bot ' + self.discord_bot_token})

        self.last_message_id = json.loads(last_message.text)['id']


    def handle_game_end(self, *args, **kwargs):
        self.send_stats(True)

    #Sends chat to discord channel if set
    @minqlx.thread
    def handle_chat(self, player, msg, channel):
        if self.discord_chat_channel_id:
            content = "**{}**: {}".format(self.clean_text(player.name), msg)
            requests.post("https://discordapp.com/api/channels/" +  self.discord_chat_channel_id + "/messages",
                                        data=json.dumps({'content': content}),
                                        headers = {'Content-type': 'application/json', 'Authorization': 'Bot ' + self.discord_bot_token})

    #Polls discord chat for new messages if set and relays message in-game
    @minqlx.thread
    def poll_discord_messages(self):
        last_message = requests.get("https://discordapp.com/api/channels/" +  self.discord_chat_channel_id + "/messages?limit=1",
                                        headers = {'Content-type': 'application/json', 'Authorization': 'Bot ' + self.discord_bot_token})
        last_message = json.loads(last_message.text)

        if self.last_polled_message_id != last_message[0]["id"]:
            self.msg("^5(DC) ^3{}: ^7{}".format(last_message[0]["author"]["username"], last_message[0]["content"]))
            self.last_polled_message_id = last_message[0]["id"]

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




