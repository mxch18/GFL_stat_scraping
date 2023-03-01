import re

if __name__ == '__main__':
    keywords = ('kickoff', 'rush', 'return', 'sacked', 'punt', 'pass',
                '1st down', 'touchdown', 'field goal attempt', 'fair catch',
                'kick attempt', 'rush attempt', 'recovered', 'no play',
                'touchback')

    # extract all patterns from the sentence
    kickoff_pattern = re.compile(
     r"[A-Z]\.[A-Za-z\-]+\skickoff\s\d+\syard(s)*\sto\sthe\s[A-Z]+\d+")
    return_pattern = re.compile(
     r"[A-Z]\.[A-Za-z\-]+\sreturn\s\d+\syard(s)*\sto\sthe\s[A-Z]+\d+")
    tackle_pattern = re.compile(
     r"(?<=(\(|\;))[A-Z]\.[A-Za-z\-]+(?=(\)|\;))")
    # player pattern preceded by ( or ; and followed by ) or ;
    extraPoint_pattern = re.compile(
     r"[A-Z]\.[A-Za-z\-]+\s(kick|rush)\sattempt\s(good|failed)")
    rush_pattern = re.compile(
     r"[A-Z]\.[A-Za-z\-]+\srush\s.*for\s(((loss\sof\s)*\d+\syard(s)*)|(no\sgain))\sto\sthe\s[A-Z]+\d+")

    with open('./test_sentences.txt', 'r') as sentences_file:
        sentences = sentences_file.readlines()
        for sentence in sentences:
            if not ("no play" in sentence):
                pass
            else:
                print("No play call, ignoring")
