from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd

def get_players_day():

    # Example: stats for the most recent day (LastNGames=1)
    data = leaguedashplayerstats.LeagueDashPlayerStats(
        last_n_games=1,
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Base',
        season='2025-26',  # or the current season
        season_type_all_star='Regular Season'
    )

    df = data.get_data_frames()[0]
    print(df.head())

    # Save to CSV if needed

    #df.to_csv('backup_data/nba_player_stats_today.csv', index=False)

    df.to_csv('data/nba_player_stats_today.csv', index=False)
