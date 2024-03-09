from teams import *
from players import *
from match import *
import json
import os

if '__name__' == '__main__':
        
    # leagues
    premier = "https://www.playmakerstats.com/competition/premier-league"
    liga = "https://www.playmakerstats.com/competition/la-liga"
    serie = "https://www.playmakerstats.com/competition/serie-a"
    bundesliga_1 = "https://www.playmakerstats.com/competition/1-bundesliga"
    ligue_1 = "https://www.playmakerstats.com/competition/ligue-1"
    league_urls = [premier, liga, serie, bundesliga_1, ligue_1]

    # parameters
    season_of_interest = '20'
    driver = webdriver.Chrome()

    # args
    for i in league_urls:
        league_season = get_season_link(i, driver, season_of_interest)
        team_stuff = team_data(league_season, driver)
        player_stuff = league_player_data(league_season, driver)
        match_stuff = season_match_data(league_season, driver)

    # make directory for jsons
    dir_path = f'./../data/{full_season(season_of_interest)}'
    try:
        os.mkdir(dir_path, mode = 0o666)
        f = open(f'{dir_path}/players.json', 'x')
        f = open(f'{dir_path}/managers.json', 'x')
        f = open(f'{dir_path}/match.json', 'x')
        f = open(f'{dir_path}/teams.json', 'x')
        f = open(f'{dir_path}/player_history.json', 'x')
        f = open(f'{dir_path}/manager_history.json', 'x')
        f = open(f'{dir_path}/player_ids.json', 'x')
        f = open(f'{dir_path}/manager_ids.json', 'x')
        f = open(f'{dir_path}/match_ids.json', 'x')
    except:
        print('Data is already stored')

    # jsons 
        
    # create player_insert.sql
