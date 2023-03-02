import re

if __name__ == '__main__':
    keywords = ('kickoff', 'rush', 'return', 'sacked', 'punt', 'pass',
                '1st down', 'touchdown', 'field goal attempt', 'fair catch',
                'kick attempt', 'rush attempt', 'recovered', 'no play',
                'touchback')

    # extract all patterns from the sentence
    pattern_kickoff = re.compile(r"""
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)    # Player name
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

    pattern_tackle = re.compile(
     r"(?<=(\(|\;))[[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+(?=(\)|\;))")
    # player pattern preceded by ( or ; and followed by ) or ;

    pattern_extraPoint = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+ (kick|rush) attempt (good|failed)")

    # rush
    # r"[A-Z]\.[A-Za-z\-]+ rush .*for (((loss of )*\d+ yard(s)*)|(no gain)) to the [A-Z]+\d+"
    pattern_rush_gain = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+ rush.*for \d+ yard(s)* to the [A-Z]+\d+")
    pattern_rush_noGain = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+ rush.*for no gain to the [A-Z]+\d+")
    pattern_rush_loss = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+ rush.*for loss of \d+ yard(s)* to the [A-Z]+\d+")

    pattern_firstDown = re.compile(
     r"1ST DOWN")

    pattern_pass_complete = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+.*pass complete to [A-Z]\.[A-Za-z\-]+ for \d+ yard(s)* to the [A-Z]+\d+")
    pattern_pass_incomplete = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+.*pass incomplete( to [A-Z]\.[A-Za-z\-]+)*")

    pattern_run = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+ for \d+ yard(s)*"
    )

    pattern_sack = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+ sacked for loss of \d+ yard(s)* to the [A-Z]+\d+")

    pattern_punt = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+ punt \d+ yard(s)* to the [A-Z]+\d+")

    pattern_fg = re.compile(
     r"[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+ field goal attempt from \d+ (GOOD|MISSED)")

    pattern_fairCatch = re.compile(
     r"")

    pattern_safety = re.compile(
     r"")

    pattern_fumble_forced = re.compile(r"""
     fumble\sforced\sby\s
     (?P<player>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)
    """, re.VERBOSE)
    pattern_fumble = re.compile(r"""
     fumble\sby\s
     (?P<player_fumbling>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+)   # Player fumbling
     \srecovered\sby\s
     (?P<team_recovering>[A-Z]+)                            # Team recovering
     \s
     (?P<player_recovering>[A-Z]\.([a-z]\.)?[A-Z][a-z\-]+) # Player recovering
     \sat\s
     (?P<tnyl>[A-Z]+\d+)                                   # Team Name Yard Line
    """, re.VERBOSE)

    with open('./test_sentences.txt', 'r') as sentences_file:
        sentences = sentences_file.readlines()
        for sentence in sentences:
            if not ("no play" in sentence):
                pass
            else:
                print("No play call, ignoring")
