?<strong>bot_antispec.py</strong> - fixes bug with bot_minplayers and teamsize lower than player limit that causes bots to spec (kicks them)

<strong>intermission.py</strong> - triggers a sound/music at each game end
- add intermission to your server.cfg minqlx plugins
- if you want a custom sound/music other than those included in the base paks, you can add a custom workshop item with the sound. It needs to be in mono OGG or WAV format and the pak structure is /sound/customsoundfolder/sound.ogg (or wav).
- see: https://steamcommunity.com/sharedfiles/filedetails/?id=539821860 for info on uploading your custom pak to the workshop.
- once that's up you can add: qlx_intermissionSound "soundpath" (same format as pak, or you can use a base pak sound) to your server cfg and you are good to go!

<strong>slaphappy.py</strong> - spam slap pesky players!
- usage: !slaphappy id number_of_slaps frequency_in_seconds damage (damage is optional)

<strong>weather.py</strong> - lets you check weather and forecast in-game!
- you will need an API key (free) from https://www.wunderground.com/weather/api/d/login.html
- set qlx_WeatherUndergroundKey "YOURAPIKEYHERE" in your server.cfg
- usage: !weather (postal or zip code) or (countryname or state/city> - eg. !weather M4S1C4, !weather 90210, !weather USA/newyork, !weather CA/losangeles

Enjoy! :D - roasticle (roast on quakenet IRC). Donations are appreciated :)


[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=L4PCX7WVF4L7G)
