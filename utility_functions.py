def strip_punctuation(string):
    return "".join(c for c in string if c not in "!\"*`£$;:,.?/&()-_+=[{]}\~")
