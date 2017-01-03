import nltk

print("Generating stuff")
DICT = nltk.corpus.cmudict.dict()
BROWN_WORDS = nltk.corpus.brown.tagged_words()

transitive = set()

length = len(BROWN_WORDS)
for index, (word, tag) in enumerate(BROWN_WORDS):
    if index % 1000 == 0:
        print(index, "/", length)
    if word in DICT:
        if tag in ("VBD", "VBN"):
            next_tag = BROWN_WORDS[index+1][1]
            if next_tag.startswith("DT"):
                transitive.add(word)

with open("trans.txt", "w") as f:
    f.write("\n".join(transitive))
