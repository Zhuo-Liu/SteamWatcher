import numpy as np
import requests
import datetime
import pandas as pd

from config import *

# 异常处理
class DOTA2HTTPError(Exception):
    pass


def get_team_by_slot(slot: int) -> int:
    if slot < 100:
        return 1
    else:
        return 2


def get_last_match_id_by_steamID(account_id):
    # get match_id
    url_lastmatch = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v0001/?key={}&account_id={}&matches_requested=1'.format(API_KEY,account_id)
    try:
        response = requests.get(url_lastmatch)
    except requests.RequestException:
        raise DOTA2HTTPError("Requests Error")

    if response.status_code >= 400:
        if response.status_code == 401:
            raise DOTA2HTTPError("Unauthorized request 401. Verify API key.")
        if response.status_code == 503:
            raise DOTA2HTTPError("The server is busy or you exceeded limits. Please wait 30s and try again.")
        raise DOTA2HTTPError("Failed to retrieve data: %s. URL: %s" % (response.status_code, url_lastmatch))

    results = response.json()

    if results["result"]["status"] == 1:
        #return results["result"]["matches"]
        match_id = results["result"]["matches"][0]["match_id"]
        url_details = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key={}&match_id={}'.format(API_KEY, match_id)

        try:
            response_details = requests.get(url_details)
        except requests.RequestException:
            raise DOTA2HTTPError("Requests Error")
        if response_details.status_code >= 400:
            if response_details.status_code == 401:
                raise DOTA2HTTPError("Unauthorized request 401. Verify API key.")
            if response_details.status_code == 503:
                raise DOTA2HTTPError("The server is busy or you exceeded limits. Please wait 30s and try again.")
            raise DOTA2HTTPError("Failed to retrieve data: %s. URL: %s" % (response_details.status_code, url_details))
        
        match = response_details.json()

        return match
    else:
        raise DOTA2HTTPError("Permission Error: User does not allow data")

'''
win_side
start_time
duration (minutes, second)
game_mode
cluster
win_or_lose
hero
kill
death
assist
'''
def format_match_info(account_id):
    try:
        match = get_last_match_id_by_steamID(account_id)
    except DOTA2HTTPError:
        return "failed to fetch match infomation"
    
    win_side = 0
    if match["result"]["radiant_win"] == True:
        win_side = 1 # Radiant Win
    else:
        win_side = 2 # Dire Win

    starttime_UNIX = match["result"]["start_time"]
    start_time = datetime.datetime.fromtimestamp(int(starttime_UNIX)).strftime('%Y-%m-%d %H:%M:%S')
    duration = match["result"]["duration"]
    minutes = duration // 60
    seconds = duration % 60

    game_mode = Gamemodes[int(match["result"]["game_mode"])]

    #cluster = Clusters[int(match["result"]["cluster"])]

    player_list = match["result"]["players"]
    win_or_lose = "unclear"
    for player in player_list:
        if player["account_id"] == int(account_id):
            if player["player_slot"] <100:
                player_side = 1
            else:
                player_side = 2
            if win_side == player_side:
                win_or_lose = "win"
            else:
                win_or_lose = "lost"
            
            kills = player["kills"]
            deaths = player["deaths"]
            assists = player["assists"]

    
    report = "account_id 为{}的小朋友在{}进行了一局时长为{}分{}秒的紧张刺激的游戏,结果{}了".format(account_id,start_time,minutes,seconds,win_or_lose)
    return report

if __name__ == "__main__":
    format_match_info("104744847")
