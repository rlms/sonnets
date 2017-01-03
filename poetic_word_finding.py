# pylint: disable-all
import json
from collections import defaultdict

import nltk

import wiktionary_word_changer

def proportions(frequency_dict):
    """
    Return the proportion with which each word in a dict occurs.
    """
    total = sum(frequency_dict.values())
    result = {word: (count/total) for word, count in frequency_dict.items()}
    return result

with open("poem_word_frequencies.json") as f:
    poetry_counts = json.load(f)

poetry_props = proportions(poetry_counts)

tagged_words = defaultdict(set)
for (word, tag) in nltk.corpus.brown.tagged_words():
    if word.isalpha():
        tagged_words[word.lower()].add(tag)

brown = [word.lower() for word in nltk.corpus.brown.words() if word.isalpha()]
brown_counts = defaultdict(int)
for w in brown:
    brown_counts[w] += 1

brown_props = proportions(brown_counts)

ratios = {}
for w in poetry_props:
    if w in brown_props:
        ratios[w] = poetry_props[w] / brown_props[w]

sorted_ratios = [(w, r) for w, r in ratios.items()]
sorted_ratios.sort(key=lambda x: -x[1])

nouns = []
verbs = []
adjectives = []
adverbs = []
for (w, r) in sorted_ratios:
    if any(t.startswith("NN") for t in tagged_words[w]):
        nouns.append((w, r))
    elif any(t.startswith("VB") for t in tagged_words[w]):
        verbs.append((w, r))
    elif any(t.startswith("JJ") for t in tagged_words[w]):
        adjectives.append((w, r))
    elif any(t.startswith("RB") for t in tagged_words[w]):
        adverbs.append((w, r))

#with open("adjectives.json", "w") as f:
    #json.dump(adjectives, f)

#with open("adverbs.json", "w") as f:
    #json.dump(adverbs, f)

lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
nouns = [(lemmatizer.lemmatize(n), k) for n, k in nouns]
verbs = [(lemmatizer.lemmatize(v, "v"), k) for v, k in verbs]

verb_length = len(verbs)
present_participles = []
for index, (verb, ratio) in enumerate(verbs):
    if index % 10 == 0:
        print(100 * index/verb_length)
    try:
        present_participles.append((wiktionary_word_changer.conjugate(verb,
        "participle"), ratio))
    except ValueError:
        print("'{}' couldn't be conjugated".format(verb))

with open("present_participles.json", "w") as f:
    json.dump(present_participles, f)

raise SystemExit

past_verbs = []
for index, (verb, ratio) in enumerate(verbs):
    if index % 10 == 0:
        print(100 * index/verb_length)
    try:
        past_verbs.append((wiktionary_word_changer.conjugate(verb, 3, "past"), ratio))
    except ValueError:
        print("'{}' couldn't be conjugated".format(verb))

#with open("past_verbs.json", "w") as f:
    #json.dump(past_verbs, f)

print("Verbs done")

#noun_length = len(nouns)
#plural_nouns = []
#singular_nouns = []
#for index, (noun, ratio) in enumerate(nouns):
    #if index % 10 == 0:
        #print(100 * index/noun_length)
    #try:
        #plural_nouns.append((wiktionary_word_changer.plural(noun), ratio))
        #singular_nouns.append((noun, ratio))
    #except ValueError:
        #print("'{}' couldn't be pluralized.".format(noun))

#print("Nouns translated")
#with open("plural_nouns.json", "w") as f:
    #json.dump(plural_nouns, f)

#with open("singular_nouns.json", "w") as f:
    #json.dump(singular_nouns, f)

