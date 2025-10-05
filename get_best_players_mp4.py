### Function to get all the mp4 url of the 4 bests performer of the day with the "Best option"
# V2 load them on a container

import pandas as pd

from player_last_stats import player_last_stats
from get_mp4_urls import get_mp4_urls


def get_best_players_mp4(playerS_name):

    df_best_players_mp4 = pd.DataFrame(columns=['Player', 'Game_ID', 'video_urls', 'video_urls_js'])
    df_best_players_mp4['Player'] = playerS_name

    for index, player in df_best_players_mp4['Player'].iterrows():
        # get last gane info for each player
        [last_n_games, player_id] = player_last_stats(player, 1)

        video_event_df = get_mp4_urls(player_id, last_n_games['Game_ID'], last_n_games['location'], 'Best')
        video_urls = video_event_df['video'].to_list()

        video_urls_js = ','.join(f'"{url}"' for url in video_urls)

        df_best_players_mp4.loc[index, ['Player', 'Game_ID', 'video_urls', 'video_urls_js']] = [player, last_n_games['Game_ID'], video_urls, video_urls_js]

    return df_best_players_mp4 # load all URLS and store them in a container?
