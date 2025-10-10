### Function to get the last stats of the day by scraping the page
# 'https://cdn.nba.com/static/json/staticData/EliasGameStats/00/all_players_day.txt'


import requests
import pandas as pd


def get_best_players_day(number = 4):

    """
    Function to get a dataframe of the 5 (or more it's a param) players with a high performance and 2 lists
    famous players regarding thers superstar status or nationality
    the list would be able to be a param that the enduser will define as is favorit players

    """
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
    Four_best_day = df.sort_values(by='MyScore', ascending=False).head(number)


    ### Add superstars
    my_champs_superstars = ["Jokic, Nikola ","Doncic, Luka", "Durant, Kevin", "Curry, Stephen", "Sengun, Alperen"]

    ### French players
    my_champs_french = ["Wembanyama, Victor", "Gobert, Rudy", "Yabusele, Guerschon", "Sarr, Alex", "Coulibaly, Bilal", "Beringer, Joan"]

    champs_list = my_champs_superstars + my_champs_french

    best_players_day = df[df['NAME'].isin(champs_list)]

    best_players_day = pd.concat([Four_best_day,best_players_day]).drop_duplicates()

    best_players_day['Formatted_name'] = 'name'

    # loop to reorder name properly when ther is a Jr in the name
    for index, row in best_players_day.iterrows():
      name = row['NAME']

      if 'Jr.' in row['NAME']:
        nm_list = name.replace('Jr.', '').rstrip().split(", ")[::-1]
        nm_list.append('Jr.')
        best_players_day.loc[index, 'Formatted_name'] =" ".join(nm_list).lower()

      else:
        best_players_day.loc[index, 'Formatted_name'] = " ".join(row['NAME'].split(", ")[::-1]).lower()


    return best_players_day
