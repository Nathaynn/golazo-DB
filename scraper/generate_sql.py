import json
import os

def open_json(path, foo):
    file = open(path, foo)
    return file

def close_json(file):
    file.close()

# all data generation for every table {DOESNT INCLUDE LEAGUE_SEASON, I will just write those statements since those are short}
def gen_player_insert(player_fname, player_lname, player_position, player_age, player_height, player_weight, player_nationality):
    statement = 'INSERT INTO PLAYER(PLAYER_FNAME, PLAYER_LNAME, PLAYER_POSITION, PLAYER_AGE, PLAYER_HEIGHT, PLAYER_WEIGHT, PLAYER_NATIONALITY) VALUES'

    # website sometimes has missing/incorrect info, so if an error occurs then give a default value of 0
    try: 
        age = int(player_age)
    except:
        age = 0
    try:
        height = int(player_height)
    except:
        height = 0
    try:
        weight = int(player_weight)
    except:
        weight = 0

    statement += f'("{player_fname}", "{player_lname}", "{player_position}", {age}, {height}, {weight}, "{player_nationality}");'
    return statement

def gen_player_history_insert(id, team_name, year, num):
    statement = 'INSERT INTO PLAYER_HISTORY(PLAYER_ID, TEAM_NAME, SEASON_YEAR, PLAYER_NUMBER) VALUES'
    statement += f'({id}, "{team_name}", "{year}", {num});'

    return statement


def gen_match_insert(home_name, away_name, league, year, home_score, away_score, date):
    statement = 'INSERT INTO MATCH(MATCH_HOME_TEAM_NAME, MATCH_AWAY_TEAM_NAME, LEAGUE_NAME, SEASON_YEAR, MATCH_HOME_SCORE, MATCH_AWAY_SCORE, MATCH_DATE) VALUES'
    statement += f'("{home_name}", "{away_name}", "{league}", "{year}", {int(home_score)}, {int(away_score)}, "{date}");'

    return statement

def gen_manager_insert(fname, lname, m_age, nationality):
    statement = 'INSERT INTO MANAGER(MANAGER_FNAME, MANAGER_LNAME, MANAGER_AGE, MANAGER_NATIONALITY) VALUES'

    # website sometimes has missing/incorrect info, so if an error occurs then give a default value of 0
    try: 
        age = int(m_age)
    except:
        age = 0
    
    statement += f'("{fname}", "{lname}", {age}, "{nationality}");'
    return statement

def gen_manager_history_insert(id, team, year):
    statement = 'INSERT INTO MANAGER_HISTORY(MANAGER_ID, TEAM_NAME, SEASON_YEAR) VALUES'
    statement += f'({id}, "{team}", "{year}");'

    return statement

def gen_team_insert(team_name, league_name, team_city, stadium, founded):
    statement = 'INSERT INTO TEAM(TEAM_NAME, LEAGUE_NAME, TEAM_CITY, TEAM_STADIUM, TEAM_FOUNDED) VALUES'
    founded = f'{founded}-01-01' 
    statement += f'("{team_name}", "{league_name}", "{team_city}", "{stadium}", "{founded}");'
    return statement

def generate_all_playerstuff():
    # contains a id of every unique player
    id_path = './data/player_ids.json'

    # will contain duplicates across seasons
    path_2020 = f'./data/2020/players.json'
    #path_2021 = f'./data/2021/players.json'
    #path_2022 = f'./data/2022/players.json'

    # combine all data, then take out dupes
    file_id = open_json(id_path, 'r')
    data_id = json.load(file_id)
    close_json(file_id)

    file_2020 = open_json(path_2020, 'r')
    data_2020 = json.load(file_2020)
    close_json(file_2020)
    """
    file_2021 = open_json(path_2021, 'r')
    data_2021 = json.load(file_2021)
    close_json(file_2021)

    file_2022 = open_json(path_2022, 'r')
    data_2022 = json.load(file_2022)
    close_json(file_2022)
    """
    data = data_2020 #+ data_2021 + data_2022
    unique_players = []
    for i in data:
        if i not in unique_players:
            unique_players.append(i)
    
    # Concerns: A player might have the same exact name as another player, but whoever wins gets to exist, shouldn't matter too much since this db is gonna be populated and a couple of missing
    # players shouldn't be too much of a concern
    
    # Iterate through ids (start from ID = 1001)
    player_statements = "% PLAYERS %\n\n ALTER TABLE PLAYER AUTO_INCREMENT = 1001;\n"
    for i in data_id.keys():
        name = str(i).split()
        fname = name[0]
        lname = name[1]
        for j in unique_players:
            if fname == j['Player Fname'] and lname == j['Player Lname']:
                player_statements += gen_player_insert(fname, lname, j['Player Position'], j['Player Age'], j['Player Height'], j['Player Weight'], j['Player Nationality']) + '\n'
                break
    
    # Iterate through player_history
    player_statements += '% PLAYER_HISTORY % \n\n'
    file_ph = open_json('./data/player_history.json', 'r')
    data_ph = json.load(file_ph)
    close_json(file_ph)

    for i in data_ph:
        player_statements += gen_player_history_insert(i['Player ID'], i['Team Name'], i['Season Year'].replace("/", "-"), i['Player Number']) + '\n'
    
    return player_statements

def generate_all_managerstuff():
    # contains a id of every unique manager
    id_path = './data/manager_ids.json'

    # will contain duplicates across seasons
    path_2020 = f'./data/2020/managers.json'
    #path_2021 = f'./data/2021/managers.json'
    #path_2022 = f'./data/2022/managers.json'

    # combine all data, then take out dupes
    file_id = open_json(id_path, 'r')
    data_id = json.load(file_id)
    close_json(file_id)

    file_2020 = open_json(path_2020, 'r')
    data_2020 = json.load(file_2020)
    close_json(file_2020)
    """
    file_2021 = open_json(path_2021, 'r')
    data_2021 = json.load(file_2021)
    close_json(file_2021)

    file_2022 = open_json(path_2022, 'r')
    data_2022 = json.load(file_2022)
    close_json(file_2022)
    """
    data = data_2020 #+ data_2021 + data_2022
    unique_managers = []
    for i in data:
        if i not in unique_managers:
            unique_managers.append(i)
    
    # Iterate through ids (start from ID = 1)
    manager_statements = "% MANAGERS % \n\n ALTER TABLE MANAGER AUTO_INCREMENT = 1; \n"
    for i in data_id.keys():
        name = str(i).split()
        fname = name[0]
        lname = name[1]
        for j in unique_managers:
            if fname == j['Manager Fname'] and lname == j['Manager Lname']:
                # NOTE I accidently made manager nationaly have a key of player nationality, the value is still true tho! so i'll change later
                manager_statements += gen_manager_insert(fname, lname, j['Manager Age'], j['Player Nationality']) + '\n'
                break
    
    # Iterate through manager_history
    manager_statements += '% MANAGER_HISTORY % \n\n'
    file_ph = open_json('./data/manager_history.json', 'r')
    data_ph = json.load(file_ph)
    close_json(file_ph)

    for i in data_ph:
        manager_statements += gen_manager_history_insert(i['Manager ID'], i['Team Name'], i['Season Year'].replace("/", "-")) + '\n'
    
    return manager_statements

def generate_all_matchstuff():
  # will contain duplicates across seasons
    path_2020 = f'./data/2020/match.json'
    #path_2021 = f'./data/2021/match.json'
    #path_2022 = f'./data/2022/match.json'

    # combine all data, there is no need to worry for dupes
    file_2020 = open_json(path_2020, 'r')
    data_2020 = json.load(file_2020)
    close_json(file_2020)
    """
    file_2021 = open_json(path_2021, 'r')
    data_2021 = json.load(file_2021)
    close_json(file_2021)

    file_2022 = open_json(path_2022, 'r')
    data_2022 = json.load(file_2022)
    close_json(file_2022)
    """
    data = data_2020 #+ data_2021 + data_2022

    match_statements = '% MATCHES % \n\nALTER TABLE MATCH AUTO_INCREMENT= 10001; \n'
    for i in data:
        match_statements += gen_match_insert(i['Home Team'], i['Away Team'], i['League'], i['Season'].replace("/", "-"), i['Home Score'], i['Away Score'], i['Game Date']) + '\n'

    return match_statements

def generate_all_teamstuff():
    # team data SHOULD be the same every league and season, so we just need to open 1 file
    path = './data/2020/teams.json'
    file = open_json(path, 'r')
    data = json.load(file)
    close_json(file)

    team_statements = '% TEAMS % \n\n'
    for i in data:
        team_statements += gen_team_insert(i['Team Name'], i['Team League'], i['Team City'], i['Team Stadium'], i['Team Founded']) + '\n'

    return team_statements

def cool_stuff():
    temp = ''
    temp += generate_all_teamstuff()
    temp += generate_all_matchstuff()
    temp += generate_all_managerstuff()
    temp += generate_all_playerstuff()

    return temp

def create_file():
    
    os.mkdir('./data/sql')
    f = open('./data/sql/class.sql', 'w')
    f.write(cool_stuff())
    f.close()

    
create_file()