from itertools import chain

from nltk.corpus import wordnet

def get_synset(word):
    return wordnet.synsets(word)[0]

def synset_name(synset):
    return synset.lemma_names()[0].replace("_", " ")

def cousins(word, level):
    """
    Go up `level` hypernyms from `word`, and down again.
    """
    parents = [get_synset(word)]
    for _ in range(level):
        parent_hypernyms = [parent.hypernyms() for parent in parents]
        parents = list(chain(*parent_hypernyms))

    children = parents
    for _ in range(level):
        children_hyponyms = [child.hyponyms() for child in children]
        children = list(chain(*children_hyponyms))

    children = set(children)
    children -= {get_synset(word)}
    return set(map(synset_name, children))


if __name__ == "__main__":
    print(cousins("wolf", 1))
    input()
    print(cousins("rose", 2))
    input()
    print(cousins("mountain", 1))
    input()
    print(cousins("mountain", 2))
    input()
    print(cousins("mountain", 3))
    input()

