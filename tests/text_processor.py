import re

if __name__ == '__main__':
    pattern_kickoff = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Kicker name
     \skickoff\s
     (?P<nb_yards>\d+)                             # Number of yards kicked
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
    """, re.VERBOSE)

    pattern_return = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \sreturn\s
     (?P<nb_yards>\d+)                             # Number of yards kicked
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
     """, re.VERBOSE)

    pattern_tackle = re.compile(r"""
     (?<=(\(|\;))                                  # ( or ; preceding
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     (?=(\)|\;))                                   # ; or ) following
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
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
     """, re.VERBOSE)
    pattern_rush_noGain = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Rusher name
     \srush[^,.]+for\sno\sgain\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
     """, re.VERBOSE)
    pattern_rush_loss = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Rusher name
     \srush[^,.]+for\sloss\sof\s
     (?P<nb_yards>\d+)                             # Number of Yards lost
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
     """, re.VERBOSE)

    pattern_firstDown = re.compile(r"""
     1ST DOWN
     """, re.VERBOSE)

    pattern_touchdown = re.compile(r"""
     TOUCHDOWN
     """, re.VERBOSE)

    pattern_pass_complete = re.compile(r"""
     (?P<player_passing>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)     # Passer name
     [^,.]+pass\scomplete\sto\s
     (?P<player_receiving>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)   # Receiver name
     \sfor\s
     (?P<nb_yards>\d+)                                    # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                                  # Team Name Yard Line
    """, re.VERBOSE)
    pattern_pass_incomplete = re.compile(r"""
     (?P<player_passing>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)          # Passer name
     [^,.]+pass\sincomplete\s
     (to\s(?P<player_receiving>[A-Z]\.([a-z]\.)?[A-Za-z\-]+))* # Receiver name
    """, re.VERBOSE)
    pattern_pass_intercepted = re.compile(r"""
     (?P<player_passing>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)      # Passer name
     [^,.]+pass\sintercepted\sby\s
     (?P<player_intercepting>[A-Z]\.([a-z]\.)?[A-Za-z\-]+) # Interceptor
     \sat\sthe\s
     (?P<tnyl>[A-Z]+\d+)                                   # Team Name Yard Line
    """, re.VERBOSE)

    pattern_run = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \sfor\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
    """, re.VERBOSE)

    pattern_sack = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \ssacked\sfor\sloss\sof\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
    """, re.VERBOSE)

    pattern_punt = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)    # Player name
     \spunt\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
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
     (?P<tnyl>[A-Z]+\d+)                                   # Team Name Yard Line
    """, re.VERBOSE)

    patterns = {'kickoff': pattern_kickoff,
                'return': pattern_return,
                'tackle': pattern_tackle,
                'extraPoint': pattern_extraPoint,
                'rush_gain': pattern_rush_gain,
                'rush_loss': pattern_rush_loss,
                'rush_noGain': pattern_rush_noGain,
                'firstDown': pattern_firstDown,
                'touchdown': pattern_touchdown,
                'pass_complete': pattern_pass_complete,
                'pass_incomplete': pattern_pass_incomplete,
                'pattern_pass_intercepted': pattern_pass_intercepted,
                'run': pattern_run,
                'sack': pattern_sack,
                'punt': pattern_punt,
                'fg': pattern_fg,
                'fairCatch': pattern_fairCatch,
                'touchback': pattern_touchback,
                'safety': pattern_safety,
                'fumble': pattern_fumble,
                'fumble_forced': pattern_fumble_forced}

    with open('./test_sentences.txt', 'r') as sentences_file:
        for sentence in sentences_file:
            type_of_play = []
            if not ("no play" in sentence.casefold()):
                for type, pattern in patterns.items():
                    iter_res = pattern.finditer(sentence)
                    for res in iter_res:
                        type_of_play.append(
                            (type, res.groupdict(), res.span())
                        )
                type_of_play.sort(key=lambda x: x[2])
                print(type_of_play)
            else:
                print("No play call, ignoring")
