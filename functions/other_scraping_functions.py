import pandas as pd
import sys

sys.path.insert(1, "/Users/jonahyallop/Documents/Colchester United")

import utils.scraping_utils as utils


def scrape_southern_football_league(url: str) -> dict:
    """Function to scrape player data from the southern football league.

    Args:
        url (str): URL path to scrape from.
    Returns:
        dict: Dictionary containing scraped data.
    """
    # Get HTML code
    pageSoup = utils.get_website_html(url=url)

    # Extract player data from HTML code
    multistats = pageSoup.find_all("tr")[2:]

    # Save to dictionary
    scraped_data = {
        "multistats": multistats,
    }

    return scraped_data


def convert_southern_league_data_to_frame(scraped_data: dict) -> pd.DataFrame:
    """Function to convert southern football league player data to dataframe.

    Args:
        scraped_data (dict): Dictionary containing raw scraped data.
    Returns:
        pd.DataFrame: Dataframe containing player information:
            - Name
            - Position
            - Age
            - Appearances (+ sub app)
            - League Goals
    """
    multistats = scraped_data["multistats"]
    
    players = []
    positions = []
    age = []
    appearances = []
    sub = []
    goals = []

    for i in range(0, len(multistats)):
        # Get player name
        players.append(multistats[i].find_all("td")[0].text.strip())
        # Get positions
        positions.append(multistats[i].find_all("td")[1].text.strip())
        # Get player age
        age.append(multistats[i].find_all("td")[2].text.strip()[:2])
        # Get number of appearances
        appearances.append(multistats[i].find_all("td")[3].text.strip().replace("-", ""))
        # Get sub appearances
        sub.append(multistats[i].find_all("td")[4].text.strip().replace("-", ""))
        # Get number of goals
        goals.append(multistats[i].find_all("td")[5].text.strip().replace("-", ""))

    # Save to dataframe
    final_df = pd.DataFrame(
        {
            "Player": players,
            "Position": positions,
            "Age": age,
            "Appearances": appearances,
            "As Sub": sub,
            "League Goals": goals,
        }
    )

    return final_df
