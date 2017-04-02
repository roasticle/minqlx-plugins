<strong>bot_antispec.py</strong> - fixes bug with bot_minplayers and teamsizes lower than player limit that causes bots to spec (kicks them)

<strong>gravityfixer.py</strong> - restores gravity to normal after maps with custom gravity
- in your server.cfg you will need to set qlx_alternateGravityMaps "mapname1,mapname2,etc" for each map that has an alternate gravity set 

<strong>gungames.py</strong> - custom voting triggers for gungames factories
- this REQUIRES workshop item: http://steamcommunity.com/sharedfiles/filedetails/?id=862639717
- if vote passes will reload current map with voted factory
- !gungames to show all available options
- available triggers: !glovelove !mgs !shotties !nades !rockets !lgs !rails !plasmas !bfgs !nails !mines !chainguns !hmg !kami
- note: just added hmg and kami, you will need to update the workshop item as well for them to work


<strong>nextmap.py</strong> - announce nextmap and fix nextmap repeats
- NOTE: intended for servers with no end-game map voting
- announces nextmap at end of game or on !nextmap
- !currentmap to show..current map! (mind blowing i know!)

<strong>slaphappy.py</strong> - spam slap pesky players!
- usage: !slaphappy id number_of_slaps frequency_in_seconds damage (damage is optional)

<strong>weather.py</strong> - lets you check weather and forecast in-game!
- you will need an API key (free) from https://www.wunderground.com/weather/api/d/login.html
- set qlx_WeatherUndergroundKey "YOURAPIKEYHERE" in your server.cfg
- usage: !weather (postal or zip code) or (countryname or state/city> - eg. !weather M4S1C4, !weather 90210, !weather USA/newyork, !weather CA/losangeles, !weather vostok, antarctica - using postal or zip code is usually best as it prevents multiple locations from being found (no data gets returned).

Enjoy! :D - roasticle (roast on quakenet IRC). Donations are appreciated :)


[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=L4PCX7WVF4L7G)
