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
        type_of_action = []
        sentence_lower = sentence.tolower()
        for word in keywords:
            if word in sentence:
                type_of_action.append(word)

        if not ("no play" in type_of_action):
            if "kickoff" in kickoff_str:
                # look for as many characters A-Z, a-z, - or . preceding " kickoff "
                player = re.search(
                    r"[A-Za-z\-\.]+(?=\skickoff\s)", kickoff_str)
                # look for as many digit character following " kickoff "
                yards = re.search(r"(?<=\skickoff\s)\d+", kickoff_str)
                # next landmark
                teamName_ydLine = re.search(r"[A-Z]+\d+", kickoff_str)[0]
                # slice the string
                kickoff_str = kickoff_str[teamName_ydLine.end():]
                # check for out-of-bounds (not truly necessary as case is covered
                # by NO PLAY)
                if "out-of-bounds" in kickoff_str:
                    print("Unknown case: out-of-bounds kickoff that is not NO PLAY")
                # ignore on-side kick
                on_side = kickoff_str.find("on-side kick")
                if on_side != -1:
                    kickoff_str = kickoff_str[on_side + len("on-side kick"):]
                # pass it down

                else:
                    print("No play call, ignoring")
