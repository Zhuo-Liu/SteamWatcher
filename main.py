from game_fetcher import *
from player import *
from updater import *
import time


if __name__ == "__main__":
    player_list_temp = [
        ["Zard-", "104744847"]
    ]
    player_list = []
    for player_temp in player_list_temp:
        nickname = player_temp[0]
        steam_id = player_temp[1]
        try:
            last_match_id = get_last_match_id_by_steamID(steam_id)
        except DOTA2HTTPError:
            last_match_id = "-1"
        #insert_info(steam_id,nickname,last_match_id,database)

        player_list.append(player(steam_id,nickname,last_match_id))
    
    print(player_list)
    print("玩家载入完毕")
    while True:
        reports = update(player_list)
        print(reports[0])
        time.sleep(10)
