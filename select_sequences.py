# select video_event_pd where desc does not contain remove terms

def select_sequences(pbp, player_id, game_location, option):
    """
    Select sequences for one player from a play-by-play dataframe.
    """
    if option == 'Full':
        pbp_player = pbp[
            (pbp['PLAYER1_ID'] == int(player_id)) |
            (pbp['PLAYER2_ID'] == int(player_id))
        ]

    elif option == 'Best':
        pbp_player = pbp[
            (pbp['PLAYER1_ID'] == int(player_id)) |
            (pbp['PLAYER2_ID'] == int(player_id))
        ]

        remove_terms = ['REBOUND', 'MISS', 'Free Throw']
        if game_location == 'away':
            pbp_player = pbp_player[
                ~pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(remove_terms), na=False)
            ]
        elif game_location == 'home':
            pbp_player = pbp_player[
                ~pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(remove_terms), na=False)
            ]

    elif option == 'FGA':
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]
        selected_terms = ['PTS', '3PT', 'Shot']

    elif option == 'FGM':
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]
        selected_terms = ['PTS']

    elif option == 'AST':
        pbp_player = pbp[(pbp['PLAYER2_ID'] == int(player_id))]
        selected_terms = ['AST']

    elif option == 'REB':
        pbp_player = pbp[(pbp['PLAYER1_ID'] == int(player_id))]
        selected_terms = ['REBOUND']

    elif option == 'BLOCK':
        pbp_player = pbp[
            (pbp['PLAYER1_ID'] == int(player_id)) |
            (pbp['PLAYER2_ID'] == int(player_id)) |
            (pbp['PLAYER3_ID'] == int(player_id))
        ]
        selected_terms = ['BLOCK']

    # Apply selected_terms filters for all but "Full" and "Best"
    if option not in ['Full', 'Best']:
        if game_location == 'away':
            pbp_player = pbp_player[
                pbp_player['VISITORDESCRIPTION'].str.contains('|'.join(selected_terms), na=False)
            ]
        elif game_location == 'home':
            pbp_player = pbp_player[
                pbp_player['HOMEDESCRIPTION'].str.contains('|'.join(selected_terms), na=False)
            ]

    pbp_player = pbp_player.drop_duplicates(subset=['EVENTNUM']).sort_values(by=['EVENTNUM'])
    print(pbp_player)

    return pbp_player
