import minqlx
import requests

class weather(minqlx.Plugin):

    def __init__(self):
        self.add_command("weather", self.cmd_weather, usage="<postal or zip code>")
        self.set_cvar_once("qlx_OpenweatherKey", "")

    def cmd_weather(self, player, msg, channel):
        api_key = self.get_cvar("qlx_OpenweatherKey")

        if not api_key:
            self.msg("^3You need to set qlx_OpenweatherKey.")
            return minqlx.RET_STOP_ALL

        if(len(msg) == 1):
            return minqlx.RET_USAGE

        @minqlx.thread
        def get_weather():
            try:
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + str(msg[1]) + "&appid=" + api_key)
                r.raise_for_status()
                channel.reply(r.json())
            except requests.exceptions.RequestException as e:
                self.logger.info("ERROR: {}".format(e))

        get_weather()
