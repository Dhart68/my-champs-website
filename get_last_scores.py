### Function to get the last scores of the day by scraping the page
# https://cdn.nba.com/static/json/staticData/EliasGameStats/00/day_scores.txt'

# to update with
 # https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json

import requests
import pandas as pd

def get_last_scores():
    # Fetch the content
    url = 'https://cdn.nba.com/static/json/staticData/EliasGameStats/00/day_scores.txt'

    response = requests.get(url)

    # Preprocess the data: split into lines and skip unnecessary header lines
    games_date = response.text.splitlines()[2]
    games_lines = response.text.splitlines()[6:]  # Skip the first header line

    scores = []
    lines = [line for line in games_lines if line.strip()] # remove empty lines
    number_of_games = int(len(lines)/2)

    scores_df = pd.DataFrame()
    white_col = pd.DataFrame({"white": ['','']})

    # Iterate through lines and parse
    for i in range(0, len(lines)-1,2):  # Each game spans two lines
        # Parse team 1
        team1_name = lines[i][:14].strip()
        team1_data = lines[i][14:].split(maxsplit=16)
        team1 = {
            "Team": team1_name,
            "Total": int(team1_data[0]),
            }

        # Parse team 2
        team2_name = lines[i + 1][:14].strip()
        team2_data = lines[i + 1][14:].split(maxsplit=16)
        team2 = {
            "Team": team2_name,
            "Total": int(team2_data[0]),
            }
        #text horizonatl for banner
        scores.append(f'{team1_name} : {team1["Total"]} - {team2["Total"]} : {team2_name}')

        # DataFrame for 2 lines scores
        scores_df = pd.concat([scores_df, pd.DataFrame([team1, team2]), white_col], axis = 1)


    return games_date, number_of_games, scores, scores_df
