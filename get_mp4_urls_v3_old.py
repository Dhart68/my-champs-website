# Fetch all the video event for one game, the selection regarding FGM, blocks etc will be done afterward

# pbp is not available just after the game, i have to find another way


import requests
import pandas as pd
from datetime import datetime

from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.endpoints import ScheduleLeagueV2

def daily_schedule():

    ## trouver le temps du moment la veille des match
    today = datetime.today().strftime("%Y-%m-%d")

    ## chercher dans le schedule les match prevu et trouver les heures des matchs
    schedule = ScheduleLeagueV2()
    schedule_nba = schedule.get_data_frames()[0]

    schedule_day = schedule_nba[schedule_nba['gameDateEst'].str[:10] == today]

    select_columns = ['gameDate', 'gameId','gameStatus','gameStatusText',
                  'gameDateTimeUTC','homeTeam_teamName','homeTeam_score',
                  'awayTeam_teamName','awayTeam_score']

    df = schedule_day[select_columns]
    # Add 3h to estimate end of the game
    df.insert(5, 'estimate_end_time_UTC', pd.to_datetime(df['gameDateTimeUTC'], utc=True) + pd.Timedelta(hours=3))

    daily_schedule = df

    # store info in data folder
    output_file = f'data/daily_schedule_{today}.csv'
    daily_schedule.to_csv(output_file, index=False)


    return daily_schedule



def get_mp4_urls_v3(game_id):
    '''
    Function to get the URL of the video of the player picked, need the game_id and the player_id
    get the list of URLs of the video part of interest, could be improve with the EVENTMSGACTIONTYPE
    to select only some type of actions
    '''

    # get all the pbp of the game
    pbp = playbyplayv2.PlayByPlayV2(game_id)
    pbp = pbp.get_data_frames()[0]

    print(pbp.head())

    # event num list with video flag
    event_id_list = pbp[pbp['VIDEO_AVAILABLE_FLAG']==1]['EVENTNUM'].tolist()
    event_id_list = list(set(event_id_list))
    print(event_id_list[:5])

    # for loop to get all the video url
    headers = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://stats.nba.com/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    # Initialize the columns in pbp_player
    pbp['video'] = None
    pbp['desc'] = None

    print(game_id)

    for event_id in event_id_list:
        print(event_id)
        url = f'https://stats.nba.com/stats/videoeventsasset?GameEventID={event_id}&GameID={game_id}'
        r = requests.get(url, headers=headers)
        json_data = r.json()
        video_urls = json_data['resultSets']['Meta']['videoUrls']
        playlist = json_data['resultSets']['playlist']

        # Safely get first URL and description
        if video_urls and playlist:
            video_url = video_urls[0].get('lurl')
            desc = playlist[0].get('dsc')

            # Assign to pbp_player using .loc
            mask = pbp['EVENTNUM'] == event_id
            pbp.loc[mask, 'video'] = video_url
            pbp.loc[mask, 'desc'] = desc

    video_event_df = pbp.copy()

    return video_event_df


#### Test

#game_id_1 = str(daily_schedule()['gameId'].iloc[0])
game_id_1 ='0022500001'
print(game_id_1)
pbp_video = get_mp4_urls_v3(game_id_1)

print(pbp_video.head())

output_file = f"data/game_id_1.csv"
pbp_video.to_csv(output_file, index=False)
