# pylint: disable-all
import random
import itertools
import json
from copy import deepcopy
from collections import defaultdict

import nltk

from rhyme_generator import DICT, all_rhymes
from grammar_generator import generate_sentence, parse_tag

with open("singular_nouns.json") as f:
    NN = json.load(f)

with open("plural_nouns.json") as f:
    NNS = json.load(f)

with open("adjectives.json") as f:
    JJ = json.load(f)

with open("adverbs.json") as f:
    RB = json.load(f)

with open("past_verbs.json") as f:
    VBD = json.load(f)

with open("present_participles.json") as f:
    VBG = json.load(f)

def filter_unpoetic_words(word_ratio_pairs, lower_limit):
    """
    Filter a list of (word, poetry_ratio) pairs to a list of words with a
    poetry_ratio >= lower_limit that are also in CMUDict.
    """
    return set([w for (w, k) in word_ratio_pairs if k >= lower_limit and w in DICT])

NN = filter_unpoetic_words(NN, 2)
NNS = filter_unpoetic_words(NNS, 2)
JJ = filter_unpoetic_words(JJ, 2)
RB = filter_unpoetic_words(RB, 2)
# filter adverbs like "yea", "aye", "yon" etc.
RB = set([w for w in RB if len(w) > 3])
VBD = filter_unpoetic_words(VBD, 2)
VBG = filter_unpoetic_words(VBG, 2)

ALL_WORDS = NN | NNS | JJ | RB | VBD | {"the"}

PARTS_OF_SPEECH_POETIC = {"NN": NN, "NNS": NNS, "JJ": JJ, "RB": RB, "VBD": VBD, "VBG": VBG,
        "DTT": {"the"}, "DTS": {"the", "some"}, "CD": {"seven", "two", "five", "thirteen", "twelve"}}

def make_parts_of_speech_dictionary(structures):
    poss = set()
    for line in structures:
        for pos in line:
            poss.add(pos)

    parts_of_speech = {p: set() for p in poss}

    print("Making Treebank corpus set")
    words = set([(w, t) for w, t in nltk.corpus.treebank.tagged_words()])

    print("Making NPS chat corpus set")
    words |= set([(w, t) for w, t in nltk.corpus.nps_chat.tagged_words()])

    print("Making parts of speech dictionary")
    for index, (word, tag) in enumerate(words):
        if word in DICT:
            if tag in poss:
                parts_of_speech[tag].add(word)

    return parts_of_speech


with open("custom_structures.txt") as f:
    structures = f.read().split("\n")
    structures = [s for s in structures if not s.startswith("#")]
    STRUCTURES = [line.split(" ") for line in structures if line]

# build a dictionary of structures
# with final POS in each structure as keys
STRUCTURE_DICT = defaultdict(list)
for structure in STRUCTURES:
    STRUCTURE_DICT[structure[-1]].append(structure)

def word_of_kind(part_of_speech):
    print(part_of_speech)
    words = PARTS_OF_SPEECH_POETIC[part_of_speech]
    words = list(words)
    random.shuffle(words)
    return words[0]

def translate_parts_of_speech(parts_of_speech):
    return [word_of_kind(pos) for pos in PARTS_OF_SPEECH_POETIC]

def partitions(n):
    """
    Return the different ways integers can be summed to produce a number.
    Code taken from here:

        http://jeromekelleher.net/partitions.php
    """
    a = [0 for i in range(n + 1)]
    k = 1
    a[1] = n
    while k != 0:
        x = a[k - 1] + 1
        y = a[k] - 1
        k -= 1
        while x <= y:
            a[k] = x
            y -= x
            k += 1
        a[k] = x + y
        yield a[:k + 1]

def partition_permutations(n):
    return set(itertools.chain.from_iterable(map(itertools.permutations, partitions(n))))

print("Generating partitions of 10")
TEN_PARTITIONS = partition_permutations(10)

def word_length(word):
    """
    Return the number of syllables in a word.
    """
    return len([s for s in DICT[word][0] if s[-1] in ("0", "1", "2")])

def lengths(incomplete_line, cache={}):
    """
    Return the number of syllables in each word in a line.
    """
    if tuple(incomplete_line) in cache:
        return cache[tuple(incomplete_line)]

    result = []
    for w in incomplete_line:
        if w.isupper():
            result.append(w)
        else:
            result.append(word_length(w))
    cache[tuple(incomplete_line)] = result
    return result

def generate_syllable_patterns(pattern):
    """
    Generate the possible syllable patterns for a POS pattern.
    """
    possible_syl_patterns = [p for p in TEN_PARTITIONS if len(p) == len(pattern)]
    syl_patterns = []
    pattern_lengths = lengths(pattern)
    for p in possible_syl_patterns:
        for word_len, n in zip(pattern_lengths, p):
            if isinstance(word_len, int):
                if word_len != n:
                    break
        else:
            syl_patterns.append(p)

    return syl_patterns

def generate_line(syllable_patterns, pattern, parts_of_speech):
    """
    Generate a line of 10 syllables.
    """
    for p in syllable_patterns:
        result = []
        for pos, n in zip(pattern, p):
            if pos.isupper():
                words = parts_of_speech[pos] & set(words_of_length(n))
                if not words:
                    break
                result.append(random.choice(list(words)))
            else:
                result.append(pos)
        else:
            return result

    return False


def get_sentence_length(sentence):
    """
    Return the number of syllables in a list of words.
    """
    return sum(map(word_length, sentence))

def words_of_length(length):
    """
    Yield all words with a certain number of syllables.
    """
    for word in ALL_WORDS:
        if word_length(word) == length:
            yield word

def sentence_pattern(pattern):
    """
    Return a sentence with words with specific numbers of syllables.
    """
    result = []
    for n in pattern:
        possible = list(words_of_length(n))
        result.append(random.choice(possible))

    return result

def random_sentence(length, max_word_length=5, min_word_length=1):
    ps = list(x for x in partition_permutations(length)
                if max(x) <= max_word_length and
                   min(x) >= min_word_length)
    p = random.choice(ps)
    return sentence_pattern(p)

def random_rhyme_of_length(word, length):
    possible = all_rhymes(word)
    possible = [w for w in possible if word_length(w) == length]
    try:
        return random.choice(possible)
    except IndexError:
        return None

def stress_pattern(word_list):
    result = []
    for word in word_list:
        syllables = DICT.get(word)
        if syllables is None:
            return False
        syllables = syllables[0]
        for s in syllables:
            for c in "012":
                if s.endswith(c):
                    result.append(c)

    return result

def iambicness(word_list):
    """
    Return representing how closely a line matches iambic pentameter.
    Higher values are better.
    """
    pattern = stress_pattern(word_list)
    result = 0

    # first syllable is often strong
    # so don't take it into account

    for index in range(2, 9, 2):
        if pattern[index] == "0":
            result += 0.6
        elif pattern[index] == "1":
            result += 0.4
        # ignore "2" meaning secondary stress

    for index in range(1, 10, 2):
        if pattern[index] == "0":
            result += 0.1
        elif pattern[index] == "2":
            result += 0.4
        elif pattern[index] == "1":
            result += 0.9

    return result


def line_structure():
    """
    Generate the POS structure of a line.
    """
    return random.choice(STRUCTURES)

def rhyming_pos(first_word, part_of_speech):
    """
    Get a word of a certain part of speech that rhymes with something.
    """
    # find words that rhyme with the first word
    # and are of the right kind of speech
    rhymes = set(all_rhymes(first_word))
    speech = PARTS_OF_SPEECH_POETIC[part_of_speech]

    both = rhymes & speech

    # if there are some, pick a random one
    if both:
        second_word = random.choice(tuple(both))
        return second_word
    else:
        return False


def find_rhyme(first_word):
    """
    Find a word that rhymes with one word and is part of a second list of
    structures.
    """
    # try each structure for the second line
    length = len(STRUCTURE_DICT)
    for index, ultimate_pos in enumerate(STRUCTURE_DICT):
        second_structure = random.choice(STRUCTURE_DICT[ultimate_pos])
        print(index+1, "/", length)
        second_part = second_structure[-1]
        parsed = parse_tag(second_part)
        pos = parsed["pos"]
        word = rhyming_pos(first_word, pos)
        if word:
            return word, second_structure
    return False

def get_rhyme_pair(first_part_of_speech):
    """
    Find a pair of words that rhyme.
    """
    speech_parts = PARTS_OF_SPEECH_POETIC

    # randomise search order
    words = list(deepcopy(speech_parts[first_part_of_speech]))
    random.shuffle(words)
    # iterate through possible first_words to find one that works
    for first_word in words:
        print(1, first_word)
        result = find_rhyme(first_word)
        if result:
            second_word, second_structure = result
            return (first_word, second_word), second_structure

    # else no rhyming words in any structure in `second_line_structures`
    return False


def get_pair_and_structures(ultimate_pos_list):
    # try each structure for the first line in turn
    for ultimate_pos in ultimate_pos_list:
        first_structure = random.choice(STRUCTURE_DICT[ultimate_pos])
        # get last part of speech in the line
        first_part = first_structure[-1]
        parsed = parse_tag(first_part)
        pos = parsed["pos"]
        result = get_rhyme_pair(pos)
        if result:
            pair, second_structure = result
            print(0, pair)
            return pair, (first_structure, second_structure)

    return False

def make_line(final_word, structure, max_tries=500):
    counter = 0
    pattern = structure[:-1] + [final_word]
    syllable_patterns = generate_syllable_patterns(pattern)
    print("Trying to make line")
    while counter < max_tries:
        random.shuffle(syllable_patterns)
        line = generate_line(syllable_patterns, pattern, PARTS_OF_SPEECH_POETIC)
        if not line:
            counter += 1
            continue
        if iambicness(line) > 5.2:
            return line
        counter += 1
    return False

def get_rhyming_line(number):
    """
    Return the line that rhymes with a certain line.
    """
    if number in (0, 1, 4, 5, 8, 9):
        return number + 2
    elif number in (2, 3, 6, 7, 10, 11):
        return number - 2
    elif number == 12:
        return 13
    elif number == 13:
        return 12

def get_pair_of_lines():
    ultimate_pos_list = list(STRUCTURE_DICT.keys())
    random.shuffle(ultimate_pos_list)
    pair_and_structures = get_pair_and_structures(ultimate_pos_list)
    return pair_and_structures


def new_sonnet():
    """
    Generate a new sonnet.
    """
    rhyming_lines = [(0, 2), (1, 3),
                     (4, 6), (5, 7),
                     (8, 10), (9, 11),
                     (12, 13)]

    # working list of lines
    last_words = [None for _ in range(14)]
    line_structures = [None for _ in range(14)]

    lines = [None for _ in range(14)]

    for i in range(14):
        print("Line #{}".format(i))
        line = last_words[i]
        if line:
            line = make_line(last_words[i], line_structures[i])
        while not line:
            pair, structures = get_pair_of_lines()
            matching_line = get_rhyming_line(i)
            last_words[i] = pair[0]
            last_words[matching_line] = pair[1]
            line_structures[i] = structures[0]
            line_structures[matching_line] = structures[1]
            line = make_line(last_words[i], line_structures[i])
            other_line = make_line(last_words[matching_line],
                                   line_structures[matching_line])
            if not other_line:
                line = False
                continue

        lines[i] = line
        lines[matching_line] = other_line

    for i in range(14):
        print(line_structures[i])
        print(iambicness(lines[i]))
        print(" ".join(lines[i]))


if __name__ == "__main__":
    for _ in range(10):
        new_sonnet()
        input()
