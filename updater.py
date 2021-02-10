from game_fetcher import *

#database = "D:/Github/SteamWatcher/database/playerinfo.db"

def update(player_list):
    reports = []
    for player in player_list:
        # try:
        #     last_match_id = get_last_match_id_by_steamID(player.steam_id)
        # except DOTA2HTTPError:
        #     continue
        # if last_match_id != player.last_match_id:
        #     report = format_match_info(player.steam_id)
        #     #update_last_match_id(player.steam_id,last_match_id,database)
        #     player.last_match_id = last_match_id
        report = format_match_info(player.steam_id)
        reports.append(report)
        #reports.update({player.nickname: report})
    
    return reports
