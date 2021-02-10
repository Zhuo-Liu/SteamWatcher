class player:
    '''
    player intrinsic attributes
    '''
    steam_id = 0
    nickname = ''
    last_match_id = ''

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

    def __init__(self, steam_id, nickname, last_match_id):
        self.nickname = nickname
        self.steam_id = steam_id
        self.last_last_match_id = last_match_id


#PLAYER_LIST = []