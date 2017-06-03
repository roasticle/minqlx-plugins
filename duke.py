import minqlx
import random
import time

duke_sounds = ["2ride06","abort01","ahh04","ahmuch03","aisle402","amess06","annoy03","beback01","bitchn04","blowit01","booby04","bookem03","born01","chew05","comeon02","con03","cool01","cry01","damn03","damnit04","dance01","dieob03","dmdeath","doomed16","dscrem04","dscrem15","dscrem16","dscrem17","dscrem18","dscrem38","duknuk14","eat08","face01","force01","gasp","gasps07","getcrap1","getsom1a","gmeovr05","gothrt01","groovy02","gulp01","guysuk01","hail01","happen01","holycw01","holysh02","imgood12","indpnc01","inhell01","introc","jones04","kick01-i","ktitx","letgod01","letsrk03","lookin01","makeday1","mdevl01","meat04-n","myself3a","name01","needed03","nobody01","onlyon03","pain13","pain28","pain39","pain54","pain68","pain75","pain87","pain93","party03","pay02","piece02","pisses01","pissin01","postal01","quake06","r&r01","ready2a","rides09","rip01","ripem08","rockin02","shake2a","slacker1","smack02","sohelp02","sukit01","termin01","thsuk13a","vacatn01","waitin03","wansom4a","whipyu01","whrsit05","yippie01","yohoho01","yohoho09"]

class duke(minqlx.Plugin):
    database = minqlx.database.Redis

    def __init__(self):
        self.add_command("duke", self.cmd_duke)
        self.last_sound = None

    def cmd_duke(self, player, msg, channel):
        message_string = ""
        for i in range(1, len(msg)): message_string += str(msg[i])

        if message_string:
            if message_string in duke_sounds:
                self.play_sound("sound/duke/" + message_string + ".wav")
            else:
                self.msg("Not a valid Duke sound! See ''Duke Nukem Voice Sound Pack for minqlx'' on workshop for list!")
        else:
            self.play_sound("sound/duke/" + random.choice(duke_sounds) + ".wav")

    def play_sound(self, path):
        if not self.last_sound:
            pass
        elif time.time() - self.last_sound < self.get_cvar("qlx_funSoundDelay", int):
            return

        self.last_sound = time.time()
        for p in self.players():
            if self.db.get_flag(p, "essentials:sounds_enabled", default=True):
                super().play_sound(path, p)
