###################
# Import Packages #
###################

import yaml
import sys
import re
import os
import pandas as pd
from tqdm import tqdm
from time import sleep
from random import randint
from datetime import datetime

sys.path.insert(1, os.getcwd())

import functions.other_scraping_functions as scrape

################
# Load Configs #
################

with open("configs/tier_7.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

# Get current date for file naming
ts = datetime.today().strftime('%Y%m%d')

###############
# Scrape Data #
###############

temp_club_dfs = []

for league in tqdm(config["club_dict"]):

    for club, num in tqdm(config["club_dict"][league].items()):
 
        # 1. Scrape general player data

        url = f"https://southern-football-league.co.uk/players/{club}/2023/2024/{num}/P/Position/"
        # Scrape URL
        temp_player_data = scrape.scrape_southern_football_league(url=url)
    
        # Convert data into pandas dataframe
        club_player_data = scrape.convert_southern_league_data_to_frame(scraped_data=temp_player_data)

        # Add league column
        club_player_data.insert(1, "League", league.replace("_", " ").title())
        # Add spaces between club names for output
        club = " ".join(re.findall('[A-Z][^A-Z]*', club))
        # Add club column
        club_player_data.insert(2, "Club", club)

        # Save results to list
        temp_club_dfs.append(club_player_data)

        sleep(randint(2, 10))

#################
# Clean Outputs #
#################

# Aggregate club dataframes into one dataframe at league level
league_df = pd.concat(temp_club_dfs)
league_df.reset_index(drop=True, inplace=True)

# Save results to excel
with pd.ExcelWriter(f'outputs/{ts}_Tier7_Player_Database.xlsx') as writer:
    league_df.to_excel(writer, sheet_name="Tier 7 Player Database", index=False)
