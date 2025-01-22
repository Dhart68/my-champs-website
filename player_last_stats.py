### Function do get info an NBA player

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import BoxScoreSummaryV2

def player_last_stats(player_picked):

    # Get info about the player
    player_id = players.find_players_by_full_name(player_picked)[0]['id']

    #Get the player's game logs for the current season
    game_log = playergamelog.PlayerGameLog(player_id=player_id)  # Adjust the season if needed
    games_data = game_log.get_data_frames()[0]  # Retrieve the DataFrame

    # Reorder the columns and add location column
    last_5_games = games_data.head(5).copy()
    last_5_games['location'] = last_5_games['MATCHUP'].apply(lambda x: "home" if 'vs' in x else "away")

    # get the score of the games
    last_5_games['score']='not found'

    for index, row in last_5_games.iterrows():
        game_id = row['Game_ID']
        box_score = BoxScoreSummaryV2(game_id=game_id)
        # Extract game data
        game_box = box_score.get_normalized_dict()

        score_0 = game_box['LineScore'][0]['PTS'] # position of the linescore is not link with the name of the team or the location of the game
        score_1 = game_box['LineScore'][1]['PTS'] # to make it better needs couple of test (if) it will take to much time, i give up for now

        last_5_games.loc[index, 'score'] = f'{score_0}-{score_1}'


    # Reorder the columns
    last_5_games = last_5_games[['GAME_DATE', 'Game_ID', 'MATCHUP', 'location', 'score', 'WL', 'MIN', 'PTS', 'REB',
                               'AST', 'STL', 'BLK', 'FGA', 'FG_PCT', 'FG3A',
                               'FG3_PCT', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'TOV', 'PF', 'PLUS_MINUS']]

    last_5_games.reset_index(drop=True, inplace=True)

    return [last_5_games, player_id]
