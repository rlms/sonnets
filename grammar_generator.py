# pylint: disable-all
import random
from collections import defaultdict

import nltk

from rhyme_generator import DICT

# Format of custom POS tags:
# tag;theme
# where `tag` is an ordinary tag,
# and `theme` is a number representing a theme
# If provided, `theme` is used to index
# the `generate_sentence` function's `themes` argument

# Extensions to the Upenn tagging system:
# DTT: determiner, single
# DTS: determiner, plural

pos_list = ["$", "(", ")", ",", "--", ".", ":",
            "CC", "CD", "EX", "IN",
            "JJ", "JJR", "JJS", "LS", "MD",
            "NN", "NNP", "NNPS", "NNS",
            "PDT", "POS", "PRP", "PRP$",
            "RB", "RBR", "RBS", "RP", "TO",
            "VB", "VBD", "VBG", "VBN", "VBP", "VBZ",
            "WDT", "WP", "WP$", "WRB"]

custom_pos = ["DTT", "DTS",]

parts_of_speech = defaultdict(set)
parts_of_speech["DTT"] = {
                         "this", "either", "any", "another", "the", "every",
                         "neither", "each", "that", "a",
                         }

parts_of_speech["DTS"] = {
                         "those", "these", "any", "no", "the", "both", "all",
                         "some",
                         }

print("Getting tagged words from Treebank corpus")
for word, tag in nltk.corpus.treebank.tagged_words():
    if tag in pos_list:
        if word in DICT:
            parts_of_speech[tag].add(word)

for k in parts_of_speech:
    print(k, len(parts_of_speech[k]))

print("Adjusting verbs")
with open("trans.txt") as f:
    verbs = set(f.read().splitlines())
    parts_of_speech["VBD"] = verbs


def correct_a(noun):
    """
    Determine if "a" or "an" is the appropriate article for a noun.
    """
    if noun[0] in "aeiou":
        return "an"
    else:
        return "a"

def parse_tag(tag):
    parts = tag.split(";")
    pos = parts[0]
    if len(parts) >= 2:
        theme = int(parts[1])
    else:
        theme = None

    return {"pos": pos, "theme": theme,}

def generate_sentence(sentence, parts_of_speech, themes=None):
    """
    Replace a list of POS tags with words.
    """
    result = []
    for tag in sentence:
        parsed = parse_tag(tag)
        pos = parsed["pos"]
        theme = parsed["theme"]

        if theme is None:
            possible = parts_of_speech
        else:
            possible = themes[theme]

        if pos in possible:
            word = random.choice(list(possible[pos]))
            result.append(word)
        else:
            # a word by itself
            result.append(pos)

    for index, word in enumerate(result):
        if word == "a":
            if not index+2 == len(result):
                result[index] = correct_a(result[index+1])

    return result


if __name__ == "__main__":
    with open("custom_structures.txt") as f:
        structures = f.read().splitlines()

    structures = [line.split() for line in structures]
    for _ in range(5):
        for line in structures:
            print(line)
            print(generate_sentence(line))
            input()

        input()

