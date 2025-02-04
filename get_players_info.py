import pandas as pd

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import commonplayerinfo


from get_player_image import get_player_image


def get_players_info(list_of_players_name):
    playerS_name = pd.DataFrame(list_of_players_name, columns=['player_name'])

    picked_players = pd.DataFrame(columns=['player_name','player_id', 'img', 'game_id', 'location', 'video_urls'])
    picked_players_info = pd.DataFrame(columns=['Name', 'Birthday', 'PTS', 'AST', 'REB', 'COUNTRY', 'HEIGHT', 'WEIGHT', 'JERSEY', 'POSITION', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER'])

    for index, player_name in playerS_name.iterrows():

    # player_id and name:
        picked_players.loc[index,'player_name'] = player_name['player_name']

    # get players id
        player_id = players.find_players_by_full_name(player_name['player_name'])[0]['id']
        picked_players.loc[index,'player_id']=player_id

    # get players info
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        player_info = player_info.get_normalized_dict()

        list_items = ['COUNTRY', 'HEIGHT', 'WEIGHT', 'JERSEY', 'POSITION', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER']
        player_picked_info = pd.DataFrame({key:[player_info['CommonPlayerInfo'][0][key]] for key in list_items})

        player_picked_info ['Name'] = player_name['player_name']
        player_picked_info ['Birthday'] = player_info['CommonPlayerInfo'][0]['BIRTHDATE'][:10]
        player_picked_info ['PTS'] = player_info['PlayerHeadlineStats'][0]['PTS']
        player_picked_info ['AST'] = player_info['PlayerHeadlineStats'][0]['AST']
        player_picked_info ['REB'] = player_info['PlayerHeadlineStats'][0]['REB']

        picked_players_info = pd.concat([picked_players_info, player_picked_info], ignore_index=True)

    # get the images and info of a player
        picked_players.loc[index,'img'] = get_player_image(player_id)

    # Find the game id and game location
        #Get the player's game logs for the current season
        game_log = playergamelog.PlayerGameLog(player_id=player_id)  # Adjust the season if needed
        games_data = game_log.get_data_frames()[0]  # Retrieve the DataFrame

        # Reorder the columns and add location column
        last_game = games_data.head(1).copy()
        last_game_id=last_game['Game_ID'][0]

        picked_players.loc[index,'game_id'] = last_game_id

        last_game_location = last_game['MATCHUP'].apply(lambda x: "home" if 'vs' in x else "away")[0]

        picked_players.loc[index,'location']  = last_game_location

    # list of the last video with get_mp4_urls()
        #picked_players.loc[index,'video_urls'] = [get_mp4_urls(player_id, last_game_id, last_game_location, 'Full').to_dict()]

    return [picked_players, picked_players_info]
