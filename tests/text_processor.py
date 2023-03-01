import re

if __name__ == '__main__':
    keywords = ('kickoff', 'rush', 'return', 'sacked', 'punt', 'pass',
                '1st down', 'touchdown', 'field goal attempt', 'fair catch',
                'kick attempt', 'rush attempt', 'recovered', 'no play',
                'touchback')

    # extract all patterns from the sentence
    pattern_kickoff = re.compile(
     r"[A-Z]\.[A-Za-z\-]+ kickoff \d+ yard(s)* to the [A-Z]+\d+")
    pattern_return = re.compile(
     r"[A-Z]\.[A-Za-z\-]+ return \d+ yard(s)* to the [A-Z]+\d+")
    pattern_tackle = re.compile(
     r"(?<=(\(|\;))[A-Z]\.[A-Za-z\-]+(?=(\)|\;))")
    # player pattern preceded by ( or ; and followed by ) or ;
    pattern_extraPoint = re.compile(
     r"[A-Z]\.[A-Za-z\-]+ (kick|rush) attempt (good|failed)")
    # rush
    # r"[A-Z]\.[A-Za-z\-]+ rush .*for (((loss of )*\d+ yard(s)*)|(no gain)) to the [A-Z]+\d+"
    pattern_rush_gain = re.compile(
     r"[A-Z]\.[A-Za-z\-]+ rush.*for \d+ yard(s)* to the [A-Z]+\d+")
    pattern_rush_noGain = re.compile(
     r"[A-Z]\.[A-Za-z\-]+ rush.*for no gain to the [A-Z]+\d+")
    pattern_rush_loss = re.compile(
     r"[A-Z]\.[A-Za-z\-]+ rush.*for loss of \d+ yard(s)* to the [A-Z]+\d+")

    pattern_firstDown = re.compile(
     r"1ST DOWN")
    pattern_pass_complete = re.compile(
     r"[A-Z]\.[A-Za-z\-]+.*pass complete to [A-Z]\.[A-Za-z\-]+ for \d+ yard(s)* to the [A-Z]+\d+")
    pattern_pass_incomplete = re.compile(
     r"[A-Z]\.[A-Za-z\-]+.*pass incomplete( to [A-Z]\.[A-Za-z\-]+)*")

    pattern_sack = re.compile(
     r"[A-Z]\.[A-Za-z\-]+ sacked for loss of \d+ yard(s)* to the [A-Z]+\d+")
    pattern_punt = re.compile(
     r"")
    pattern_fg = re.compile(
     r"[A-Z]\.[A-Za-z\-]+ field goal attempt from \d+ (GOOD|MISSED)")
    pattern_recovered = re.compile(
     r"")
    pattern_fairCatch = re.compile(
     r"")
    pattern_safety = re.compile(
     r"")

    with open('./test_sentences.txt', 'r') as sentences_file:
        sentences = sentences_file.readlines()
        for sentence in sentences:
            if not ("no play" in sentence):
                pass
            else:
                print("No play call, ignoring")
