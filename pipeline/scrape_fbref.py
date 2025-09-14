###################
# Import Packages #
###################

import sys
import pandas as pd
from time import sleep
from random import randint
from tqdm import tqdm

sys.path.insert(1, "/Users/jonahyallop/Documents/Colchester United")

import functions.fbref_scraping_functions as fbref

#######################
# Get Desired Leagues #
#######################

# Get stats to keep for each league
general_stats = ["player", "team", "position", "nationality", "age", "birth_year", "games", "games_starts", "minutes", "goals", "assists", "pens_made", "pens_att", "cards_yellow", "cards_red"]

leagues_to_scrape = {
    "National-League": {"num": 34, "stats": general_stats},
    "Premier-League-2": {"num": 852, "stats": general_stats},
    "Scottish-Premiership": {"num": 40, "stats": general_stats},
    "Scottish-Championship": {"num": 72, "stats": general_stats},
}

#########################
# Scrape Outfield Stats #
#########################

#Go to the 'Standard stats' page of the league
#For the National League 2023/24, the link is this: https://fbref.com/en/comps/34/stats/National-League-Stats
#Remove the 'stats', and pass the first and third part of the link as parameters like below

temp_league_dfs = []

for league_name, league_info in tqdm(leagues_to_scrape.items()):

    # Scrape URL
    league_player_data = fbref.get_outfield_data(
        top=f"https://fbref.com/en/comps/{league_info['num']}/",
        end=f"/{league_name}-Stats",
        stats=league_info["stats"]
    )
    # Add league column
    league_player_data.insert(1, "League", league_name.replace("-", " "))
    # Save results to list
    temp_league_dfs.append(league_player_data)

    sleep(randint(2, 10))

# Aggregate league dataframes into one dataframe
league_df = pd.concat(temp_league_dfs)
league_df.reset_index(drop=True, inplace=True)

print(league_df)

# Save results to excel
with pd.ExcelWriter(f'outputs/Fbref_Player_Database.xlsx') as writer:
    league_df.to_excel(writer, sheet_name="Full Player Database", index=False)
