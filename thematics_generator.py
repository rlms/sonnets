from itertools import chain

from nltk.corpus import wordnet as wn
from nltk.corpus import brown

from rhyme_generator import DICT

BROWN_WORDS = brown.words()

def check_brown_words(words):
    """
    Return a set of words that are in the Brown corpus.
    """
    result = set()
    for w in BROWN_WORDS:
        if w in words:
            result.add(w)

    return result


def name(synset):
    """
    Return the English for a synset.
    """
    return synset.lemma_names()[0].replace("_", " ")

def in_cmudict(name):
    """
    If a name or the last word in it is in CMUDict,
    return the relevant part.
    """
    possible = name.split()[-1]
    if possible in DICT:
        return possible

def last_children(synset):
    """
    Find the eventual hyponyms of a synset.
    """
    children = synset.hyponyms()
    old_children = None
    while children != old_children:
        old_children = children
        new_children = []
        for c in children:
            hypos = c.hyponyms()
            if hypos:
                new_children.extend(hypos)
            else:
                new_children.append(c)
        children = new_children

    return children

def theme_words(synset):
    """
    Get words related to a synset.
    """
    result = set()
    for index, c in enumerate(last_children(synset)):
        dict_name = in_cmudict(name(c))
        if dict_name:
            result.add(dict_name.lower())

    result = check_brown_words(result)
    return result

FRUIT = wn.synset("fruit.n.01")
BIRD = wn.synset("bird.n.01")
EMOTION = wn.synset("emotion.n.01")

if __name__ == "__main__":
    print("Getting themes")
    print("Getting birds")
    BIRDS = theme_words(BIRD)
    print("Getting fruits")
    FRUITS = theme_words(FRUIT)
    print("Getting emotions")
    EMOTIONS = theme_words(EMOTION)

    for name, words in zip(["birds", "fruits", "emotions"],
                           [BIRDS, FRUITS, EMOTIONS]):
        with open("{}.txt".format(name), "w") as f:
            f.write("\n".join(words))
    print("Done!")
