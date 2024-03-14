from teams import *
from players import *
from match import *
import json
import os
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

if __name__ == '__main__':
        
    # leagues
    premier = "https://www.playmakerstats.com/competition/premier-league"
    liga = "https://www.playmakerstats.com/competition/la-liga"
    serie = "https://www.playmakerstats.com/competition/serie-a"
    bundesliga_1 = "https://www.playmakerstats.com/competition/1-bundesliga"
    ligue_1 = "https://www.playmakerstats.com/competition/ligue-1"
    league_urls = [serie, bundesliga_1, liga, premier]
    league_focus = league_urls[1]
    league_urls = [league_focus]

    # for debugging

    # parameters
    season_of_interest = '22'
    chop = webdriver.ChromeOptions()
    chop.add_extension('./adblock/Adblock.crx')
    # saved my life, hides the browser so now i can use computer 
    chop.add_argument('--headless=new')
    matches_settings = webdriver.ChromeOptions()
    matches_settings.add_extension('./adblock/Adblock.crx')

    
    team_stuff = []
    player_stuff = []
    match_stuff = []

    try:
        driver = webdriver.Chrome()
    except:
        chromedriver_autoinstaller.install()

    # args
    for i in league_urls:
        
        driver = webdriver.Chrome(chop)
        league_season = get_season_link(i, driver, season_of_interest)
        driver = webdriver.Chrome(chop)
        player_stuff.append(league_player_data(league_season, driver))
        driver = webdriver.Chrome(matches_settings)
        match_stuff.append(season_match_data(league_season, driver))
        driver = webdriver.Chrome(chop)
        team_stuff.append(team_data(league_season, driver))


    # make directory for jsons
    dir_path = f'./data/{full_season(season_of_interest)[0:4]}'
    try:
        os.mkdir('./data')
    except:
        print('data folder already exists!')

    try:
        os.mkdir(dir_path)
        f = open(f'{dir_path}/players.json', 'x')
        f.close()
        f = open(f'{dir_path}/managers.json', 'x')
        f.close()
        f = open(f'{dir_path}/match.json', 'x')
        f.close()
        f = open(f'{dir_path}/teams.json', 'x')
        f.close()
    except:
        print('Data is already stored')

    important_jsons = ['player_ids.json', 'manager_ids.json', 'player_history.json', 'manager_history.json']
    global_jsons = os.listdir(f'{dir_path}/../.')
    for i in important_jsons:
        if i not in global_jsons:
            f = open(f'./data/{i}', 'x')
            f.close()

    # jsons data entry
    # teams.json
    x = []
    for i in team_stuff:
        for j in i:
            x.append(j)
    
    try:
        pre_append = open(f'{dir_path}/teams.json', 'r')
        pre_append_data = json.load(pre_append)
        pre_append_data.append(x)
    except:
        pre_append_data = x
    
    json_stuff = json.dumps(pre_append_data, indent=4)
    with open(f'{dir_path}/teams.json', 'w') as file:
        file.write(json_stuff)
        file.close()
    
    # match.json
    x = []
    for i in match_stuff: 
        for j in i:
            if j['Home Team'] != '' or j['Away Team'] != '':
                x.append(j)
    
    try:
        pre_append = open(f'{dir_path}/match.json', 'r')
        pre_append_data = json.load(pre_append)
        pre_append_data.append(x)
    except:
        pre_append_data = x

    json_stuff = json.dumps(pre_append_data, indent=4)
    with open(f'{dir_path}/match.json', 'w') as file:
        file.write(json_stuff)
        file.close()

    # players.json
    x = []
    for i in player_stuff:
        for j in i[1]:
            x.append(j)
    try:
        pre_append = open(f'{dir_path}/players.json', 'r')
        pre_append_data = json.load(pre_append)
        pre_append_data.append(x)
    except:
        pre_append_data = x

    json_stuff = json.dumps(pre_append_data, indent=4)
    with open(f'{dir_path}/players.json', 'w') as file:
        file.write(json_stuff)
        file.close()

    # managers.json
    x = []
    for i in player_stuff:
        for j in i[3]:
            x.append(j)
    try:
        pre_append = open(f'{dir_path}/managers.json', 'r')
        pre_append_data = json.load(pre_append)
        pre_append_data.append(x)
    except:
        pre_append_data = x

    json_stuff = json.dumps(pre_append_data, indent=4)
    with open(f'{dir_path}/managers.json', 'w') as file:
        file.write(json_stuff)
        file.close()
    
    # player_ids.json
    x = {}
    file = open('./data/player_ids.json', 'r')
    try:
        data = json.load(file)
    except:
        data = ''
    file.close()
    if data == "":
        player_id = 1001
        for i in player_stuff:
            for j in i[1]:
                player_name = f'{j['Player Fname']} {j['Player Lname']}'
                x[player_name] = player_id
                player_id += 1
        x = json.dumps(x, indent=4)
    else:
        names = list(data.keys())
        player_id = max(list(data.values())) + 1
        for i in player_stuff:
            for j in i[1]:
                player_name = f'{j['Player Fname']} {j['Player Lname']}'
                if player_name not in names:
                    x[player_name] = player_id
                    player_id += 1
        data.update(x)
        x = json.dumps(data, indent=4)

    with open(f'./data/player_ids.json', 'w') as file:
        file.write(x)
        file.close()

    # manager_ids.json
    x = {}
    file = open('./data/manager_ids.json', 'r')
    try:
        data = json.load(file)
    except:
        data = ''
    file.close()
    if data == "":
        manager_id = 1
        for i in player_stuff:
            for j in i[3]:
                manager_name = f'{j['Manager Fname']} {j['Manager Lname']}'
                x[manager_name] = manager_id
                manager_id += 1
        x = json.dumps(x, indent=4)
    else:
        names = list(data.keys())
        manager_id = max(list(data.values())) + 1
        for i in player_stuff:
            for j in i[3]:
                manager_name = f'{j['Manager Fname']} {j['Manager Lname']}'
                if manager_name not in names:
                    x[manager_name] = manager_id
                    manager_id += 1
        data.update(x)
        x = json.dumps(data, indent=4)

    with open(f'{dir_path}/../manager_ids.json', 'w') as file:
        file.write(x)
        file.close()

    # NO MATCH_IDS.JSON, Its only used within the trigger so no need to keep track of it
    
    # Player_history.json
    x = []
    file = open('./data/player_ids.json', 'r')
    data_id = json.load(file)
    file.close()
    file = open('./data/player_history.json', 'r')
    try:
        data_history = json.load(file)
    except:
        data_history = ''
    file.close()

    for i in player_stuff:
        for j in i[0]:
            j['Player ID'] = data_id[j['Player Name']]
            x.append(j)

    if data_history != "":
        data = data_history + x
    else:
        data = x

    x = json.dumps(data, indent=4)
    with open(f'{dir_path}/../player_history.json', 'w') as file:
        file.write(x)
        file.close()
    
    # manger_history.json
    x = []
    file = open('./data/manager_ids.json', 'r')
    data_id = json.load(file)
    file.close()
    file = open('./data/manager_history.json', 'r')
    try:
        data_history = json.load(file)
    except:
        data_history = ''    
    file.close()

    for i in player_stuff:
        for j in i[2]:
            j['Manager ID'] = data_id[j['Manager Name']]
            x.append(j)

    if data_history != "":
        data = data_history + x
    else:
        data = x
        
    x = json.dumps(data, indent=4)
    with open(f'{dir_path}/../manager_history.json', 'w') as file:
        file.write(x)
        file.close()
