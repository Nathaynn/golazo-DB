from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from teams import open_url, get_season_link
import json

# get data for every team within a league + season
# also note that this grabs the managers stuff too

def league_player_data(url, driver):
    open_url(url, driver)

    # table full of each team
    team_table = driver.find_element(By.ID, 'page').find_element(By.ID,'edition_table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    for i in team_table:
        # grab team name + link to team stats. NOTE that team_id is just the name, will change with values once we have a cohesive way of determining id's
        href_area = i.find_element(By.CLASS_NAME, 'text').find_element(By.TAG_NAME, 'a')
        team_id = href_area.get_attribute('innerHTML')
        href = href_area.get_attribute('href')

        # open tab and check out the team stats
        driver.execute_script('window.open(https://www.google.com)')
        driver.switch_to.window(driver.window_handles[1])
        driver.get(href)

        # locate each squad player
        # each box seperates the goalkeepers, defenders, midfielders, and forwards
        players = []
        squad_table = driver.find_element(By.ID, 'page').find_element(By.ID, 'team_squad').find_elements(By.CLASS_NAME, 'innerbox')
        for j in squad_table:
            position = j.find_element(By.CLASS_NAME, 'title').get_attribute('innerHTML')
            staff_lines = j.find_elements(By.CLASS_NAME, 'staff_line')
            for g in staff_lines:
                staff = g.find_elements(By.CLASS_NAME, 'staff')
                # quadruple loop :O
                for y in staff:
                    player = staff.find_element(By.TAG_NAME, 'a')
                    player_link = player.get_attribute('href')
                    player_stuff = player_data(player_link, driver)                    
                    player_stuff['Player Position'] = position
                    players.append(player_stuff)
        driver.close()
        driver.swith_to.window(driver.window_handles[0])

# data for a SINGLE player
def player_data(url, driver):
    pass