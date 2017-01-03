# pylint: disable-all
import glob
import json
import codecs
from string import ascii_uppercase, ascii_lowercase, digits
from collections import defaultdict

valid = ascii_uppercase + ascii_lowercase + digits + " \n\t'"

if __name__ == "__main__":
    words = defaultdict(int)
    for index, path in enumerate(glob.glob("scraped_poems/*.txt")):
        if index % 100 == 0:
            print(index)
            with open("poem_frequencies.json", "w") as f:
                json.dump(words, f)
        with codecs.open(path, "r", "utf-8") as f:
            text = f.read()
        new = []
        for c in text:
            if c in valid:
                new.append(c)
        text = "".join(new)
        poem_words = text.lower().split()
        for w in poem_words:
            words[w] += 1

    with open("poem_frequencies.json", "w") as f:
        json.dump(words, f)
