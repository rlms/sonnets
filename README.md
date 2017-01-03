Sonnet generator
================

This repository contains some code to automatically generate sonnets (and some
related code to do various other things). One of the sonnets it has written:

incessantly inhabited the kite

the dumb mumbles remembered thereabouts

furtively fell the flammable delight

i lopped the unimaginable shouts

the goddess is like the northeastern pan

the wildest eucalyptus caved afloat

they bounded the unfathomable clan

the yellowish despair is like the goat

the jagged window diminished anymore

and infinitely overwhelmed and bowed

fitfully scattered the obsessive drawer

he camped the unimaginable crowd

the squeaky filament is like the rain

as discontented as the meaty reign

Running the program
-------------------
If you want to run the program yourself, the requirements are Python 3 and NLTK.
Before running it, you need to use `nltk.download()` in Python to download some
corpora. I think the required corpora are the Treebank corpus and CMUDict, but
there might be others I've forgotten. After doing that `python
sentence_generator.py` will generate 10 sonnets (I can't guarantee they'll be
good though). Generally it takes about 10 minutes to make each sonnet.

How it works
------------

The final program consists of several pieces bolted together in a haphazard
fashion. The key parts are the system that fills in line schemes made of word
types (adjective, noun etc.) with specific words to make a possible line; the
system that determines whether a possible a line has the correct length, metre,
and rhyme scheme; and the system that ensures only objectively poetic vocabulary
is used.
