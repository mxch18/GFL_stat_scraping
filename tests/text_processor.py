import re

if __name__ == '__main__':
    keywords = ('kickoff', 'rush', 'return', 'sacked', 'punt', 'pass',
                '1st down', 'touchdown', 'field goal attempt', 'fair catch',
                'kick attempt', 'rush attempt', 'recovered', 'no play',
                'touchback')

    kickoff_1 = "M.Achiepi kickoff 54 yards to the PR11, out-of-bounds, PENALTY DP Free Kick out of bounds (M.Achiepi) 5 yards to the DP30, NO PLAY."
    kickoff_2 = "M.Achiepi kickoff 61 yards to the PR9, B.Polk return 91 yards to the DP0, TOUCHDOWN, clock 00:00."
    kickoff_3 = "D.Schumacher kickoff 58 yards to the DP7, N.Lawrence return 14 yards to the DP21 (F.Fort;S.Alvarez)."
    kickoff_4 = "N.Merrikh kickoff 2 yards to the PR37, on-side kick, recovered by SHU J.Haas on PR37, J.Haas return 37 yards to the PR0, TOUCHDOWN, clock 06:50, PENALTY PR Offside Free Kick declined."

    kickoff_str = (kickoff_1, kickoff_2, kickoff_3, kickoff_4)

    for sentence in kickoff_str:
        if not ("no play" in sentence):
            # extract all patterns from the sentence
            kickoff_pattern = re.compile(
             r"[A-Z]\.[A-Za-z\-]+(\skickoff\s)\d+(\syards\sto\sthe\s)[A-Z]+\d+")
            return_pattern = re.compile(
             r"[A-Z]\.[A-Za-z\-]+(\sreturn\s)\d+(\syards\sto\sthe\s)[A-Z]+\d+")
            tackle_pattern = re.compile(
             r"(?<=(\(|\;))[A-Z]\.[A-Za-z\-]+(?=(\)|\;))")
            # player pattern preceded by ( or ; and followed by ) or ;
            extraPoint_pattern = re.compile(
             r"[A-Z]\.[A-Za-z\-]+\s(kick\sattempt|rush\sattempt)\s(good|failed)")

        else:
            print("No play call, ignoring")
