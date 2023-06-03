import re
import ast
import pandas as pd

if __name__ == '__main__':
    pattern_kickoff = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Kicker name
     \skickoff\s
     (?P<nb_yards>\d+)                             # Number of yards kicked
     \syard(s)*\sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                           # Location
    """, re.VERBOSE)

    pattern_return = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \sreturn\s
     (?P<nb_yards>\d+)                             # Number of yards kicked
     \syard(s)*\sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                           # Location
     """, re.VERBOSE)

    pattern_tackle = re.compile(r"""
     (\;|[A-Z]+\d+\s\(|1ST\sDOWN\s[A-Z]+\s\(|yardline\s\(|out-of-bounds\s\()
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)
    """, re.VERBOSE)

    pattern_extraPoint = re.compile(r"""
    (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
    \s
    (?P<type>kick|rush)                           # Type of extra point
    \sattempt\s
    (?P<result>good|failed)                       # Good or bad attempt
    """, re.VERBOSE)

    # rush
    pattern_rush_gain = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Rusher name
     \srush[^,.]+for\s
     (?P<nb_yards>\d+)                             # Number of Yards gained
     \syard(s)*\sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                           # Location
     """, re.VERBOSE)
    pattern_rush_noGain = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Rusher name
     \srush[^,.]+for\sno\sgain\sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                           # Location
     """, re.VERBOSE)
    pattern_rush_loss = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Rusher name
     \srush[^,.]+for\sloss\sof\s
     (?P<nb_yards>\d+)                             # Number of Yards lost
     \syard(s)*\sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                           # Location
     """, re.VERBOSE)

    pattern_firstDown = re.compile(r"""
     1ST\sDOWN
     """, re.VERBOSE)

    pattern_touchdown = re.compile(r"""
     TOUCHDOWN
     """, re.VERBOSE)

    pattern_pass_complete = re.compile(r"""
     (?P<passer>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)     # Passer name
     [^,.]+pass\scomplete\sto\s
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)   # Receiver name
     \sfor\s
     ((?P<for_loss>loss\sof\s)?(?P<nb_yards>\d+)\syard(s)*|no\sgain) # Yards number
     \sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)             # Location
    """, re.VERBOSE)
    pattern_pass_incomplete = re.compile(r"""
     (?P<passer>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)             # Passer name
     [^,.]+pass\sincomplete
     (\sto\s(?P<receiver>[A-Z]\.([a-z]\.)?[A-Za-z\-]+))*  # Receiver name
     (\s\((?P<breakuper>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)\))*   # Pass breakup
    """, re.VERBOSE)
    pattern_pass_intercepted = re.compile(r"""
     (?P<passer>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)      # Passer name
     [^,.]+pass\sintercepted\sby\s
     (?P<interceptor>[A-Z]\.([a-z]\.)?[A-Za-z\-]+) # Interceptor
     \sat\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)             # Location
    """, re.VERBOSE)

    pattern_run = re.compile(r"""
     (?<!to\s)                                  # not preceded by "to "
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \sfor\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)       # Location
    """, re.VERBOSE)

    pattern_sack = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \ssacked\sfor\sloss\sof\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                           # Location
    """, re.VERBOSE)

    pattern_punt = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \spunt\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                           # Location
    """, re.VERBOSE)
    pattern_punt_blocked = re.compile(r"""
     (?P<punter>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Punter name
     \spunt\sBLOCKED,\srecovered\sby\s[A-Z]+\s
     (?P<player_recovering>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Recovering name
     \sat\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                           # Location
     \s\(blocked\sby\s
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
    """, re.VERBOSE)

    pattern_fg = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \sfield\sgoal\sattempt\sfrom\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \s
     (?P<result>GOOD|MISSED)                       # Good or missed
    """, re.VERBOSE)

    pattern_fairCatch = re.compile(r"""
     fair\scatch\sby\s
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
    """, re.VERBOSE)
    pattern_touchback = re.compile(r"""
     touchback
    """, re.VERBOSE)

    pattern_safety = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \ssafety
    """, re.VERBOSE)

    pattern_fumble_forced = re.compile(r"""
     fumble\sforced\sby\s
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)            # Player forcing
    """, re.VERBOSE)
    pattern_fumble = re.compile(r"""
     fumble\sby\s
     (?P<player_fumbling>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)   # Player fumbling
     \srecovered\sby\s
     (?P<team_recovering>[A-Z]+)                           # Team recovering
     \s
     (?P<player_recovering>[A-Z]\.([a-z]\.)?[A-Za-z\-]+) # Player recovering
     \sat\s
     ((?P<location>[A-Z]+\d+)|50\syardline)                      # Location
    """, re.VERBOSE)

    patterns = {'kickoff': pattern_kickoff,  # ok
                'return': pattern_return,  # ok
                'tackle': pattern_tackle,  # ok
                'extraPoint': pattern_extraPoint,
                'rush_gain': pattern_rush_gain,
                'rush_loss': pattern_rush_loss,
                'rush_noGain': pattern_rush_noGain,
                'firstDown': pattern_firstDown,  # ok
                'touchdown': pattern_touchdown,  # ok
                'pass_complete': pattern_pass_complete,
                'pass_incomplete': pattern_pass_incomplete,
                'pass_intercepted': pattern_pass_intercepted,
                'run': pattern_run,  # ok
                'sacked': pattern_sack,
                'punt': pattern_punt,  # ok
                'punt_blk': pattern_punt_blocked,  # ok
                'fg': pattern_fg,
                'fairCatch': pattern_fairCatch,
                'touchback': pattern_touchback,  # ok
                'safety': pattern_safety,  # ok
                'fumble': pattern_fumble, # ok
                'fumble_forced': pattern_fumble_forced} # ok

    index_pass = ['pass_cmp', 'pass_att', 'pass_cmp_pct', 'pass_yds_gain',
                  'pass_td', 'pass_td_pct', 'pass_int', 'pass_int_pct',
                  'pass_first_down', 'pass_long', 'pass_sack', 'pass_lateral',
                  'pass_yds_loss', 'pass_net_yds_per_att', 'pass_yds_per_game',
                  'pass_yds_per_cmp']
    index_rcv = ['rcv_targets', 'rcv_recep', 'rcv_yds_gain', 'rcv_yds_per_recep',
                 'rcv_td', 'rcv_first_down', 'rcv_long', 'rcv_per_game',
                 'rcv_yds_per_game', 'rcv_catch_pct', 'rcv_yds_loss']
    index_rush = ['rush_att', 'rush_td', 'rush_first_down', 'rush_2pm', 'rush_2pa',
                  'rush_long', 'rush_yds_per_att', 'rush_yds_per_game',
                  'rush_per_game', 'rush_att_gain', 'rush_att_loss', 'rush_att_noGain',
                  'rush_yds_gain', 'rush_yds_loss', 'rush_yds_net']
    index_fmbl = ['fmbl_ff', 'fmbl_fmbl',
                  'fmbl_recov', 'fmbl_recov_yds', 'fmbl_td']
    index_int = ['int_nb', 'int_yds', 'int_td',
                 'int_long', 'int_def_pass', 'int_tb']
    index_tackle = ['tackle_sk', 'tackle_ast', 'tackle_solo', 'tackle_tfl', 'tackle_qbh',
                    'tackle_blk_kick', 'tackle_safety', 'tackle_cmb', 'tackle_tfl_yds',
                    'tackle_sk_yds']
    index_ret_kick = ['ret_kick_nb', 'ret_kick_yds', 'ret_kick_td', 'ret_kick_long',
                      'ret_kick_yds_per']
    index_ret_punt = ['ret_punt_nb', 'ret_punt_yds', 'ret_punt_td', 'ret_punt_long',
                      'ret_punt_yds_per']
    index_kick = ['kick_0-19_fga', 'kick_0-19_fgm', 'kick_20-29_fga', 'kick_20-29_fgm',
                  'kick_30-39_fga', 'kick_30-39_fgm', 'kick_40-49_fga', 'kick_40-49_fgm',
                  'kick_50_fga', 'kick_50_fgm', 'kick_long', 'kick_xp_att', 'kick_xp_made',
                  'kick_fgm', 'kick_fga', 'kick_fg_pct', 'kick_ko_nb', 'kick_ko_yds',
                  'kick_ko_oob', 'kick_ko_tb', 'kick_ko_long']
    index_punt = ['punt_nb', 'punt_yds', 'punt_yds_ret', 'punt_yds_net', 'punt_long',
                  'punt_tb', 'punt_in20', 'punt_in20_pct', 'punt_blk']
    index_misc = ['team', 'position', 'number', 'isStarter']

    index_stats = [*index_pass, *index_rcv, *index_rush, *index_fmbl, *index_int,
                   *index_tackle, *index_ret_kick, *index_ret_punt, *index_kick,
                   *index_punt]

    # filename = '../games/gfl/2022/2022-08-27_(Duesseldorf Panther)@(Potsdam Royals).game'
    filename = '../games/gfl/2022/2022-08-14_(New Yorker Lions Br.)@(Cologne Crocodiles).game'

    with open(filename, 'r') as sentences_file:
        # read first line (participation report)
        participation_report_str = sentences_file.readline().strip('\n')
        participation_report_dict = ast.literal_eval(participation_report_str)

        df_game = pd.DataFrame()
        player_series = {}
        for team, roster in participation_report_dict.items():
            for player in roster:
                # player = (name, position, number, isStarter)
                # build dict of Series
                numeric_stats = pd.Series(0, index=index_stats, dtype=object)
                non_num_stats = pd.Series([team, *list(player[1:])],
                                          index=index_misc, dtype=object)
                player_series[player[0]] = pd.concat(
                    [numeric_stats, non_num_stats])
        # build pandas game dataframe
        df_game = pd.DataFrame(player_series)
        previous_play = (None, None, None)
        for line in sentences_file:
            play_info = line.split('$')
            play_description = play_info[-1]
            type_of_play = []
            if not ("no play" in play_description.casefold()):
                for type, pattern in patterns.items():
                    iter_res = pattern.finditer(play_description)
                    count = 0
                    for res in iter_res:
                        count += 1
                        type_of_play.append(
                            (type, res.groupdict(), res.span())
                        )
                    if type == 'tackle' and count > 1:
                        # fuse separate tackles into one
                        player_list = []
                        for i in range(count):
                            temp = type_of_play.pop()
                            player_list.append(temp[1]['player'])
                            span = temp[2]
                        type_of_play.append(
                            (type, {'player': player_list}, span)
                        )

                type_of_play.sort(key=lambda x: x[2])
                for play in type_of_play:
                    play_type = play[0]
                    if play_type == 'kickoff':
                        player = play[1]['player']
                        yds = int(play[1]['nb_yards'])
                        df_game[player]['kick_ko_nb'] += 1
                        df_game[player]['kick_ko_yds'] += yds
                        longest = df_game[player]['kick_ko_long']
                        df_game[player]['kick_ko_long'] = yds if yds > longest else longest
                    elif play_type == 'return':
                        player = play[1]['player']
                        yds = int(play[1]['nb_yards'])
                        if previous_play[0] == 'kickoff':
                            play_type = 'ret_kick'
                        elif previous_play[0] == 'punt':
                            play_type = 'ret_punt'
                        elif previous_play[0] == 'pass_intercepted':
                            play_type = 'int'
                        else:
                            print(f"Return on {previous_play[0]}, skipping")
                            continue
                        if not play_type == 'int':
                            df_game[player][play_type+'_nb'] += 1
                        df_game[player][play_type+'_yds'] += yds

                        longest = df_game[player][play_type+'_long']
                        df_game[player][play_type
                                        + '_long'] = yds if yds > longest else longest
                    elif play_type == 'tackle':
                        players = play[1]['player']
                        play_type = 'tackle_ast'
                        assist = isinstance(players, list)
                        if not assist:
                            players = [players]
                            play_type = 'tackle_solo'

                        # print(
                        #     f"\nplay:{play}\nprevious:{previous_play}\nassist:{assist}\nplayers:{players}\nplay_type:{play_type}")
                        for player in players:
                            if previous_play[0] == 'sacked':
                                # it's a sack
                                df_game[player][play_type] += 1
                                df_game[player]['tackle_sk'] += 1 - assist*0.5
                                df_game[player]['tackle_sk_yds'] += int(
                                    previous_play[1]['nb_yards'])
                            elif previous_play[0] == 'rush_loss':
                                # it's a tackle for loss
                                df_game[player][play_type] += 1
                                df_game[player]['tackle_tfl'] += 1 - assist*0.5
                                df_game[player]['tackle_tfl_yds'] += int(
                                    previous_play[1]['nb_yards'])
                            else:
                                df_game[player][play_type] += 1
                    elif play_type == 'run':
                        player = play[1]['player']
                        yds = int(play[1]['nb_yards'])
                        if previous_play[0] in ['pass_complete', 'run', 'rush_gain', 'ret_kick', 'ret_punt']:
                            # means it was a lateral pass
                            df_game[previous_play[1]['player']
                                    ]['pass_lateral'] += 1
                            df_game[player]['rush_att_gain'] += 1
                            df_game[player]['rush_yds_gain'] += yds
                            longest = df_game[player]['rush_long']
                            df_game[player]['rush_long'] = yds if yds > longest else longest
                        elif previous_play[0] == 'fumble':
                            # it's a fumble return
                            df_game[player]['rush_att_gain'] += 1
                            df_game[player]['fmbl_recov_yds'] += int(yds)
                            play_type = 'ret_fmbl'
                    elif play_type == 'fumble':
                        fumbler = play[1]['player_fumbling']
                        recoverer = play[1]['player_recovering']
                        df_game[fumbler]['fmbl_fmbl'] += 1
                        df_game[recoverer]['fmbl_recov'] += 1
                    elif play_type == 'fumble_forced':
                        player = play[1]['player']
                        df_game[player]['fmbl_ff'] += 1
                    elif play_type == 'safety':
                        df_game[player]['tackle_safety'] += 1
                    elif play_type == 'firstDown':
                        if previous_play[0] == 'pass_complete':
                            df_game[previous_play[1]['passer']
                                    ]['pass_first_down'] += 1
                            df_game[previous_play[1]['player']
                                    ]['rcv_first_down'] += 1
                        elif previous_play[0] == 'rush_gain':
                            df_game[previous_play[1]['player']
                                    ]['rush_first_down'] += 1
                    elif play_type == 'touchdown':
                        if previous_play[0] == 'pass_complete':
                            df_game[previous_play[1]['player']]['rcv_td'] += 1
                            df_game[previous_play[1]['passer']]['pass_td'] += 1
                            play_type = 'pass_td'
                        elif previous_play[0] in ['rush_gain', 'run']:
                            df_game[previous_play[1]['player']]['rush_td'] += 1
                            play_type = 'rush_td'
                        elif previous_play[0] == 'ret_fmbl':
                            df_game[previous_play[1]['player']]['fmbl_td'] += 1
                            play_type = 'fmbl_td'
                        elif previous_play[0] in ['ret_kick', 'ret_punt', 'int']:
                            play_type = previous_play[0] + '_td'
                            df_game[previous_play[1]['player']][play_type] += 1
                    elif play_type == 'touchback':
                        if previous_play[0] == 'kickoff':
                            df_game[previous_play[1]['player']
                                    ]['kick_ko_tb'] += 1
                        elif previous_play[0] == 'punt':
                            df_game[previous_play[1]['player']
                                    ]['punt_tb'] += 1
                        elif previous_play[0] == 'pass_intercepted':
                            df_game[previous_play[1]['player']
                                    ]['int_tb'] += 1
                    elif play_type == 'fairCatch':
                        pass
                    elif play_type == 'punt':
                        player = play[1]['player']
                        yds = int(play[1]['nb_yards'])
                        df_game[player]['punt_nb'] += 1
                        df_game[player]['punt_yds'] += int(yds)
                        longest = df_game[player]['punt_long']
                        df_game[player]['punt_long'] = yds if yds > longest else longest
                    elif play_type == 'punt_blk':
                        punter = play[1]['punter']
                        player = play[1]['player']
                        df_game[punter]['punt_blk'] += 1
                        df_game[player]['tackle_blk'] += 1
                    elif play_type == 'extraPoint':
                        xp_type = play[1]['type']
                        player = play[1]['player']
                        result = play[1]['result']
                        if xp_type == 'rush':
                            df_game[player]['rush_2pa'] += 1
                            if result == 'good':
                                df_game[player]['rush_2pm'] += 1
                        elif xp_type == 'kick':
                            df_game[player]['kick_xp_att'] += 1
                            if result == 'good':
                                df_game[player]['kick_xp_made'] += 1
                    elif play_type == 'fg':
                        yds = int(play[1]['nb_yards'])
                        player = play[1]['player']
                        result = play[1]['result']
                        txt = ['0-19', '20-29', '30-39', '40-49', '50']
                        dist = [19, 29, 39, 40, 100]
                        cat = next(x for i, x in enumerate(
                            txt) if yds < dist[i])
                        df_game[player]['kick_'+cat+'_fga'] += 1
                        if result == 'GOOD':
                            df_game[player]['kick_'+cat+'_fgm'] += 1
                            longest = df_game[player]['kick_long']
                            df_game[player]['kick_long'] = yds if yds > longest else longest
                    elif play_type == 'pass_complete':
                        yds = int(play[1]['nb_yards']
                                  ) if play[1]['nb_yards'] else 0
                        player = play[1]['player']
                        passer = play[1]['passer']

                        df_game[passer]['pass_att'] += 1
                        df_game[passer]['pass_cmp'] += 1
                        df_game[player]['rcv_targets'] += 1
                        df_game[player]['rcv_recep'] += 1

                        gain_loss = 'loss' if play[1]['for_loss'] else 'gain'

                        df_game[passer]['pass_yds_' + gain_loss] += yds
                        df_game[player]['rcv_yds_' + gain_loss] += yds

                        if not play[1]['for_loss']:
                            longest = df_game[passer]['pass_long']
                            df_game[passer]['pass_long'] = yds if yds > longest else longest

                            longest = df_game[player]['rcv_long']
                            df_game[player]['rcv_long'] = yds if yds > longest else longest

                    elif play_type == 'pass_incomplete':
                        passer = play[1]['passer']
                        receiver = play[1]['receiver']
                        breakuper = play[1]['breakuper']
                        df_game[passer]['pass_att'] += 1

                        if receiver:
                            df_game[receiver]['rcv_targets'] += 1
                        if breakuper:
                            df_game[breakuper]['int_def_pass'] += 1

                    elif play_type == 'pass_intercepted':
                        passer = play[1]['passer']
                        interceptor = play[1]['interceptor']

                        df_game[passer]['pass_att'] += 1
                        df_game[passer]['pass_int'] += 1
                        df_game[interceptor]['int_nb'] += 1

                    elif play_type == 'rush_gain':
                        yds = int(play[1]['nb_yards'])
                        player = play[1]['player']

                        df_game[player]['rush_att_gain'] += 1
                        df_game[player]['rush_yds_gain'] += yds

                        longest = df_game[player]['rush_long']
                        df_game[player]['rush_long'] = yds if yds > longest else longest

                    elif play_type == 'rush_noGain':
                        player = play[1]['player']

                        df_game[player]['rush_att_noGain'] += 1

                    elif play_type == 'rush_loss':
                        yds = int(play[1]['nb_yards'])
                        player = play[1]['player']

                        df_game[player]['rush_att_loss'] += 1
                        df_game[player]['rush_yds_loss'] += yds

                    elif play_type == 'sacked':
                        yds = int(play[1]['nb_yards'])
                        player = play[1]['player']

                        df_game[player]['pass_sack'] += 1
                        df_game[player]['pass_yds_loss'] += yds

                    if not play_type == 'firstDown':  # first downs don't update state
                        previous_play = (play_type, *play[1:])

        # Compute team scores
        # t = 'Cologne Crocodiles'
        t = 'New Yorker Lions Br.'
        df_game = df_game.T  # pandas is best used with column selection
        df_game['rush_att'] = df_game['rush_att_gain'] + \
            df_game['rush_att_loss']+df_game['rush_att_noGain']
        print(t)
        df_t = df_game.query(f'team == "{t}"')
        print(f"{df_t['tackle_sk'].sum()}-{df_t['tackle_sk_yds'].sum()}")
        # print(df_game['D.McCants '][''])
