# select video_event_pd where desc does not contain remove terms

def select_sequences(pbp, player_id, game_location, option):
    """
    Function to select the  sequences in a play by play dataframe for one player
    Needs :
     - pbp df
     - id of the player
     - game location
     - options = ['Full', 'Best', 'FGA', 'FGM', 'AST', 'REB', 'BLOCK'],

    Return:
        - dataframe of selected sequences

    """
    if option == 'Best':
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id)) |
                            (pbp['PLAYER2_ID'] == int(player_id)) ]

        Remove_terms = ['REBOUND', 'MISS', 'Free Throw']

        if game_location == 'away':
            pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(Remove_terms), na=False) == False) ]
        if game_location == 'home':
            pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(Remove_terms), na=False) == False) ]

    else:
        if option == 'FGA':
            pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]
            selected_terms = ['PTS', '3PT', 'Shot']

        if option == 'FGM':
            pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]
            selected_terms = ['PTS']

        if option == 'AST':
            pbp_player = pbp[(pbp['PLAYER2_ID'] == int(player_id))]
            selected_terms = ['AST']

        if option == 'REB':
            pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]
            selected_terms = ['REBOUND']

        if option == 'BLOCK':
            pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id)) |
                            (pbp['PLAYER2_ID'] == int(player_id)) |
                            (pbp['PLAYER3_ID'] == int(player_id)) ]
            selected_terms = ['BLOCK']


        if game_location == 'away':
            pbp_player = pbp_player[(pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]
        if game_location == 'home':
            pbp_player = pbp_player[(pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(selected_terms), na=False) == True) ]


    return pbp_player
