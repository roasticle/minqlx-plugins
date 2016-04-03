import minqlx
import requests

class weather(minqlx.Plugin):

    def __init__(self):
        self.add_command("weather", self.cmd_weather, usage="<postal or zip code>")
        self.set_cvar_once("qlx_WeatherUndergroundKey", "")

    def cmd_weather(self, player, msg, channel):
        api_key = self.get_cvar("qlx_WeatherUndergroundKey")

        if not api_key:
            self.msg("^3You need to set qlx_WeatherUndergroundKey.")
            return minqlx.RET_STOP_ALL

        if(len(msg) == 1):
            return minqlx.RET_USAGE

        @minqlx.thread
        def get_weather():
            try:
                r = requests.get("http://api.wunderground.com/api/" + api_key + "/geolookup/conditions/forecast/q/" + str(msg[1]) + ".json")
                r.raise_for_status()
                r = r.json()
                if 'location' in r:
                    city = r["location"]["city"]
                    state = r["current_observation"]["observation_location"]["state"].title()
                    country = r["location"]["country_name"]
                    temp = r["current_observation"]["temperature_string"]
                    weather = r["current_observation"]["weather"]
                    wind = r["current_observation"]["wind_string"]
                    if country == "USA":
                        forecast = r["forecast"]["txt_forecast"]["forecastday"][0]["fcttext"]
                    else:
                        forecast = r["forecast"]["txt_forecast"]["forecastday"][0]["fcttext_metric"]
                    channel.reply("^2{}, {}, {} ^5Current Temp: ^6{}, {}, ^5Wind: ^6{}, ^5Forecast: ^6{}".format(city, state, country, temp, weather, wind, forecast))
                else:
                    channel.reply("No weather results!")
            except requests.exceptions.RequestException as e:
                self.logger.info("ERROR: {}".format(e))

        get_weather()
