from nltk.corpus import cmudict

getter = cmudict.dict()

def syllables(word):
    print("!!!!!", word)
    try:
        syls = getter["".join(i for i in word.lower() if i not in ".,;:()!?")][0]
    except KeyError:
        return word
    new = []
    for syl in syls:
        for n in "012":
            print(syl, n)
            if n in syl:
                new.append(n)

    print(new)
    return "".join(new)

def analyse(poem):
    lines = poem.splitlines()
    new_lines = []
    for line in lines:
        temp = []
        for word in line.split():
            temp.append(syllables(word))
        new_lines.append(" ".join(temp))

    return "\n".join(new_lines)

def main():
    with open("s18.txt") as f:
        print(analyse(f.read()))
    input()
    
if __name__ == '__main__':
    main()
