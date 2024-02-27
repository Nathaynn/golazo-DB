from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import json

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