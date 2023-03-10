import re

if __name__ == '__main__':
    pattern_kickoff = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Kicker name
     \skickoff\s
     (?P<nb_yards>\d+)                             # Number of yards kicked
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
    """, re.VERBOSE)

    pattern_return = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
     \sreturn\s
     (?P<nb_yards>\d+)                             # Number of yards kicked
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
     """, re.VERBOSE)

    pattern_tackle = re.compile(r"""
     (?<=(\(|\;))                                  # ( or ; preceding
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
     (?=(\)|\;))")                                 # ; or ) following
    """, re.VERBOSE)

    pattern_extraPoint = re.compile(r"""
    (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
    \s
    (kick|rush)                                   # Type of extra point
    \sattempt\s
    (good|failed)                                 # Good or bad attempt
    """, re.VERBOSE)

    # rush
    pattern_rush_gain = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Rusher name
     \srush.*for\s
     (?P<nb_yards>\d+)                             # Number of Yards gained
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
     """, re.VERBOSE)
    pattern_rush_noGain = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Rusher name
     \srush.*for\sno\sgain\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
     """, re.VERBOSE)
    pattern_rush_loss = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Rusher name
     \srush.*for\sloss\sof\s
     (?P<nb_yards>\d+)                             # Number of Yards lost
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
     """, re.VERBOSE)

    pattern_firstDown = re.compile(
     r"1ST DOWN")

    pattern_pass_complete = re.compile(r"""
     (?P<player_passing>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)   # Passer name
     .*pass\scomplete\sto\s
     (?P<player_receiving>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+) # Receiver name
     \sfor\s
     (?P<nb_yards>\d+)                                    # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                                  # Team Name Yard Line
    """, re.VERBOSE)
    pattern_pass_incomplete = re.compile(r"""
     (?P<player_passing>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)          # Passer name
     .*pass\sincomplete\s
     (to\s(?P<player_receiving>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+))* # Receiver name
    """, re.VERBOSE)

    pattern_run = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
     \sfor\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
    """, re.VERBOSE)

    pattern_sack = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
     \ssacked\sfor\sloss\sof\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
    """, re.VERBOSE)

    pattern_punt = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
     \spunt\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \syard(s)*\sto\sthe\s
     (?P<tnyl>[A-Z]+\d+)                           # Team Name Yard Line
    """, re.VERBOSE)

    pattern_fg = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
     \sfield\sgoal\sattempt\sfrom\s
     (?P<nb_yards>\d+)                             # Number of Yards
     \s
     (?P<result>GOOD|MISSED)                       # Good or missed
    """, re.VERBOSE)

    pattern_fairCatch = re.compile(r"""
     fair\scatch\sby\s
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
    """, re.VERBOSE)
    pattern_touchback = re.compile(r"""
     touchback
    """, re.VERBOSE)

    pattern_safety = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
     \ssafety
    """, re.VERBOSE)

    pattern_fumble_forced = re.compile(r"""
     fumble\sforced\sby\s
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)            # Player forcing
    """, re.VERBOSE)
    pattern_fumble = re.compile(r"""
     fumble\sby\s
     (?P<player_fumbling>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)   # Player fumbling
     \srecovered\sby\s
     (?P<team_recovering>[A-Z]+)                           # Team recovering
     \s
     (?P<player_recovering>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+) # Player recovering
     \sat\s
     # Team Name Yard Line
     (?P<tnyl>[A-Z]+\d+)
    """, re.VERBOSE)

    patterns = (pattern_kickoff, pattern_return,
                pattern_tackle, pattern_extraPoint, pattern_rush_gain,
                pattern_rush_loss, pattern_rush_noGain, pattern_firstDown,
                pattern_pass_complete, pattern_pass_incomplete, pattern_run,
                pattern_sack, pattern_punt, pattern_fg, pattern_fairCatch,
                pattern_touchback, pattern_safety, pattern_fumble,
                pattern_fumble_forced)

    with open('./test_sentences.txt', 'r') as sentences_file:
        for sentence in sentences_file:
            if not ("no play" in sentence.casefold()):
                pass
            else:
                print("No play call, ignoring")
