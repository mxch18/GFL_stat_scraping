import re
import ast
import pandas as pd

if __name__ == '__main__':
    pattern_kickoff = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Kicker name
     \skickoff\s
     (?P<nb_yards>\d+)                             # Number of yards kicked
     \syard(s)*\sto\sthe\s
     (?P<location>[A-Z]+\d+)                           # Location
    """, re.VERBOSE)

    pattern_return = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \sreturn\s
     (?P<nb_yards>\d+)                             # Number of yards kicked
     \syard(s)*\sto\sthe\s
     (?P<location>[A-Z]+\d+)                           # Location
     """, re.VERBOSE)

    pattern_tackle = re.compile(r"""
     (\;|[A-Z]+\d+\s\(|1ST\sDOWN\s[A-Z]+\s\()
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
     (?P<location>[A-Z]+\d+)                           # Location
     """, re.VERBOSE)
    pattern_rush_noGain = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Rusher name
     \srush[^,.]+for\sno\sgain\sto\sthe\s
     (?P<location>[A-Z]+\d+)                           # Location
     """, re.VERBOSE)
    pattern_rush_loss = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Rusher name
     \srush[^,.]+for\sloss\sof\s
     (?P<nb_yards>\d+)                             # Number of Yards lost
     \syard(s)*\sto\sthe\s
     (?P<location>[A-Z]+\d+)                           # Location
     """, re.VERBOSE)

    pattern_firstDown = re.compile(r"""
     1ST DOWN
     """, re.VERBOSE)

    pattern_touchdown = re.compile(r"""
     TOUCHDOWN
     """, re.VERBOSE)

    pattern_pass_complete = re.compile(r"""
     (?P<passer>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)     # Passer name
     [^,.]+pass\scomplete\sto\s
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)   # Receiver name
     \sfor\s
     (?P<nb_yards>\d+)                                    # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<location>[A-Z]+\d+)                                  # Location
    """, re.VERBOSE)
    pattern_pass_incomplete = re.compile(r"""
     (?P<passer>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)          # Passer name
     [^,.]+pass\sincomplete\s
     (to\s(?P<receiver>[A-Z]\.([a-z]\.)?[A-Za-z\-]+))* # Receiver name
    """, re.VERBOSE)
    pattern_pass_intercepted = re.compile(r"""
     (?P<passer>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)      # Passer name
     [^,.]+pass\sintercepted\sby\s
     (?P<interceptor>[A-Z]\.([a-z]\.)?[A-Za-z\-]+) # Interceptor
     \sat\sthe\s
     (?P<location>[A-Z]+\d+)                                   # Location
    """, re.VERBOSE)

    pattern_run = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \sfor\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<location>[A-Z]+\d+)                           # Location
    """, re.VERBOSE)

    pattern_sack = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \ssacked\sfor\sloss\sof\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<location>[A-Z]+\d+)                           # Location
    """, re.VERBOSE)

    pattern_punt = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \spunt\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<location>[A-Z]+\d+)                           # Location
    """, re.VERBOSE)
    pattern_punt_blocked = re.compile(r"""
     (?P<punter>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Punter name
     \spunt\sBLOCKED,\srecovered\sby\s[A-Z]+\s
     (?P<player_recovering>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Recovering name
     \sat\s
     (?P<location>[A-Z]+\d+)                           # Location
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
     (?P<location>[A-Z]+\d+)                                   # Location
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
                 'rcv_yds_per_game', 'rcv_catch_pct']
    index_rush = ['rush_att', 'rush_yds', 'rush_td', 'rush_first_down', 'rush_2pm',
                  'rush_2pa', 'rush_long', 'rush_yds_per_att', 'rush_yds_per_game',
                  'rush_per_game']
    index_fmbl = ['fmbl_ff', 'fmbl_fmbl',
                  'fmbl_recov', 'fmbl_recov_yds', 'fmbl_td']
    index_int = ['int_nb', 'int_yds', 'int_td',
                 'int_long', 'int_def_pass', 'int_tb']
    index_tackle = ['tackle_sk', 'tackle_ast', 'tackle_solo', 'tackle_tfl', 'tackle_qbh',
                    'tackle_blk_kick', 'tackle_safety', 'tackle_cmb']
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
                   *index_punt, *index_misc]

    filename = '../games/gfl/2022/2022-08-27_(Duesseldorf Panther)@(Potsdam Royals).game'

    with open(filename, 'r') as sentences_file:
        # read first line (participation report)
        participation_report_str = sentences_file.readline().strip('\n')
        participation_report_dict = ast.literal_eval(participation_report_str)
        # build pandas game dataframe
        df_game = pd.DataFrame()
        for team, roster in participation_report_dict.items():
            for player in roster:
                # player = (name, position, number, isStarter)
                df_game[player[0]] = pd.Series(
                    0, index=index_stats, dtype=object)
                df_game[player[0]][index_misc] = [team, *list(player[1:])]
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
                previous_play = (None, None, None)
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

                        for player in players:
                            df_game[player][play_type] += 1
                            if previous_play[0] == 'sack':
                                # it's a sack
                                df_game[player]['tackle_sk'] = 1 - assist*0.5
                            elif previous_play[0] == 'rush_loss':
                                # it's a tackle for loss
                                df_game[player]['tackle_tfl'] = 1 - assist*0.5
                    elif play_type == 'run':
                        player = play[1]['player']
                        yds = int(play[1]['nb_yards'])
                        if previous_play[0] in ['pass_complete', 'run', 'rush_gain', 'ret_kick', 'ret_punt']:
                            # means it was a lateral pass
                            df_game[previous_play[1]['player']
                                    ]['pass_lateral'] += 1
                            df_game[player]['rush_att'] += 1
                            df_game[player]['rush_yds'] += yds
                            longest = df_game[player]['rush_long']
                            df_game[player]['rush_long'] = yds if yds > longest else longest
                        elif previous_play[0] == 'fumble':
                            # it's a fumble return
                            df_game[player]['rush_att'] += 1
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
                            df_game[previous_play[1]['player']
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
                    previous_play = (play_type, *play[1:])

            else:
                print("No play call, ignoring")
                print("No play call, ignoring")
        print(df_game['M.Achiepi'].to_string())
        print(df_game['N.Lawrence'].to_string())
        print(df_game['C.Cranston'].to_string())
        print(df_game['S.Dardour'].to_string())
