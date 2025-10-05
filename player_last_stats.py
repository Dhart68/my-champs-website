from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, BoxScoreSummaryV2
import pandas as pd

# Version pimped by Chat GPT to work even it not in the regular season

def player_last_stats(player_picked, n_games=5):
    # Find player id
    found = players.find_players_by_full_name(player_picked)
    if not found:
        raise ValueError(f"Player '{player_picked}' not found")

    player_id = found[0]['id']

    # Season types to try (order = priority)
    season_types = [
        "Regular Season",
        "Playoffs",
        "In Season Tournament",
        "Pre Season",
        "All Star"
    ]

    games_data = pd.DataFrame()

    # Try each season type until we find data
    for s_type in season_types:
        try:
            game_log = playergamelog.PlayerGameLog(player_id=player_id, season_type_all_star=s_type)
            df = game_log.get_data_frames()[0]
            if not df.empty:
                games_data = df
                active_season_type = s_type
                break
        except Exception:
            continue

    if games_data.empty:
        print(f"⚠️ No games found for {player_picked}")
        return [pd.DataFrame(), player_id]

    # Process last n games
    last_n_games = games_data.head(n_games).copy()
    last_n_games['location'] = last_n_games['MATCHUP'].apply(lambda x: "home" if 'vs' in x else "away")
    last_n_games['score'] = 'not found'

    # Add score from box score
    for index, row in last_n_games.iterrows():
        game_id = row['Game_ID']
        try:
            box_score = BoxScoreSummaryV2(game_id=game_id).get_normalized_dict()
            score_0 = box_score['LineScore'][0]['PTS']
            score_1 = box_score['LineScore'][1]['PTS']
            last_n_games.loc[index, 'score'] = f'{score_0}-{score_1}'
        except Exception:
            pass

    # Reorder columns
    cols = ['GAME_DATE', 'Game_ID', 'MATCHUP', 'location', 'score', 'WL', 'MIN', 'PTS', 'REB',
            'AST', 'STL', 'BLK', 'FGA', 'FG_PCT', 'FG3A', 'FG3_PCT', 'FTA',
            'FT_PCT', 'OREB', 'DREB', 'TOV', 'PF', 'PLUS_MINUS']
    last_n_games = last_n_games[[c for c in cols if c in last_n_games.columns]]

    last_n_games.reset_index(drop=True, inplace=True)

    print(f"✅ Found games in {active_season_type}")

    return [last_n_games, player_id]
