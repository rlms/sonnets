"""
Analyze the sentence structures in Shakespearean sonnets
"""
from collections import Counter

import nltk
from utility_functions import strip_punctuation

def lines():
    """
    Yield all the lines in Shakespearean sonnets.
    """
    with open("shakesonnets.txt") as f:
        text = f.read()

    sonnets = text.split("\n\n")
    lines = []

    for s in sonnets:
        for line in s.split("\n"):
            if line:
                lines.append([strip_punctuation(word.lower())
                              for word in line.split(" ")])

    return lines

if __name__ == "__main__":
    line_structures = Counter()

    for line in lines():
        print(line)
        tags = tuple(tag[1] for tag in nltk.pos_tag(line))
        print(tags)
        command = input(": ").strip().lower()
        if command == "y":
            line_structures[tags] += 1
        elif command.startswith("c"):
            correct = input("Enter correct tags: ")
            tags = tuple(correct.split())
            line_structures[tags] += 1
        print()

    output = "\n".join(" ".join(k) for k in line_structures.keys())
    with open("sentence_structures.txt", "w") as f:
        f.write(output)
