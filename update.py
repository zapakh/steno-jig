#!/usr/bin/python3

# Update steno-jig dictionary and whatnot according to whatever is
# currently on ~/ploverdict.

import json

IDONTKNOW_PATH = '../ploverdict/idontknow.json'
IDONTKNOW_OUTPUT_PATH = 'idk-translations.js'

INPUT_PATHS = ['../ploverdict/main.json',
#              '../ploverdict/contractions.json',
#              '../ploverdict/the_prefix.json',   # numbers are confusing...
               '../ploverdict/punctuation.json',
               '../ploverdict/user.json', ]

OUTPUT_PATH = 'extra-translations.js'

def make_out(single_words=True):
    OUT = {}
    for (chord, text) in DICT.items():
        text = text.replace('{.}', '.').replace('{,}', ',') \
                   .replace('{?}', '?').replace('{!}', '!')
        if not single_words and " " not in text:
            continue
        if text in OUT:
            if len([c for c in OUT[text] if c == '/']) < \
                      len([c for c in chord if c == '/']):
                continue
            if len(OUT[text]) < len(chord):
                continue
            if len(OUT[text]) == len(chord) and \
                    ('*' in chord or '*' not in OUT[text]):
                continue
        OUT[text] = chord
    return OUT

with open(IDONTKNOW_PATH) as f:
    DICT = json.load(f)

# Don't add hints for single words in idontknow theory, because some
# of those chords are pretty ridiculous.
OUT = make_out(single_words=False)

outfile = open(IDONTKNOW_OUTPUT_PATH, 'w')
outfile.write("Object.assign(TypeJig.Translations.Plover,\n")
json.dump(OUT, outfile, indent=0)
outfile.write(")\n")
outfile.close()

DICT = {}
for INPUT_PATH in INPUT_PATHS:
    with open(INPUT_PATH) as f:
        DICT.update(json.load(f))

OUT = make_out()

outfile = open(OUTPUT_PATH, 'w')
outfile.write("Object.assign(TypeJig.Translations.Plover,\n")
json.dump(OUT, outfile, indent=0)
outfile.write(")\n")
outfile.close()
