# update_nba_data.py
import pandas as pd
from datetime import datetime


from get_best_players_day import get_best_players_day
from get_players_info_v2 import get_players_info_v2

### Add superstars
#my_champs_superstars = ["Jokic, Nikola ","Doncic, Luka", "Durant, Kevin", "Curry, Stephen", "Sengun, Alperen"]

### French players
#my_champs_french = ["Wembanyama, Victor", "Gobert, Rudy", "Yabusele, Guerschon", "Sarr, Alex", "Coulibaly, Bilal", "Beringer, Joan"]

#champs_list = my_champs_superstars + my_champs_french

best_players_day = get_best_players_day(number = 1)

playerS_name=best_players_day['Formatted_name'].to_list()

print(playerS_name)

[picked_players, picked_players_info, picked_players_video_event_df] = get_players_info_v2(playerS_name)


# Get today's date in a clean format (e.g. 2025-10-09)
today = datetime.today().strftime("%Y-%m-%d")

# --- 3. Save to local files with date in name ---
output_file_1 = f"data/best_players_day_{today}.csv"
best_players_day.to_csv(output_file_1, index=False)

output_file_2 = f"data/picked_players_{today}.csv"
picked_players.to_csv(output_file_2, index=False)

output_file_3 = f"data/picked_players_info_{today}.csv"
picked_players_info.to_csv(output_file_3, index=False)

output_file_4 = f"data/picked_players_video_event_df_{today}.csv"
picked_players_video_event_df.to_csv(output_file_4, index=False)


print(f"✅ Data updated")
