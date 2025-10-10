# Function to get the URL of the video of the player picked

import requests
import pandas as pd

from nba_api.stats.endpoints import playbyplayv2


def get_mp4_urls(player_id, game_id, game_location, option):
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

    # option to choose what to select, many possibilities
    if option == 'Full': # Full option = all the sequences
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id)) |
                         (pbp['PLAYER2_ID'] == int(player_id)) ]

    if option == 'Best':
        # select video_event_pd where desc does not contain remove terms
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id)) |
                         (pbp['PLAYER2_ID'] == int(player_id)) ]

        Remove_terms = ['REBOUND', 'MISS', 'Free Throw']

        if game_location == 'away':
            pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(Remove_terms), na=False) == False) ]
        if game_location == 'home':
            pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(Remove_terms), na=False) == False) ]

    # Should be other options...
    if option == 'FGA':
        # select video_event_pd where desc does not contain remove terms
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]

        selected_terms = ['PTS', '3PT', 'Shot']

        if game_location == 'away':
            pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]
        if game_location == 'home':
            pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]

    if option == 'FGM':
        # select video_event_pd where desc does not contain remove terms
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]

        selected_terms = ['PTS']

        if game_location == 'away':
            pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]
        if game_location == 'home':
            pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]

    if option == 'AST':
        # select video_event_pd where desc does not contain remove terms
        pbp_player = pbp[(pbp['PLAYER2_ID'] == int(player_id))]

        selected_terms = ['AST']

        if game_location == 'away':
            pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]
        if game_location == 'home':
            pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]

    if option == 'REB':
        # select video_event_pd where desc does not contain remove terms
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]

        selected_terms = ['REBOUND']

        if game_location == 'away':
            pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]
        if game_location == 'home':
            pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]

    if option == 'BLOCK':
        # select video_event_pd where desc does not contain remove terms
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id)) |
                         (pbp['PLAYER2_ID'] == int(player_id)) |
                         (pbp['PLAYER3_ID'] == int(player_id)) ]

        selected_terms = ['BLOCK']

        if game_location == 'away':
            pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]
        if game_location == 'home':
            pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]

    # event num list with video flag
    event_id_list = pbp_player[pbp_player['VIDEO_AVAILABLE_FLAG']==1]['EVENTNUM'].tolist()

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

    video_event_list = []

    for event_id in event_id_list:
        url = 'https://stats.nba.com/stats/videoeventsasset?GameEventID={}&GameID={}'.format(event_id, game_id)
        r = requests.get(url, headers=headers)
        json = r.json()
        video_urls = json['resultSets']['Meta']['videoUrls']
        playlist = json['resultSets']['playlist']
        video_event_list.append({'video': video_urls[0]['lurl'], 'desc': playlist[0]['dsc']})

    video_event_df = pd.DataFrame(video_event_list)
    video_event_df['player_id'] = player_id
    video_event_df['game_id'] = game_id
    video_event_df['game_location'] = game_location
    video_event_df['option'] = option

    return video_event_df
