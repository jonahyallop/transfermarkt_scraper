###################
# Import Packages #
###################

from tqdm import tqdm
import yaml
import sys
import pandas as pd
from time import sleep
from random import randint
from datetime import datetime

sys.path.insert(1, "/Users/jonahyallop/Documents/04. Football Data/01. Colchester United")

import functions.transfermarkt_scraping_functions as tfmrkt

################
# Load Configs #
################

with open("configs/transfermarkt.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

# Get current date for file naming
ts = datetime.today().strftime('%Y%m%d')

###############
# Scrape Data #
###############

temp_club_dfs = []

# Get season
season = config["season"]

for league in tqdm(config["club_dict"]):

    for club, num in tqdm(config["club_dict"][league].items()):

        # 1. Scrape general player data

        url = f"https://www.transfermarkt.co.uk/{club}/kader/verein/{num}/saison_id/{season}/plus/1"
        # Scrape URL
        temp_player_data = tfmrkt.scrape_player_data(url=url)
        # Convert data into pandas dataframe
        club_player_data = tfmrkt.convert_player_data_to_dataframe(scraped_data=temp_player_data)
        # Add club column
        club_player_data.insert(1, "League", league.replace("_", " ").title())
        club_player_data.insert(2, "Club", club.replace("-", " ").title())

        # 2. Scrape agent data

        agent_url = f"https://www.transfermarkt.co.uk/{club}/berateruebersicht/verein/{num}"
        # Scrape URL
        temp_agent_data = tfmrkt.scrape_agent_data(url=agent_url)
        # Convert data into pandas dataframe
        club_agent_data = tfmrkt.convert_agent_data_to_dataframe(scraped_data=temp_agent_data)

        # 3. Merge player and agent data

        club_player_data = club_player_data.merge(club_agent_data, on="Player", how="left")
        # Save results to list
        temp_club_dfs.append(club_player_data)

        sleep(randint(2, 10))

######################
# Scrape Free Agents #
######################

free_agent_base_url = "https://www.transfermarkt.co.uk/transfers/vertragslosespieler/statistik"
params = {
    "ausrichtung": "",
    "spielerposition_id": "0",
    "land_id": "",
    "wettbewerb_id": "alle",
    "seit": "0",
    "altersklasse": "",
    "plus": "1",
}

free_agents = []

for page_num in range(1, config["free_agent_pages"] + 1):

    params.update({"page": page_num})
    # Scrape URL
    raw_free_agent_data = tfmrkt.scrape_free_agents(url=free_agent_base_url, params=params)
    # Convert data into pandas dataframe
    temp_free_agents = tfmrkt.convert_free_agents_to_dataframe(scraped_data=raw_free_agent_data)
    free_agents.append(temp_free_agents)

#################
# Clean Outputs #
#################

# Aggregate club dataframes into one dataframe at league level
league_df = pd.concat(temp_club_dfs)
league_df.reset_index(drop=True, inplace=True)

# Merge free agents onto output dataframe
league_df = pd.concat([league_df] + free_agents)

# Save results to excel
with pd.ExcelWriter(f'outputs/{ts}_Transfermarkt_Player_Database.xlsx') as writer:
    league_df.to_excel(writer, sheet_name="Full Player Database", index=False)
