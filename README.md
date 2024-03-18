# Golazo Webscraper

This is a webscraper for a database project named Golazo. It scrapes the data off of [PlayerMakerStats](https:www.playermakerstats.com). Its capable of scraping data for various football leagues, including teams, players, managers, and matches for a given league and year.

## Why I made this

I created this web scraper to simplify the process of gathering football data needed to create a database for a class (CSC 365). The project needed a file full of insert statements. Creating MySQL statements is tedious and exhausting. So, I decided to scrape the data and use the data given to create a large database. This may have been more work since initially we were expecting to create around 300+ statements (and to be fair, this was more work than needed), but we are now able to use thousands of statements to populate the database. This tool not only saves time but also allows us to work with a much larger dataset, enabling for a more comprehensive database
## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Nathaynn/golazo-DB.git
    ```

2. Navigate to the project directory:

    ```bash
    cd golazo-DB
    ```

3. Install the required Python packages using pip:

    ```bash
    pip3 install -r requirements.txt

    ```
## Usage

To use the web scraper, follow these steps:

1. Open `generate_json.py` in your preferred text editor.

2. Set the `league_focus` and `season_of_interest` variables to the desired league and year for which you want to scrape data. NOTE: You need chrome installed.

3. Run the script:

    ```bash
    python3 generate_json.py
    ```

4. The scraped data will be saved in JSON format in the `data` directory.

## Supported Leagues

Currently, the script supports scraping data for the following leagues (as I know of):

- Premier League
- La Liga

## Sample Output

The scraped data includes the following information:

- Teams: Team name, league, city, stadium, year of founding.
- Players: Player name, position, age, height, weight, nationality.
- Managers: Manager name, nationality age, manager nationality.
- Player History: Team played for, season, player number.
- Manager History: Team managed for, season
- Matches: Match date, home team, away team, final score, match date, league

## Known Issues and Unsupported Instances

I wrote this code for a class project, so I didn't write for reliable real-life usage. While the web scraper is designed to handle various football leagues and seasons, there may be instances where certain leagues or seasons are not supported or encountered unexpected issues. Here are some known issues and unsupported instances:

- **Unsupported Leagues**: Some football leagues may have unique formatting or structures that are not currently supported by the web scraper. As a result, scraping data for these leagues may not yield accurate results.

- **Unexpected Behavior**: Due to changes in the website structure or data presentation on PlaymakerStats, the scraper may encounter unexpected behavior or errors during the scraping process. This could result in incomplete or inaccurate data being scraped. This is apparent when scraping data off a season that is currently being played.

- **Bugs and Limitations**: The scraper may contain bugs or limitations that affect its functionality, such as failure to handle certain edge cases.


