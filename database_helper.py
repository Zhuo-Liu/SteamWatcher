import sqlite3
from sqlite3 import Error
from player import *
from game_fetcher import *
from player import *

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def update_last_match_id_helper(conn,steam_id,last_match_id):
    try:
        c = conn.cursor()
        c.execute("UPDATE playerinfo SET last_match_id='{}'WHERE steam_id={}".format(last_match_id, steam_id))
        conn.commit()
    except Error as e:
        print(e)
    conn.close()

def insert_info_helper(conn,steam_id,nickname,last_match_id):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO playerinfo (steam_id, nickname, last_match_id) VALUES ({}, '{}', '{}')".format(steam_id,nickname,last_match_id))
        conn.commit()
    except Error as e:
        print(e)
    conn.close()

def update_last_match_id(steam_id,last_match_id,database):
    conn = create_connection(database)
    if conn is not None:
        update_last_match_id_helper(conn,steam_id,last_match_id)
    else:
        print("Error! cannot create the database connection.")


def insert_info(steam_id,nickname,last_match_id,database):
    conn = create_connection(database)
    if conn is not None:
        insert_info_helper(conn,steam_id,nickname,last_match_id)
    else:
        print("Error! cannot create the database connection.")

def if_player_exists(steam_id,database):
    conn = create_connection(database)
    if conn is not None:
        c = conn.cursor()
        c.execute("SELECT * FROM playerinfo WHERE steam_id={}".format(steam_id))
        rows = c.fetchall()
        if len(rows) == 0:
            return False
        else:
            return True
    else:
        print("Error! cannot create the database connection.")
        exit(1)

def get_players_from_database(database):
    PLAYER_LIST = []
    conn = create_connection(database)
    if conn is not None:
        c = conn.cursor()
        players = c.execute("SELECT * FROM playerinfo")
        for it in players:
            player_obj = player(steam_id=it[0],nickname=it[1],last_match_id=it[2])
            PLAYER_LIST.append(player_obj)
    else:
        print("Error! cannot create the database connection.")
    
    return PLAYER_LIST

if __name__ == "__main__":
    #database = "D:/Github/SteamWatcher/database/playerinfo.db"
    player_list_temp = [
        ["zliu", 243044275],
        ["Zard-", 165652483]
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

