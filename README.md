# Golazo Webscraper

This is a webscraper for a database named Golazo. It scrapes the data off of [PlayerMakerStats](https:www.playermakerstats.com). Its capable of scraping data for various football leagues, including teams, players, managers, and matches for a given league and year.

## Why I made this

I create this web scraper to simplify the process of gathering football data needed to create a database for my database class (CSC 365 Jenny Wang). The project needed a file full of statements. Our team knew that creating MySQL statements is tedious and exhausting. So, I decided to scrape the data and use the data given to create a large database. This may have been more work since initially we were expecting to create around 300+ statements (and to be fair, is was more work than needed), but we are now able to use thousands of statements to populate the database. This tool not only saves time but also allows us to work with a much larger dataset, enabling for a more comprehensive database
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
    pip install -r requirements.txt

    ```
## Usage

To use the PlaymakerStats web scraper, follow these steps:

1. Open `generate_json.py` in your preferred text editor.

2. Set the `league` and `year` variables to the desired league and year for which you want to scrape data.

3. Run the script:

    ```bash
    python generate_json.py
    ```

4. The scraped data will be saved in JSON format in the `data` directory.

## Supported Leagues

Currently, the script supports scraping data for the following leagues:

- Premier League

## Sample Output

The scraped data includes the following information:

- Teams: Team name, league, city, stadium, year of founding.
- Players: Player name, position, age, height, weight, nationality.
- Managers: Manager name, nationality age, manager nationality.
- Player History: Team played for, season, player number.
- Manager History: Team managed for, season
- Matches: Match date, home team, away team, final score, match date, league

