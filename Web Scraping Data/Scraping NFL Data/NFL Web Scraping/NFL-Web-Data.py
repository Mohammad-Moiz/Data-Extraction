import numpy as np
import pandas as pd
import random
import time


seasons = [str(season) for season in range(2010, 2023)]
print(f"number of seasons = {len(seasons)}")

team_abbrs = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx", "clt", "jax", "kan", "sdg", "ram", "rai", "mia", "min", "nwe", "nor", "nyg", "nyj", "phi", "pit", "sea", "sfo", "tam", "oti", "was"]
print(f"number of teams = {len(team_abbrs)}")

nfl_df = pd.DataFrame()

for season in seasons:
    for team in team_abbrs:
        url = "" + team + "/" + season + "gamelog/"
        print(url)

        try:
            off_df = pd.read_html(url, attrs={"id": "gamelog" + season}, header=1)[0]

            def_df = pd.read_html(url, attrs={"id": "gamelog_opp" + season}, header=1)[0]

            team_df = pd.concat([off_df, def_df], axis=1)

            team_df.insert(loc=0, column="Season", value=season)
            team_df.insert(loc=1, column="Team", value=team.upper())

            nf1_df = pd.concat([nfl_df, team_df], ignore_index=True)

        except Exception as e:
            print(f"Error accessing URL: {url}")
            print(e)

        time.sleep(random.randint(4, 5))

    print(nf1_df)

nf1_df.to_csv("nf1_gamelogs_2010-2022.csv",index=False)

print(nf1_df)


