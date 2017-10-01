import minqlx

country_code_anthems = {'AF': 'afghanistan', 'SO': 'somalia', 'JP': 'japan-youtube', 'RU': 'russia', 'VA': 'vaticancity', 'CG': 'republicofthecongo', 'GR': 'greece', 'NO': 'norway', 'BF': 'burkinafaso', 'KH': 'cambodia-youtube', 'CN': 'china', 'TV': 'tuvalu', 'ET': 'ethiopia', 'AW': 'aruba', 'AG': 'antiguaandbarbuda', 'CO': 'colombia', 'VN': 'vietnam', 'LU': 'luxembourg', 'NL': 'netherlands', 'SM': 'sanmarino-youtube', 'FJ': 'fiji', 'BE': 'belgium', 'FR': 'france', 'LK': 'srilanka', 'CR': 'costarica', 'FM': 'micronesia', 'KG': 'kyrgyzstan', 'PE': 'peru', 'ML': 'mali', 'CY': 'cyprus', 'SL': 'sierraleone', 'ZM': 'zambia', 'NP': 'nepal', 'LT': 'lithuania', 'HR': 'croatia', 'IL': 'israel', 'PH': 'philippines', 'GH': 'ghana', 'BN': 'brunei', 'CL': 'chile', 'SC': 'seychelles', 'KP': 'northkorea', 'MN': 'mongolia', 'BW': 'botswana', 'BI': 'burundi', 'KR': 'southkorea', 'MU': 'mauritius', 'BJ': 'benin', 'GD': 'grenada', 'PW': 'palau', 'GA': 'gabon', 'ZA': 'southafrica', 'MR': 'mauritania', 'BH': 'bahrain', 'SD': 'sudan', 'RS': 'serbia', 'XK': 'kosovo', 'GY': 'guyana', 'MD': 'moldova', 'ER': 'eritrea', 'GM': 'gambia', 'VE': 'venezuela', 'PK': 'pakistan', 'SE': 'sweden', 'AT': 'austria', 'TH': 'thailand', 'SN': 'senegal', 'DE': 'germany', 'MX': 'mexico', 'HT': 'haiti', 'TR': 'turkey', 'AL': 'albania', 'TL': 'easttimor', 'PG': 'papuanewguinea', 'BG': 'bulgaria', 'VU': 'vanuatu', 'AM': 'armenia', 'AD': 'andorra', 'SR': 'suriname', 'AZ': 'azerbaijan', 'KZ': 'kazakhstan', 'JO': 'jordan', 'DM': 'dominica', 'IT': 'italy', 'TD': 'chad', 'RW': 'rwanda', 'GT': 'guatemala', 'SG': 'singapore', 'EG': 'egypt', 'MH': 'marshallislands', 'KE': 'kenya', 'IQ': 'iraq', 'BR': 'brazil', 'KW': 'kuwait', 'DJ': 'djibouti', 'YE': 'yemen', 'MC': 'monaco', 'GB': 'unitedkingdom', 'BD': 'bangladesh', 'LA': 'laos', 'AE': 'unitedarabemirates', 'NI': 'nicaragua', 'ME': 'montenegro', 'US': 'unitedstatesofamerica', 'LC': 'stlucia', 'TN': 'tunisia', 'HU': 'hungary', 'PA': 'panama', 'MA': 'morocco', 'TT': 'trinidadandtobago', 'UZ': 'uzbekistan', 'LB': 'lebanon', 'CZ': 'czechrepublic', 'JM': 'jamaica', 'HN': 'honduras', 'IN': 'india-janaganamana', 'BY': 'belarus', 'UA': 'ukraine', 'PL': 'poland', 'SI': 'slovenia', 'LR': 'liberia', 'SZ': 'swaziland', 'MY': 'malaysia', 'CK': 'thecookislands', 'BA': 'bosniaandherzegovina', 'MG': 'madagascar', 'AU': 'australia', 'BS': 'thebahamas', 'MW': 'malawi', 'CA': 'canada', 'DK': 'denmark', 'MT': 'malta', 'WS': 'samoa', 'LI': 'liechtenstein', 'CV': 'capeverde', 'CI': 'theivorycoast', 'CH': 'switzerland', 'OM': 'oman', 'LY': 'libya', 'GE': 'georgia', 'BT': 'bhutan', 'NA': 'namibia', 'SV': 'elsalvador', 'EC': 'ecuador', 'LV': 'latvia', 'IR': 'iran', 'PY': 'paraguay', 'TO': 'tonga', 'NZ': 'newzealand', 'BB': 'barbados', 'CM': 'cameroon', 'SA': 'saudiarabia', 'CF': 'centralafricanrepublic', 'KM': 'comoros', 'BZ': 'belize', 'AR': 'argentina', 'AO': 'angola', 'RO': 'romania', 'NE': 'nigeria', 'MZ': 'mozambique', 'CU': 'cuba', 'PT': 'portugal', 'GN': 'guinea-bisssau', 'SK': 'slovakia', 'MV': 'themaldives', 'TZ': 'tanzania', 'TG': 'togo', 'DZ': 'algeria', 'UY': 'uruguay', 'TM': 'turkmenistan', 'ST': 'saotomeandprincipe-independenciatotal', 'PR': 'puertorico', 'MM': 'burma', 'QA': 'qatar', 'FI': 'finland', 'ID': 'indonesia', 'ES': 'spain', 'MK': 'macedonia', 'EE': 'estonia', 'BO': 'bolivia'}

class winneranthem(minqlx.Plugin):

    def __init__(self):
        self.add_hook("game_end", self.handle_game_end)
        self.add_hook("stats", self.handle_stats)
        self.winner = ""

    def handle_stats(self, stats):
        if stats['TYPE'] == "PLAYER_STATS":
            if stats['DATA']['QUIT'] == 0 and stats['DATA']['WARMUP'] == 0 and stats['DATA']['LOSE'] == 0:
                if int(stats['DATA']['STEAM_ID']) != 0:
                    self.winner = self.player(int(stats['DATA']['STEAM_ID']))
                else:
                    self.winner = "bot"

    @minqlx.delay(0.3)
    def handle_game_end(self, data):
        if not data["ABORTED"]:
            if self.winner != "bot":
                if self.winner.country in country_code_anthems:
                    self.song_player("sound/anthems/{}.ogg".format(country_code_anthems[self.winner.country]))
            else:
                self.song_player("sound/anthems/roboto.ogg")
        self.winner = ""

    def song_player(self, song):
        for p in self.players():
            if self.db.get_flag(p, "essentials:sounds_enabled", default=True):
                self.stop_music(p)
                self.play_sound(song, p)


