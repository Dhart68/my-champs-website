### Here is the library of all the function DH created for my-champ-website

''' List of functions :
    - get_last_scores()
    - get_best_players_day()
    - get_player_image(player_id)
    - [picked_players, picked_players_info] = get_players_info(playerS_name)
    - [last_n_games, player_id] = player_last_stats(player_picked, 5)
    - video_event_df = get_mp4_urls(player_id, game_id, game_location, option)
    - get_best_players_mp4(playerS_name)


'''
### imports
import pandas as pd
import requests
from bs4 import BeautifulSoup

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import BoxScoreSummaryV2
from nba_api.stats.endpoints import playbyplayv2

### Function to get the last scores of the day by scraping the page
# https://cdn.nba.com/static/json/staticData/EliasGameStats/00/day_scores.txt'

def get_last_scores():
    # Fetch the content
    url = 'https://cdn.nba.com/static/json/staticData/EliasGameStats/00/day_scores.txt'
    response = requests.get(url)

    # Preprocess the data: split into lines and skip unnecessary header lines
    games_date = response.text.splitlines()[2]
    games_lines = response.text.splitlines()[6:]  # Skip the first header line

    scores = []
    lines = [line for line in games_lines if line.strip()] # remove empty lines
    number_of_games = int(len(lines)/2)

    scores_df = pd.DataFrame()
    white_col = pd.DataFrame({"white": ['','']})

    # Iterate through lines and parse
    for i in range(0, len(lines)-1,2):  # Each game spans two lines
        # Parse team 1
        team1_name = lines[i][:14].strip()
        team1_data = lines[i][14:].split(maxsplit=16)
        team1 = {
            "Team": team1_name,
            "Total": int(team1_data[0]),
            }

        # Parse team 2
        team2_name = lines[i + 1][:14].strip()
        team2_data = lines[i + 1][14:].split(maxsplit=16)
        team2 = {
            "Team": team2_name,
            "Total": int(team2_data[0]),
            }
        #text horizonatl for banner
        scores.append(f'{team1_name} : {team1["Total"]} - {team2["Total"]} : {team2_name}')

        # DataFrame for 2 lines scores
        scores_df = pd.concat([scores_df, pd.DataFrame([team1, team2]), white_col], axis = 1)


    return games_date, number_of_games, scores, scores_df


### Function to get the last stats of the day by scraping the page
# 'https://cdn.nba.com/static/json/staticData/EliasGameStats/00/all_players_day.txt'

def get_best_players_day():
    # Download the text file
    url = 'https://cdn.nba.com/static/json/staticData/EliasGameStats/00/all_players_day.txt'
    response = requests.get(url)

    # Convert text to list of lines, skipping the first 5 header lines
    lines = response.text.splitlines()[5:]

    # header
    header_line = lines[0] #
    Col_names = header_line.split()

    ## For name longer than 20 char I have to add this lines of code to calculate the widths of each column (pd.read_fwf limit to 20 chars)
    # Find the starting position of each column name
    start_positions = {}
    current_position = 0
    for col_name in Col_names:
      start_positions[col_name] = header_line.find(col_name, current_position)
      current_position = start_positions[col_name] + len(col_name)

    list_start = list(start_positions.values())

    widths_list = []
    for i in range(len(list_start)-1):
      widths_list.append((list_start[i+1])-(list_start[i]))

    widths_list.append(3)

    # data
    data = response.text.splitlines()[6:]
    # Read the data using pandas with fixed-width format
    df = pd.read_fwf(pd.io.common.StringIO("\n".join(data)), names = Col_names, widths = widths_list) # specify the size of the col

    df['MyScore'] = df['PTS']+df['AST']+df['TRB']
    Four_best_day = df.sort_values(by='MyScore', ascending=False).head(4)

    Four_best_day['Formatted_name'] = 'name'

    # loop to reorder name properly when ther is a Jr in the name
    for index, row in Four_best_day.iterrows():
      name = row['NAME']

      if 'Jr.' in row['NAME']:
        nm_list = name.replace('Jr.', '').rstrip().split(", ")[::-1]
        nm_list.append('Jr.')
        Four_best_day.loc[index, 'Formatted_name'] =" ".join(nm_list).lower()

      else:
        Four_best_day.loc[index, 'Formatted_name'] = " ".join(row['NAME'].split(", ")[::-1]).lower()


    return Four_best_day


# This function will get a player's headshot image


def get_player_image(player_id):
    # The image will be retrieved from this URL
    url = f'https://www.nba.com/stats/player/{player_id}'

    # Make an HTTP GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the player image tag using the appropriate class
    img_tag = soup.find('img', {'class': 'PlayerImage_image__wH_YX PlayerSummary_playerImage__sysif'})

    # Extract and return the src attribute if the img tag is found
    if img_tag and 'src' in img_tag.attrs:
        return img_tag['src']

    # extract bio info (born, age ,nationality, position, taille)

    # Return message if the image tag is not found
    return print("Player image not found.")



# Function get_players_info()
# Need get_player_image

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


### Function do get info an NBA player

def player_last_stats(player_picked, n_games = 5):

    # Get info about the player
    player_id = players.find_players_by_full_name(player_picked)[0]['id']

    #Get the player's game logs for the current season
    game_log = playergamelog.PlayerGameLog(player_id=player_id)  # Adjust the season if needed
    games_data = game_log.get_data_frames()[0]  # Retrieve the DataFrame

    # Reorder the columns and add location column
    last_n_games = games_data.head(n_games).copy()
    last_n_games['location'] = last_n_games['MATCHUP'].apply(lambda x: "home" if 'vs' in x else "away")

    # get the score of the games
    last_n_games['score']='not found'

    for index, row in last_n_games.iterrows():
        game_id = row['Game_ID']
        box_score = BoxScoreSummaryV2(game_id=game_id)
        # Extract game data
        game_box = box_score.get_normalized_dict()

        score_0 = game_box['LineScore'][0]['PTS'] # position of the linescore is not link with the name of the team or the location of the game
        score_1 = game_box['LineScore'][1]['PTS'] # to make it better needs couple of test (if) it will take to much time, i give up for now

        last_n_games.loc[index, 'score'] = f'{score_0}-{score_1}'


    # Reorder the columns
    last_n_games = last_n_games[['GAME_DATE', 'Game_ID', 'MATCHUP', 'location', 'score', 'WL', 'MIN', 'PTS', 'REB',
                               'AST', 'STL', 'BLK', 'FGA', 'FG_PCT', 'FG3A',
                               'FG3_PCT', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'TOV', 'PF', 'PLUS_MINUS']]

    last_n_games.reset_index(drop=True, inplace=True)

    return [last_n_games, player_id]


# Function to get the URL of the video of the player picked

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

    return video_event_df

### Function to get all the mp4 url of the 4 bests performer of the day with the "Best option"
# V2 load them on a container

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
