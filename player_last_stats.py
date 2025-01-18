### Function do get info an NBA player

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

def player_last_stats(player_picked = 'victor wembanyama'):

    # Get info about the player
    player_id = players.find_players_by_full_name(player_picked)[0]['id']

    #Get the player's game logs for the current season
    game_log = playergamelog.PlayerGameLog(player_id=player_id)  # Adjust the season if needed
    games_data = game_log.get_data_frames()[0]  # Retrieve the DataFrame

    # Reorder the columns and add location column
    last_3_games = games_data.head(3).copy()
    last_3_games['location'] = last_3_games['MATCHUP'].apply(lambda x: "home" if 'vs' in x else "away")

    # get the score of the games

    # Reorder the columns
    last_3_games = last_3_games[['GAME_DATE','Game_ID', 'MATCHUP','WL','location', 'MIN','PTS', 'REB',
                               'AST', 'STL', 'BLK', 'FGA', 'FG_PCT', 'FG3A',
                               'FG3_PCT', 'FTA','FT_PCT', 'OREB', 'DREB', 'TOV', 'PF', 'PLUS_MINUS']]

    last_3_games.reset_index(drop=True, inplace=True)

    return [last_3_games, player_id]
