from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from teams import open_url


def season_match_data(url, driver):
    open_url(url, driver)
    sleep(2)
    
    # handle adblocker window
    chld = driver.window_handles[1]
    driver.switch_to.window(chld)
    driver.close()
    current_tab=driver.window_handles[0]
    driver.switch_to.window(current_tab)
    sleep(2)

    # go back to orignal tab
    driver.execute_script("window.stop();")
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
        ActionChains(driver).click(driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[4].find_element(By.TAG_NAME, 'div')).perform()
        sleep(1)

        options = driver.find_element(By.ID, 'page').find_element(By.ID, 'team_filters').find_elements(By.TAG_NAME, 'label')[4].find_element(By.CLASS_NAME, 'chosen-drop').find_element(By.TAG_NAME, 'ul').find_elements(By.CLASS_NAME, 'active-result')
        type_area = driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[4].find_element(By.CLASS_NAME, 'chosen-search').find_element(By.TAG_NAME, 'input')
        for p in options:
            if p.get_attribute('innerHTML') == focus_year:
                type_area.send_keys(focus_year)
                type_area.send_keys(Keys.ENTER)
                break

        # go to select and pick league of focus
        # no matter what, this only works with 2 clicks, i'm not sure why but yeah
        ActionChains(driver).click(driver.find_element(By.ID, 'page').find_elements(By.CLASS_NAME, 'chosen-single')[2].find_element(By.TAG_NAME, 'div')).perform()
        ActionChains(driver).click(driver.find_element(By.ID, 'page').find_elements(By.CLASS_NAME, 'chosen-single')[2].find_element(By.TAG_NAME, 'div')).perform()
        sleep(1)
        type_area = driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[2].find_element(By.CLASS_NAME, 'chosen-search').find_element(By.TAG_NAME, 'input')  
        options = driver.find_element(By.ID, 'page').find_elements(By.TAG_NAME, 'label')[2].find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
        for p in options:
            if p.text == focus_league:
                type_area.send_keys(focus_league)
                type_area.send_keys(Keys.ENTER)
                break

        # page loaded and now do cool stuff
        while next_link_condition:
            # for some reason, the website likes to have two different team_games elements on the first page of matches, afterwards only 1 exists
            try:
                game_table = driver.find_element(By.ID, 'page').find_elements(By.ID, 'team_games')[1].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            except:
                game_table = driver.find_element(By.ID, 'page').find_elements(By.ID, 'team_games')[0].find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            for j in game_table:
                # some tables aren't a game and instead padding, so if error occurs just ignore the element and go to next
                try:
                    game_date = j.find_element(By.CLASS_NAME, 'double').get_attribute('innerHTML')
                except:
                    continue
                league_name = focus_league
                season_year = focus_year
                home_condition = j.find_elements(By.TAG_NAME, 'td')[3].get_attribute('innerHTML')
                other_team = j.find_elements(By.TAG_NAME, 'td')[4].find_element(By.TAG_NAME, 'a').get_attribute('innerHTML')
                if home_condition == '(A)':
                    home = other_team
                    away = team_name
                else:
                    home = team_name
                    away = other_team
                score = j.find_element(By.CLASS_NAME, 'result').find_element(By.TAG_NAME, 'a').get_attribute('innerHTML')
                for g in range(len(score)):
                    if score[g] == '-':
                        home_score = score[0:g]
                        away_score = score[g+1:]

                # COULDNT FIND ATTENDANCE ANYWHERE :(
                full_match = {'Home Team': home, 'Away Team': away, 'Home Score': home_score, 'Away Score': away_score, 'Game Date': game_date, 
                'League': league_name, 'Season': season_year}
                # debugging
                print(full_match)
                if full_match not in league_matches:
                    league_matches.append(full_match)
            try:
                next_page = driver.find_element(By.ID, 'page').find_element(By.CLASS_NAME, 'next-link').get_attribute('href')
                driver.get(next_page)
                sleep(2)
            except:
                next_link_condition = False
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    return league_matches
"""
chop = webdriver.ChromeOptions()
chop.add_extension('./adblock/Adblock.crx')
driver = webdriver.Chrome(chop)
season_match_data("https://www.playmakerstats.com/edition/serie-a-2021-2022/156515", driver)
"""
