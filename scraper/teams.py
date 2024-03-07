from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import json

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

def get_season_link(url, driver, season):
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
    return 'https://www.playmakerstats.com/edition/' + value

# assume URL is from get_season_link
def team_data(url, driver):
    open_url(url, driver)
    cool_team_stuff = []
    team_table = driver.find_element(By.ID, 'page').find_element(By.ID,'edition_table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    for i in team_table:
        i = i.find_element(By.CLASS_NAME, 'text').find_element(By.TAG_NAME, 'a')
        team_name = i.get_attribute('innerHTML')
        href_link = i.get_attribute('href')
        driver.execute_script("window.open('https://www.google.com')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(href_link)
        # page change -> team stats for season
        team_elements = driver.find_element(By.ID, "page").find_element(By.CLASS_NAME, 'zz-enthdr-info').find_element(By.CLASS_NAME, 'info')
        team_foo = team_elements.find_elements(By.TAG_NAME, 'span')
        for j in team_foo:
            team_cy = team_elements.text.replace(j.text, "").split()
        city_cutoff = team_cy.index('established')
        team_city = ''
        for j in range(city_cutoff):
            if team_city == '':
                team_city = f'{team_cy[0]}'
            team_city = f'{team_city} {team_cy[j]}'
        team_year = int(team_cy[city_cutoff + 2])
        # go back to original page and append data
        team_dict= {}
        team_dict['Team Name'] = team_name
        team_dict['Team City'] = team_city
        team_dict['Team Founded'] = team_year
        cool_team_stuff.append(team_dict)
        print(team_dict)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        sleep(2)

        
    

if __name__ == '__main__':
    # leagues
    premier = "https://www.playmakerstats.com/competition/premier-league"
    liga = "https://www.playmakerstats.com/competition/la-liga"
    serie = "https://www.playmakerstats.com/competition/serie-a"
    bundesliga_1 = "https://www.playmakerstats.com/competition/1-bundesliga"
    bundesliga_2 = "https://www.playmakerstats.com/competition/2-bundesliga"
    league_urls = [premier, liga, serie, bundesliga_1, bundesliga_2]

    # web stuff
    driver = webdriver.Chrome()

    x = get_season_link(league_urls[0], driver, '21')
    team_data(x, driver)