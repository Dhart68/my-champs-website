import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import commonplayerinfo

from get_player_image import get_player_image

# Version amelioree par ChatGPT

def get_players_info(list_of_players_name):
    playerS_name = pd.DataFrame(list_of_players_name, columns=['player_name'])

    picked_players = pd.DataFrame(columns=['player_name','player_id', 'img', 'game_id', 'location', 'video_urls'])
    picked_players_info = []  # collect infos as list, concat once

    for index, player_name in playerS_name.iterrows():
        pname = player_name['player_name']

        # --- find player id ---
        found = players.find_players_by_full_name(pname)
        if not found:   # skip if no match
            print(f"⚠️ No player found for '{pname}'")
            continue
        player_id = found[0]['id']

        picked_players.loc[index, 'player_name'] = pname
        picked_players.loc[index, 'player_id'] = player_id

        # --- get player info ---
        try:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_normalized_dict()
            cinfo = player_info.get('CommonPlayerInfo', [{}])[0]
            hstats = player_info.get('PlayerHeadlineStats', [{}])[0]

            list_items = ['COUNTRY', 'HEIGHT', 'WEIGHT', 'JERSEY', 'POSITION',
                          'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER']
            player_picked_info = pd.DataFrame({key: [cinfo.get(key, None)] for key in list_items})

            player_picked_info['Name'] = pname
            player_picked_info['Birthday'] = cinfo.get('BIRTHDATE', '')[:10] if cinfo.get('BIRTHDATE') else None
            player_picked_info['PTS'] = hstats.get('PTS', None)
            player_picked_info['AST'] = hstats.get('AST', None)
            player_picked_info['REB'] = hstats.get('REB', None)

            picked_players_info.append(player_picked_info)

        except Exception as e:
            print(f"⚠️ Could not fetch info for {pname}: {e}")
            continue

        # --- get image ---
        try:
            picked_players.loc[index, 'img'] = get_player_image(player_id)
        except Exception:
            picked_players.loc[index, 'img'] = None

        # --- get last game info ---
        try:
            game_log = playergamelog.PlayerGameLog(player_id=player_id)
            games_data = game_log.get_data_frames()[0]
            if not games_data.empty:
                last_game = games_data.head(1).copy()
                last_game_id = last_game['Game_ID'].iloc[0]
                picked_players.loc[index, 'game_id'] = last_game_id

                last_game_location = "home" if 'vs' in last_game['MATCHUP'].iloc[0] else "away"
                picked_players.loc[index, 'location'] = last_game_location
            else:
                picked_players.loc[index, 'game_id'] = None
                picked_players.loc[index, 'location'] = None
        except Exception as e:
            print(f"⚠️ Could not fetch games for {pname}: {e}")
            picked_players.loc[index, 'game_id'] = None
            picked_players.loc[index, 'location'] = None

    # --- concat all infos safely ---
    if picked_players_info:
        picked_players_info = pd.concat(picked_players_info, ignore_index=True)
    else:
        picked_players_info = pd.DataFrame(columns=['Name', 'Birthday', 'PTS', 'AST', 'REB',
                                                    'COUNTRY', 'HEIGHT', 'WEIGHT', 'JERSEY',
                                                    'POSITION', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER'])

    return [picked_players, picked_players_info]
