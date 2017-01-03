"""
Analyze the sentence structures in the Treebank corpus
"""
from collections import Counter
from itertools import groupby

import nltk

sentences = nltk.corpus.treebank.tagged_sents()
new = []
print(len(sentences))
for s in sentences:
    temp = []
    for w in s:
        if len(w[1]) > 1:
            temp.append(w[1])
    new.append(temp)

sentences = [s for s in new if 4 <= len(s) <= 10]
sentences = [s for s in sentences if not "''" in s]
sentences = [s for s in sentences if not "``" in s]
sentences = [s for s in sentences if not "-NONE-" in s]
sentences = [s for s in sentences if not "-LRB-" in s]
sentences = [s for s in sentences if not "-RRB-" in s]

print(len(sentences))

with open("treebank_structures.txt", "w") as f:
    f.write("\n".join(" ".join(s) for s in sentences))


