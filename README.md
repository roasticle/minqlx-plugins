<strong>bot_antispec.py</strong> - fixes bug with bot_minplayers and teamsizes lower than player limit that causes bots to spec (kicks them)

<strong>discordbot.py</strong> - announce server stats to your Discord server!
- example output: https://i.gyazo.com/d52607e54225419f4ed61e3789b68181.png
- qlx_discord_channel_id and qlx_discord_bot_token MUST be set for this to work
- you also need to authenticate the bot with a gateway at least once for it to be able to send messages - for instance using https://github.com/roasticle/QLStats-Discord-Minimal - after it auths with the gateway once, you don't need to use the bot php script anymore
- see https://github.com/Just-Some-Bots/MusicBot/wiki/FAQ for creating the bot and also follow enabling developer mode
- once developer mode is enabled, right click on your Discord channel and copy id - use this for qlx_discord_channel_id
- optional cvar discord_chat_channel_id - this will output chat to a discord channel and also forward discord chat to the server from that channel

<strong>duke.py</strong> - Duke Nukem sound triggers
- requires http://steamcommunity.com/sharedfiles/filedetails/?id=572453229
- use !duke for random sound or !duke <soundname> (without .wav at the end).. list of sounds is on workshop page

<strong>gravityfixer.py</strong> - restores gravity to normal after maps with custom gravity
- in your server.cfg you will need to set qlx_alternateGravityMaps "mapname1,mapname2,etc" for each map that has an alternate gravity set 

<strong>endstats.py</strong> - various stats given at end of game
- example output - https://thumb.gyazo.com/thumb/1200/_fb5d34fde51d1333da746ad90f25cf9f-png.jpg

<strong>gungames.py</strong> - custom voting triggers for gungames factories
- this REQUIRES workshop item: http://steamcommunity.com/sharedfiles/filedetails/?id=862639717
- if vote passes will reload current map with voted factory
- !gungames to show all available options
- available triggers: !glovelove !mgs !shotties !nades !rockets !lgs !rails !plasmas !bfgs !nails !mines !chainguns !hmg !kami

<strong>mapoo.py</strong> - allows multiple mappool files that change automatically based on player number
- the mappool files should be all located in your baseq3 folder
- threshold variables are the number of players (in-game not spec) at which the mappool gets activated
- this requires 6 cvars to be set
- For example:
- set qlx_mapoo_small_file "mappool_ffa_small.txt"
- set qlx_mapoo_medium_file "mappool_ffa_medium.txt"
- set qlx_mapoo_large_file "mappool_ffa_large.txt"
- set qlx_mapoo_small_threshhold "1"
- set qlx_mapoo_medium_threshhold "6"
- set qlx_mapoo_large_threshhold "13"

<strong>motd.py</strong> - a replacement motd plugin that allows multiple motd/welcome sounds
- replace the default motd.py with this file
- add your motd sounds to the MOTD_SOUNDS list in the file

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
