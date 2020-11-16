class player:
    steam_id = 0
    nickname = ''
    DOTA2_score = ''
    last_DOTA2_match_ID = ''

    kill = 0
    death = 0
    assist = 0
    # 1为天辉, 2为夜魇
    dota2_team = 1
    kda = 0
    gpm = 0
    xpm = 0
    hero = ''
    last_hit = 0
    damage = 0

    def __init__(self, nickname, steam_id, last_DOTA2_match_ID):
        self.nickname = nickname
        self.short_id = steam_id
        self.last_DOTA2_match_ID = last_DOTA2_match_ID


PLAYER_LIST = []