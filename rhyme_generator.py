# pylint: disable-all
print("Importing NLTK")
import nltk
from nltk.corpus import brown
print("Done!")

class NotInCMUDict(Exception):
    """
    Exception raised when a word isn't found in the CMUDict
    """
    pass

print("Getting CMUDict")
ENTRIES = nltk.corpus.cmudict.entries()
DICT = nltk.corpus.cmudict.dict()
DICT["springbok"] = [["S", "P", "R", "IH1", "NG", "B", "AA1", "K"]]
print("Done!")

def brown_cmudict():
    """
    Return a version of CMUDict
    that only contains words in the Brown corpus.
    """
    print("Getting updated CMUDict")
    new_dict = {}
    for word in brown.words():
        lowercase = word.lower()
        if lowercase in DICT:
            new_dict[lowercase] = DICT[lowercase]

    print("Done!")
    return new_dict

def most_stressed(word):
    """
    Determine the most stressed syllable in a word (0, 1 or 2).
    """
    syllableses = DICT.get(word)
    if syllableses is None:
        raise NotInCMUDict("'{}' not in the CMUDict".format(word))

    syllables = syllableses[0]

    for x in ("1", "2", "0"):
        for s in syllables:
            if s.endswith(x):
                return x

    return False


def after_last_stressed(word):
    """
    Return the syllables of a word after the ultimate stressed syllable.
    The stressed syllable is included.
    """
    syllableses = DICT.get(word)
    if syllableses is None:
        raise NotInCMUDict("'{}' not in the CMUDict".format(word))

    syllables = syllableses[0]

    max_stress = most_stressed(word)
    if not max_stress:
        raise ValueError("'{}' has no stressed syllables".format(word))

    index = None
    for i, s in enumerate(reversed(syllables)):
        if s.endswith(max_stress):
            index = i
            break

    if index is None:
        raise ValueError("'{}' has no stressed syllables".format(word))

    new_index = (-1 * index) - 1

    return syllables[new_index:]

def is_rhyme(first, second):
    end1 = after_last_stressed(first)
    end2 = after_last_stressed(second)

    return (end1 == end2) and (not first.endswith(second)) and (not second.endswith(first))

def all_rhymes(word):
    for index, w in enumerate(DICT.keys()):
        if w != word:
            try:
                if is_rhyme(w, word):
                    yield w
            except ValueError:
                pass

if __name__ == "__main__":
    rs = all_rhymes("toast")
    print(list(rs))
