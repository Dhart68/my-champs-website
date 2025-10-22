import requests
import pandas as pd
from datetime import datetime, timedelta

# Get the list of games from the scoreboard
scoreboard_url = f"https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
games = requests.get(scoreboard_url).json()["scoreboard"]["games"]

# Construct games of the day dataframe and save it
all_games = pd.DataFrame()

for i in range(len(games)):
    df = pd.DataFrame.from_dict(games[i],orient='columns')

    game_date = df['gameTimeUTC'].iloc[0][:10]
    gameId = df['gameId'].iloc[0]
    gameStatusText = df['gameStatusText'].iloc[0]

    df = df[['homeTeam','awayTeam']][:7]
    df= df.T

    df.insert(loc=0, column='game_date', value=game_date)
    df.insert(loc=1, column='game_id', value=gameId)
    df.insert(loc=2, column='game_status', value=gameStatusText)

    all_games = pd.concat([all_games,df])

all_games.to_csv("all_games_last_day.csv", index=False)

# 3️⃣ Collect boxscores for games played yesterday
rows = []
for g in games:
    game_date = g["gameTimeUTC"].split("T")[0].replace("-", "")
    if game_date == yesterday:
        game_id = g["gameId"]
        box_url = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json"
        box = requests.get(box_url).json()["game"]["players"]
        for p in box:
            p["gameId"] = game_id
            rows.append(p)

# 4️⃣ Create a DataFrame
df = pd.DataFrame(rows)

# 5️⃣ Select key columns
cols = ["gameId", "teamTricode", "personId", "firstName", "familyName",
        "points", "assists", "reboundsTotal", "fieldGoalsMade", "fieldGoalsAttempted"]
df = df[cols]

print(df.head())
df.to_csv("nba_player_stats_last_day.csv", index=False)
