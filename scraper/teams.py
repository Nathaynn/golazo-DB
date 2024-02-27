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

drop_league_button = Select(driver.find_element(By.NAME, 'league_val'))

arr_of_teams = []
for i in leagues:
    x = {}
    drop_league_button.select_by_visible_text(i["league_name"])

    drop_club_button = driver.find_element(By.ID, 'team_choice')

    clubs = [x.get_attribute('innerHTML') for x in drop_club_button.find_elements(By.TAG_NAME, 'option')]
    clubs.pop(0)
    print(clubs)

sleep(10)