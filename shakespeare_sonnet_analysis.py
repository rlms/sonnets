from collections import Counter

import nltk

from sentence_generator import stress_pattern
from utility_functions import strip_punctuation

if __name__ == "__main__":
    counts = [Counter() for syl in range(10)]

    with open("shakesonnets.txt") as f:
        text = f.read()

    sonnets = text.split("\n\n")
    for s in sonnets:
        lines = [[strip_punctuation(word.lower())
                  for word in line.split(" ")]
                  for line in s.split("\n")]

        if len(lines) == 15:
            lines = lines[1:]    # remove empty string at start

        if len(lines) != 14:
            print("Wrong length sonnet {}".format(len(lines)))
            continue

        for line in lines:
            pattern = stress_pattern(line)
            if not pattern:    # unknown word
                continue

            for syllable_index, value in enumerate(pattern):
                try:
                    counts[syllable_index][value] += 1
                except IndexError:
                    print("Wrong number of syllables on line '{}'".format(line))
                    break

    for number, syllable in enumerate(counts):
        print(number)
        print(syllable)
        print()
    print()
