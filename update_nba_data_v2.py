# update_nba_data.py
import pandas as pd
from datetime import datetime
import time

from get_best_players_day import get_best_players_day
from get_players_info_v2 import get_players_info_v2

### Add superstars
my_champs_superstars = [
    "Jokic, Nikola",
    "Gilgeous-Alexander, Shai",
    "Doncic, Luka",
    "James, LeBron",
    "Curry, Stephen",
    "Durant, Kevin",
    "Antetokounmpo, Giannis",
    "Edwards, Anthony",
    "Embiid, Joel",
    "Tatum, Jayson",
    "Davis, Anthony",
    "Booker, Devin",
    "Morant, Ja",
    "Butler, Jimmy",
    "Lillard, Damian",
    "Wembanyama, Victor",
    "Mitchell, Donovan",
    "George, Paul",
    "Towns, Karl-Anthony",
    "Irving, Kyrie",
    "Leonard, Kawhi",
    "Harden, James"
]
### French players
my_champs_french = [
    "Wembanyama, Victor",
    "Gobert, Rudy",
    "Batum, Nicolas",
    "Yabusele, Guerschon",
    "Coulibaly, Bilal",
    "Dieng, Ousmane",
    "Luwawu-Cabarrot, Timothé",
    "Sarr, Olivier",
    "Risacher, Zaccharie",
    "Sarr, Alex",
    "Sarr, Olivier",
    "Essengue, Noa",
    "Rupert, Rayan",
    "Cissoko, Sidy",
    "Beringer, Joan",
    "Diawara, Mohamed",
    "Dadiet, Pacome",
    "Raynaud, Maxime",
    "Traoré, Nolan",
    "Penda, Noah"

]

international_stars = [
    "Sengun, Alperen",
    "Yang, Hansen",
    "Siakam, Pascal",
    "Markkanen, Lauri",
    "Porziņģis, Kristaps ",
    "Schröder, Dennis",
    "Wagner,Franz",
    "Sabonis, Domantas"
    ]

rookies_2025 = [
    "Flagg, Cooper",
    "Harper, Dylan",
    "Edgecombe, V. J.",
    "Knueppel, Kon",
    "Bailey, Ace"
    ]

champs_list = my_champs_superstars + my_champs_french + international_stars + rookies_2025

start_time = time.time()

best_players_day = get_best_players_day(number = 5, champs_list=champs_list)

playerS_name=best_players_day['Formatted_name'].to_list()

print(playerS_name)
print(time.ctime())

[picked_players, picked_players_info, picked_players_video_event_df] = get_players_info_v2(playerS_name)

end_time = time.time() # or time.perf_counter()
elapsed_time = end_time - start_time
print(f"Execution took: {elapsed_time:.6f} seconds")

# Get today's date in a clean format (e.g. 2025-10-09)
today = datetime.today().strftime("%Y-%m-%d")

# --- 3. Save to backup local files with date in name ---
output_file_11 = f"backup_data/best_players_day_{today}.csv"
best_players_day.to_csv(output_file_11, index=False)

output_file_12 = f"backup_data/picked_players_{today}.csv"
picked_players.to_csv(output_file_12, index=False)

output_file_13 = f"backup_data/picked_players_info_{today}.csv"
picked_players_info.to_csv(output_file_13, index=False)

output_file_14 = f"backup_data/picked_players_video_event_df_{today}.csv"
picked_players_video_event_df.to_csv(output_file_14, index=False)

# --- 4. Save to local files for udpdate files of the app ---
output_file_1 = f"data/best_players_day.csv"
best_players_day.to_csv(output_file_1, index=False)

output_file_2 = f"data/picked_players.csv"
picked_players.to_csv(output_file_2, index=False)

output_file_3 = f"data/picked_players_info.csv"
picked_players_info.to_csv(output_file_3, index=False)

output_file_4 = f"data/picked_players_video_event_df.csv"
picked_players_video_event_df.to_csv(output_file_4, index=False)

print(f"✅ Data updated")
