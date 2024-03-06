from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import json
"""
with open('./data/leagues.json', 'r') as f:
    leagues = json.loads(f.read())
url = "https://fbref.com/en/"

driver = webdriver.Chrome()
driver.get(url)      

# get leagues + their corresponding team
drop_league_button = Select(driver.find_element(By.NAME, 'league_val'))

arr_of_teams = []

for i in leagues:
    drop_league_button.select_by_visible_text(i["league_name"])

    drop_club_button = driver.find_element(By.ID, 'team_choice')

    clubs = [x.get_attribute('innerHTML') for x in drop_club_button.find_elements(By.TAG_NAME, 'option')]
    clubs.pop(0)
    for j in clubs:
        x = {'league_name': i}
        x['team_name'] = j
        arr_of_teams.append(x)

# arr_of_teams = [{league_name: name, team_name: name_2}, ...]
# needs city, stadium, and year of founding

sleep(10)
"""
def open_json(file_path):
    with open(file_path, 'r') as f:
        json_file = json.loads(f.read())
    return json_file

def open_url(url, driver):
    driver.get(url)
    sleep(2)

# example, input is the year 22, which represents the 2022/23 season
def full_season(season):
    num_season = int(season) + 1
    if num_season < 10:
        season = f'20{season}/0{str(num_season)}'
    else:
        season = f'20{season}/{str(num_season)}'
    return season

def gather_player_data(url, driver, season):
    open_url(url, driver)
    seasons_menu = driver.find_element(By.ID, 'page')
    seasons_menu = seasons_menu.find_element(By.CLASS_NAME, 'combo')
    seasons_menu = seasons_menu.find_element(By.ID, 'id_edicao')

    # came across issue with select and options, so settled with creating the link instead
    season = full_season(season)
    for i in seasons_menu.find_elements(By.TAG_NAME, 'option'):
        if i.get_attribute('innerHTML') == season:
            value = i.get_attribute('value')
            break
    value = '-' + season[0:4] + '-20' + season[5:7] + '/' + value
    link = 'https://www.playmakerstats.com/edition/' + value
    open_url(link, driver)

    # website will change to full stats page for a given season, go to each team and record data
    sleep(2)

# leagues
premier = "https://www.playmakerstats.com/competition/premier-league"
liga = "https://www.playmakerstats.com/competition/la-liga"
serie = "https://www.playmakerstats.com/competition/serie-a"
bundesliga_1 = "https://www.playmakerstats.com/competition/1-bundesliga"
bundesliga_2 = "https://www.playmakerstats.com/competition/2-bundesliga"
league_urls = [premier, liga, serie, bundesliga_1, bundesliga_2]

# web stuff
driver = webdriver.Chrome()

gather_player_data(league_urls[0], driver, '21')
print('nice')