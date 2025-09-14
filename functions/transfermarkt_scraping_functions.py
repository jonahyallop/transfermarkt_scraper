import pandas as pd
import sys

sys.path.insert(1, "/Users/jonahyallop/Documents/Colchester United")

import utils.scraping_utils as utils


def scrape_player_data(url: str) -> dict:
    """Function to scrape player data from Transfermarkt

    Args:
        url (str): Website URL to scrape from.
    Returns:
        dict: Dictionary containing scraped player data.
    """
    # Get HTML code
    pageSoup = utils.get_website_html(url=url)

    # Extract player data from HTML code
    players = pageSoup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})
    multistats = pageSoup.find_all("td", {"class": "zentriert"})
    market_values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
    positions = pageSoup.find_all("tr")[4::3]

    scraped_data = {
        "players": players,
        "multistats": multistats,
        "positions": positions,
        "market_values": market_values,
    }

    return scraped_data


def scrape_agent_data(url: str) -> dict:
    """Function to scrape player agent data from Transfermarkt.

    Args:
        url (str): Website URL to scrape from.
    Returns:
        dict: Dictionary containing scraped agent data.
    """
    # Get HTML code
    pageSoup = utils.get_website_html(url=url)

    # Get player names to merge onto other scraped data
    players = pageSoup.find_all("td", {"class": "hauptlink"})[::2]

    # Get agents for each player
    agents = pageSoup.find_all("td", {"class": "rechts"})
    agent_data = {"players": players, "agents": agents}

    return agent_data


def convert_agent_data_to_dataframe(scraped_data: dict) -> pd.DataFrame:
    """Function to convert agent information into a dataframe

    Args:
        scraped_data (dict): Dictionary containing players and their agents
    Returns:
        pd.DataFrame
    """

    players = scraped_data["players"]
    agents = scraped_data["agents"]

    players_list, agents_list = [], []

    # 1. Get list of players
    for i in range(0, len(players)):
        players_list.append(str(players[i]).split('" title="')[-1].split('">')[0])

    # Get list of agents
    for i in range(0, len(players)):
        agents_list.append(agents[i].text)

    # Compile data into a dataframe
    final_df = pd.DataFrame(
        {
            "Player": players_list,
            "Agent": agents_list,    
        }
    )

    return final_df


def convert_player_data_to_dataframe(scraped_data: dict) -> pd.DataFrame:
    """Function to convert general player information into dataframe

    Args:
        scraped_data (dict): _description_
    Returns:
        pd.DataFrame
    """
    # Load in scraped data
    players = scraped_data["players"]
    multistats = scraped_data["multistats"]
    positions = scraped_data["positions"]
    market_values = scraped_data["market_values"]

    players_list = []
    age_list = []
    dob_list = []
    position_list = []
    nationality_list = []
    market_values_list = []
    height_list = []
    foot_list = []
    join_date_list = []
    prev_club_list = []
    contract_list = []

    # Convert HTML into readable data

    # 1. Get list of players
    for i in range(0, len(players)) :
        players_list.append(str(players[i]).split('" class')[0].split('alt="')[1])

    # 2. Get age, DOB
    for i in range(1, (len(players)*8), 8) :
        dob_list.append(str(multistats[i]).split('"zentriert">')[1].split(" (")[0])
        age_list.append(str(multistats[i]).split(" (")[-1].split(")")[0])

    # 3. Get nationalities
    for i in range(2, (len(players)*8), 8):
        nationality_list.append(str(multistats[i]).split('title="')[1].split('"/>')[0])

    # 4. Get player heights
    for i in range(3, (len(players)*8), 8):
        height_list.append(multistats[i].text)

    # 5. Get foot
    for i in range(4, (len(players)*8), 8):
        foot_list.append(multistats[i].text)

    # 6. Get join dates
    for i in range(5, (len(players)*8), 8):
        join_date_list.append(multistats[i].text)

    # 7. Get previous clubs
    for i in range(6, len(players*8), 8):
        prev_club_list.append(str(multistats[i]).split('" title="')[-1].split('"/')[0])

    # 8. Get contract date
    for i in range(7, (len(players)*8), 8):
        contract_list.append(multistats[i].text)

    # 9. Get positions
    for i in range(0, len(positions)):
        position_list.append(positions[i].text.strip())

    # 10. Get market values
    for i in range(0, len(market_values)):
        market_values_list.append(market_values[i].text)

    # Compile data into a dataframe
    final_df = pd.DataFrame(
        {
            "Player": players_list,
            "Position": position_list,
            "Nationality": nationality_list,
            "Age": age_list,
            "DOB": dob_list,
            "Height": height_list,
            "Foot": foot_list,
            "Previous Club": prev_club_list,
            "Join Date": join_date_list,
            "Contract Expiry": contract_list,
            "Market Value": market_values_list,
        }
    )

    return final_df


def scrape_free_agents(url: str, params: dict) -> dict:
    """Function to scrape free agent data from Transfermarkt

    Args:
        url (str): String representation of URL to scrape from

    Returns:
        dict: Dictionary containing scraped data
    """
    # Get HTML code
    pageSoup = utils.get_website_html(url=url, params=params)

    # Get player names to merge onto other scraped data
    players = pageSoup.find_all("td", {"class": "hauptlink"})[::4]
    clubs = pageSoup.find_all("td", {"class": "hauptlink"})[1::4]
    contract_end = pageSoup.find_all("td", {"class": "hauptlink"})[2::4]
    market_value = pageSoup.find_all("td", {"class": "hauptlink"})[3::4]
    positions = pageSoup.find_all("tr")[10::5]

    nationality = pageSoup.find_all("td", {"class": "zentriert"})[::4]
    age = pageSoup.find_all("td", {"class": "zentriert"})[1::4]
    height = pageSoup.find_all("td", {"class": "zentriert"})[2::4]
    foot = pageSoup.find_all("td", {"class": "zentriert"})[3::4]

    # Combine into dictionary for output
    free_agents = {
        "players": players,
        "clubs": clubs,
        "positions": positions,
        "contract_end": contract_end,
        "market_value": market_value,
        "nationality": nationality,
        "age": age,
        "height": height,
        "foot": foot,
    }

    return free_agents


def convert_free_agents_to_dataframe(scraped_data: dict) -> pd.DataFrame:
    """Function to convert free agent information into dataframe

    Args:
        scraped_data (dict): Dictionary containing information on free agents

    Returns:
        pd.DataFrame
    """
    # Load in scraped data
    players = scraped_data["players"]
    clubs = scraped_data["clubs"]
    contract_end = scraped_data["contract_end"]
    nationality = scraped_data["nationality"]
    age = scraped_data["age"]
    foot = scraped_data["foot"]
    height = scraped_data["height"]
    positions = scraped_data["positions"]
    market_value = scraped_data["market_value"]

    players_list = []
    club_list = []
    age_list = []
    position_list = []
    nationality_list = []
    market_values_list = []
    height_list = []
    foot_list = []
    contract_list = []

    for i in range(len(players)):
        # Get player name
        players_list.append(str(players[i]).split('" title="')[1].split('">')[0])
        # Get club
        club_list.append(str(clubs[i]).split('" title="')[1].split('">')[0])
        # Get positions
        position_list.append(positions[i].text.strip())
        # Get player age
        age_list.append(str(age[i]).split('">')[1].split("<")[0])
        # Get nationality
        nationality_list.append(str(nationality[i]).split('<img alt="')[1].split('" class')[0])
        # Get market value
        market_values_list.append(str(market_value[i]).split('">')[1].split("</")[0])
        # Get player height
        height_list.append(str(height[i]).split('">')[1].split("</")[0])
        # Get strong foot
        foot_list.append(str(foot[i]).split('">')[1].split("</")[0])
        # Get player contract
        contract_list.append(str(contract_end[i]).split('">')[1].split("</")[0])

    # Compile data into a dataframe
    final_df = pd.DataFrame(
        {
            "Player": players_list,
            "Previous Club": club_list,
            "Position": position_list,
            "Nationality": nationality_list,
            "Age": age_list,
            "Height": height_list,
            "Foot": foot_list,
            "Contract Expiry": contract_list,
            "Market Value": market_values_list,
        }
    )
    final_df.insert(1, "Club", "Free Agent")

    return final_df
