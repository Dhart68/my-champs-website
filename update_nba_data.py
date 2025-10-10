# update_nba_data.py
import pandas as pd
from datetime import date


from get_best_players_day import get_best_players_day
from get_players_info import get_players_info


best_players_day = get_best_players_day()

playerS_name=best_players_day['Formatted_name'].to_list()

[picked_players, picked_players_info, picked_players_video_event_df] = get_players_info(playerS_name)


# --- 3. Save to local file
output_file_1 = f"data/Four_best_day.csv"
best_players_day.to_csv(output_file_1, index=False)

output_file_2 = f"data/picked_players.csv"
picked_players.to_csv(output_file_2, index=False)

output_file_3 = f"data/picked_players_info.csv"
picked_players_info.to_csv(output_file_3, index=False)

output_file_4 = f"data/picked_players_video_event_df.csv"
picked_players_video_event_df.to_csv(output_file_4, index=False)


print(f"✅ Data updated")
