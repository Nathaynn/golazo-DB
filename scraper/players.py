from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from teams import open_url
from time import sleep

# get data for every team within a league + season

def league_player_data(url, driver):
    open_url(url, driver)
    sleep(2)
        
    # handle adblocker window
    chld = driver.window_handles[1]
    driver.switch_to.window(chld)
    driver.close()
    current_tab=driver.window_handles[0]
    driver.switch_to.window(current_tab)

    # table full of each team
    team_table = driver.find_element(By.ID, 'page').find_element(By.ID,'edition_table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
    player_history= []
    players = []
    manager_history = []
    managers = []
    for i in team_table:
        # grab team name + link to team stats.
        href_area = i.find_element(By.CLASS_NAME, 'text').find_element(By.TAG_NAME, 'a')
        team_id = href_area.get_attribute('innerHTML')
        href = href_area.get_attribute('href')

        # open tab and check out the team stats
        driver.execute_script("window.open('https://www.google.com')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(href)

        # locate each squad player
        # each box seperates the goalkeepers, defenders, midfielders, and forwards
        squad_table = driver.find_element(By.ID, 'page').find_element(By.ID, 'team_squad').find_elements(By.CLASS_NAME, 'innerbox')
        manager_table = driver.find_element(By.ID, 'page').find_element(By.ID, 'team_staff').find_element(By.CLASS_NAME, 'staff_line').find_element(By.CLASS_NAME, 'text').find_element(By.TAG_NAME, 'a')
        for j in squad_table:
            position = j.find_element(By.CLASS_NAME, 'title').get_attribute('innerHTML')
            staff_lines = j.find_elements(By.CLASS_NAME, 'staff_line')
            for g in staff_lines:
                staff = g.find_elements(By.CLASS_NAME, 'staff')
                # quadruple loop :O
                for y in staff:
                    player = y.find_element(By.CLASS_NAME, 'text').find_element(By.TAG_NAME, 'a')
                    player_link = player.get_attribute('href')

                    # player history
                    hist = {}
                    hist['Team Name'] = team_id
                    hist['Player Number'] = y.find_element(By.CLASS_NAME, 'number').get_attribute('innerHTML')
                    hist['Season Year'] = (Select(driver.find_element(By.ID, 'page').find_element(By.TAG_NAME, 'form').find_element(By.TAG_NAME, 'select'))).first_selected_option.get_attribute('innerHTML')

                    player_stuff = player_data(player_link, driver)                    
                    player_stuff['Player Position'] = position
                    hist['Player Name'] = f'{player_stuff['Player Fname']} {player_stuff['Player Lname']}'
                    player_history.append(hist)
                    players.append(player_stuff)

                    # debugging
                    print(player_stuff)
                    print(hist)
        manager_link = manager_table.get_attribute('href')
        manager_stuff = manager_data(manager_link, driver)
        managers.append(manager_stuff)
        manager_hist = {}
        manager_hist['Team Name'] = team_id 
        manager_hist['Manager Name'] = f'{manager_stuff['Manager Fname']} {manager_stuff['Manager Lname']}'
        manager_hist['Season Year'] = (Select(driver.find_element(By.ID, 'page').find_element(By.TAG_NAME, 'form').find_element(By.TAG_NAME, 'select'))).first_selected_option.get_attribute('innerHTML')
        manager_history.append(manager_hist)
        print(manager_stuff)
        print(manager_hist)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    return [player_history, players, manager_history, managers]

# data for a SINGLE player
def player_data(url, driver):
    # store current tab and go to player tab
    driver.execute_script("window.open('https://www.google.com')")
    current_window = driver.current_window_handle
    player_window = len(driver.window_handles) - 1
    driver.switch_to.window(driver.window_handles[player_window])
    driver.get(url)
    sleep(1)

    # each div within bio can't be uniquely identified without looking inside inside each element
    # check each div. if it has the stuff we want then commit, else ignore
    important_stuff = ['Name', 'Height', 'Weight', 'Nationality', 'Born/Age']
    bio = driver.find_element(By.ID, 'entity_bio')
    bios = bio.find_elements(By.CLASS_NAME, 'bio')
    bios += bio.find_elements(By.CLASS_NAME, 'bio_half')
    player_fname = ''
    player_lname = ''
    player_age = 0
    player_height = 0
    player_weight = 0
    player_nationality = ''
    for i in bios:
        try:
            span = i.find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
        except:
            continue
        if span in important_stuff:
            if span == 'Name':
                temp_name = i.get_attribute('innerHTML').replace('<span>Name</span>', "")
                temp_name = temp_name.split()
                player_fname = temp_name[0]
                player_lname = temp_name[-1]
            elif span == 'Height':
                temp_height = i.get_attribute('innerHTML').replace('<span>Height</span>', "")
                temp_height = temp_height.split()
                player_height = int(temp_height[0])
            elif span == 'Weight':
                temp_weight = i.get_attribute('innerHTML').replace('<span>Weight</span>', "")
                temp_weight = temp_weight.split()
                player_weight = int(temp_weight[0])
            elif span == 'Nationality':
                player_nationality = i.find_element(By.CLASS_NAME, 'text').get_attribute('innerHTML')
            elif span == 'Born/Age':
                temp_age = i.find_element(By.CLASS_NAME, 'small').get_attribute('innerHTML')[1:]
                temp_age = temp_age.split()
                player_age = int(temp_age[0])
    # close and return
    driver.close()
    driver.switch_to.window(current_window)
    return {'Player Fname': player_fname, 'Player Lname': player_lname, 'Player Age': player_age, 'Player Height': player_height, 'Player Weight': player_weight, 'Player Nationality': player_nationality}

def manager_data(url, driver):
    driver.execute_script("window.open('https://www.google.com')")
    current_window = driver.current_window_handle
    player_window = len(driver.window_handles) - 1
    driver.switch_to.window(driver.window_handles[player_window])
    driver.get(url)

    important_stuff = ['Name', 'Nationality', 'Born/Age']
    bio = driver.find_element(By.ID, 'entity_bio')
    bios = bio.find_elements(By.CLASS_NAME, 'bio')
    bios += bio.find_elements(By.CLASS_NAME, 'bio_half')
    manager_fname = ''
    manager_lname = ''
    manager_age = 0
    manager_nationality = ''
    for i in bios:
        try:
            span = i.find_element(By.TAG_NAME, 'span').get_attribute('innerHTML')
        except:
            continue
        if span in important_stuff:
            if span == 'Name':
                temp_name = i.get_attribute('innerHTML').replace('<span>Name</span>', "")
                temp_name = temp_name.split()
                manager_fname = temp_name[0]
                manager_lname = temp_name[-1]
            elif span == 'Nationality':
                manager_nationality = i.find_element(By.CLASS_NAME, 'text').get_attribute('innerHTML')
            elif span == 'Born/Age':
                temp_age = i.find_element(By.CLASS_NAME, 'small').get_attribute('innerHTML')[1:]
                temp_age = temp_age.split()
                manager_age = int(temp_age[0])
    driver.close()
    driver.switch_to.window(current_window)
    return {'Manager Fname': manager_fname, 'Manager Lname': manager_lname, 'Manager Age': manager_age, 'Player Nationality': manager_nationality}

"""
driver = webdriver.Chrome()
x = league_player_data('https://www.playmakerstats.com/edition/premier-league-2022-2023/165592', driver)
"""