# Function to get the URL of the video of the player picked
# Fetch all the video event, the selection regarding FGM, blocks etc will be done afterward


import requests
import pandas as pd

from nba_api.stats.endpoints import playbyplayv2


def get_mp4_urls_v2(player_id, game_id):
    '''
    Function to get the URL of the video of the player picked, need the game_id and the player_id
    get the list of URLs of the video part of interest, could be improve with the EVENTMSGACTIONTYPE
    to select only some type of actions
    '''

    # get all the pbp of the game
    pbp = playbyplayv2.PlayByPlayV2(game_id)
    pbp = pbp.get_data_frames()[0]


    # select rows in pbp_player containing Name of the player
    # I choose to select only the 2 players involved to limit the number of actions
    pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id)) | (pbp['PLAYER2_ID'] == int(player_id)) ].copy()

    # event num list with video flag
    event_id_list = pbp_player[pbp_player['VIDEO_AVAILABLE_FLAG']==1]['EVENTNUM'].tolist()
    event_id_list = list(set(event_id_list))

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
    pbp_player['video'] = None
    pbp_player['desc'] = None

    for event_id in event_id_list:
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
            mask = pbp_player['EVENTNUM'] == event_id
            pbp_player.loc[mask, 'video'] = video_url
            pbp_player.loc[mask, 'desc'] = desc

    video_event_df = pbp_player.copy()

    return [video_event_df]
