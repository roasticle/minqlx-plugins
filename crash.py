import minqlx
import os
import zipfile
import random

CRASH_SOUNDS = []

with zipfile.ZipFile(os.getcwd() + "/baseq3/pak00.pk3") as z:
    for fileinfo in z.infolist():
        if fileinfo.filename.startswith('sound/vo/crash_new/') and fileinfo.file_size > 0:
            CRASH_SOUNDS.append(fileinfo.filename)

class crash(minqlx.Plugin):

    def __init__(self):
        self.add_command("crash", self.cmd_crash)

    def cmd_crash(self, player, msg, channel):
        self.plugins['fun'].play_sound(random.choice(CRASH_SOUNDS))
