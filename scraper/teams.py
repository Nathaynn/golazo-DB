from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

def open_url(url, driver):
    driver.get(url)

# example, input is the year 22, which represents the 2022/23 season
def full_season(season):
    num_season = int(season) + 1
    if num_season < 10:
        season = f'20{season}/0{str(num_season)}'
    elif num_season > 30:
        season = f'19{season}/{str(num_season)}'
    else:
        season = f'20{season}/{str(num_season)}'
    return season

def get_season_link(url, driver, season):
    # open website
    open_url(url, driver)

    # select season
    seasons_menu = driver.find_element(By.ID, 'page')
    seasons_menu = seasons_menu.find_element(By.CLASS_NAME, 'combo')
    seasons_menu = seasons_menu.find_element(By.ID, 'id_edicao')

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
    sleep(2)

    # handle adblocker window
    chld = driver.window_handles[1]
    driver.switch_to.window(chld)
    driver.close()
    current_tab=driver.window_handles[0]
    driver.switch_to.window(current_tab)
    sleep(2)

    # other stuff
    l_name = driver.find_element(By.ID, 'page').find_element(By.CLASS_NAME, 'zz-enthdr-data').find_element(By.TAG_NAME, 'span')
    l_name = l_name.get_attribute('innerHTML')
    if '20' in l_name:
        l_name = l_name[0:l_name.find('20')-1]
    else:
        l_name = l_name[0:l_name.find('19')-1]


    # go back to orignal tab
    driver.execute_script("window.stop();")
    cool_team_stuff = []
    team_table = driver.find_element(By.ID, 'page').find_element(By.ID,'edition_table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    for i in team_table:
        i = i.find_element(By.CLASS_NAME, 'text').find_element(By.TAG_NAME, 'a')
        team_name = i.get_attribute('innerHTML')
        href_link = i.get_attribute('href')
        driver.execute_script("window.open('https://www.google.com')")
        driver.switch_to.window(driver.window_handles[1])
        sleep(1)
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
            else:
                team_city = f'{team_city} {team_cy[j]}'

        team_year = int(team_cy[city_cutoff + 2])
        stad = driver.find_element(By.ID, 'page').find_element(By.CLASS_NAME, 'faq').find_element(By.CLASS_NAME, 'text')
        stad = stad.get_attribute('innerHTML').split()
        stadium_cutoff = stad.index('is')
        team_stadium = ''
        for j in range(stadium_cutoff):
            if team_stadium == '':
                team_stadium = stad[0]
            else:
                team_stadium += " " + stad[j]
            
        # go back to original page and append data
        team_dict= {}
        team_dict['Team League'] = l_name
        team_dict['Team Name'] = team_name
        team_dict['Team City'] = team_city
        team_dict['Team Founded'] = team_year
        team_dict['Team Stadium'] = team_stadium
        cool_team_stuff.append(team_dict)
        # debugging
        print(team_dict)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    return cool_team_stuff

        
"""
if __name__ == '__main__':
    
    # leagues
    premier = "https://www.playmakerstats.com/competition/premier-league"
    liga = "https://www.playmakerstats.com/competition/la-liga"
    serie = "https://www.playmakerstats.com/competition/serie-a"
    bundesliga_1 = "https://www.playmakerstats.com/competition/1-bundesliga"
    league_urls = [premier, liga, serie, bundesliga_1]

    # web stuff
    chop = webdriver.ChromeOptions()
    chop.add_extension('./adblock/Adblock.crx')
    driver = webdriver.Chrome(chop)

    x = get_season_link(league_urls[0], driver, '21')
    team_data(x, driver)
"""