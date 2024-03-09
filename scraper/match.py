from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from time import sleep
from teams import open_url
import json


def season_match_data(url, driver):
    open_url(url, driver)

    team_table = driver.find_element(By.ID, 'page').find_element(By.ID,'edition_table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    focus_league = driver.find_element(By.ID, 'page').find_element(By.CLASS_NAME, 'zz-enthdr-data').find_element(By.TAG_NAME, 'span')
    focus_league = focus_league.get_attribute('innerHTML')
    if '20' in focus_league:
        focus_league = focus_league[0:focus_league.find('20')-1]
    else:
        focus_league = focus_league[0:focus_league.find('19')-1]

    league_matches = []
    for i in team_table:
        next_link_condition = True

        href_area = i.find_element(By.CLASS_NAME, 'text').find_element(By.TAG_NAME, 'a')
        team_name = href_area.get_attribute('innerHTML')
        href = href_area.get_attribute('href')

        # open new tab and go to a teams match history
        driver.execute_script('window.open("https://www.google.com")')
        driver.switch_to.window(driver.window_handles[1])
        driver.get(href)
        href = driver.find_element(By.ID, 'page').find_element(By.CLASS_NAME, 'zz-enthdr-bottom').find_element(By.CLASS_NAME, 'h2').find_elements(By.TAG_NAME, 'span')[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
        # year of the matches
        
        focus_year = driver.find_element(By.ID, 'page').find_element(By.CLASS_NAME, 'chosen-single').find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
        driver.get(href)

        # go to select and pick the year of focus
        ActionChains(driver).click(driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[4].find_element(By.TAG_NAME, 'div')).perform()
        options = driver.find_element(By.ID, 'page').find_element(By.ID, 'team_filters').find_elements(By.TAG_NAME, 'label')[4].find_element(By.CLASS_NAME, 'chosen-drop').find_element(By.TAG_NAME, 'ul').find_elements(By.CLASS_NAME, 'active-result')
        type_area = driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[4].find_element(By.CLASS_NAME, 'chosen-search').find_element(By.TAG_NAME, 'input')
        for p in options:
            if p.get_attribute('innerHTML') == focus_year:
                type_area.send_keys(focus_year)
                type_area.send_keys(Keys.ENTER)
                break

        # go to select and pick league of focus
        ActionChains(driver).click(driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[2].find_element(By.TAG_NAME, 'div')).perform()
        ActionChains(driver).click(driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[2].find_element(By.TAG_NAME, 'div')).perform()
        type_area = driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[2].find_element(By.CLASS_NAME, 'chosen-search').find_element(By.TAG_NAME, 'input')  
        options = driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[2].find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
        for p in options:
            if p.text == focus_league:
                type_area.send_keys(focus_league)
                type_area.send_keys(Keys.ENTER)
                break
        sleep(10)
        # page loaded and now do cool stuff
        while next_link_condition:
            game_table = driver.find_element(By.ID, 'page').find_element(By.ID, 'team_games').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            for j in game_table:
                game_date = j.find_element(By.CLASS_NAME, 'double').get_attribute('innerHTML')
                league_name = focus_league
                season_year = focus_year
                home_condition = j.find_elements(By.TAG_NAME, 'td')[3].get_attribute('innerHTML')
                other_team = j.find_elements(By.TAG_NAME, 'td')[4].get_attribute('innerHTML')
                if home_condition == '(A)':
                    home = other_team
                    away = team_name
                else:
                    home = team_name
                    away = other_team
                score = j.find_element(By.CLASS_NAME, 'result').get_attribute('innerHTML')
                score = [*score]
                for g in range(len(score)):
                    if score[g] == '-':
                        home_score = score[0:g]
                        away_score = score[g+1:]

                # COULDNT FIND ATTENDANCE ANYWHERE :(
                full_match = {'Home Team': home, 'Away Team': away, 'Home Score': home_score, 'Away Score': away_score, 'Game Date': game_date, 
                'League': league_name, 'Season': season_year}
                if full_match not in league_matches:
                    league_matches.append(full_match)
            try:
                next_page = driver.find_element(By.ID, 'page').find_element(By.CLASS_NAME, 'next-link').get_attribute('href')
                driver.get(next_page)
            except:
                next_link_condition = False
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # finish collecting match data for a team

driver = webdriver.Chrome()
season_match_data("https://www.playmakerstats.com/edition/premier-league-2022-2023/165592", driver)

