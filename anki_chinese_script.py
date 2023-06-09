#!/usr/bin/env python3

import csv
import random
import genanki

# Filename of the data file
data_filename = "chinese_vocab_words_v3.csv"

# Filename of the Anki deck to generate
deck_filename = "Chinese_Review_Test_3.apkg"

# Title of the deck as shown in Anki
anki_deck_title = "Chinese Review Test 3 SCRIPT GENERATED"

# Name of the card model
anki_model_name = "Basic Chinese Flash"

# Create the deck model

model_id = random.randrange(1 << 30, 1 << 31)

style = """
.card {
 font-family: arial;
 font-size: 24px;
 text-align: center;
 color: black;
 background-color: white;
}
.hanzi {
 font-size: 64px;
}
"""

anki_model = genanki.Model(
    model_id,
    anki_model_name,
    fields=[{"name": "hanzi"}, {"name": "pinyin"},
            {"name": "meaning"}, {"name": "example"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '<p class="hanzi">{{hanzi}}</p>',
            "afmt": '{{FrontSide}}<hr id="answer"><p class="pinyin">{{pinyin}}</p><p class="meaning">{{meaning}}</p><p class="example">{{example}}</p>',
        },
    ],
    css=style,
)

# The list of flashcards
anki_notes = []

with open(data_filename, "r") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=",")

    for row in csv_reader:
        print(row)
        anki_note = genanki.Note(
            model=anki_model,
            # simplified writing, pinyin, meaning
            fields=[row[0], row[1], row[2], row[3]],
        )
        anki_notes.append(anki_note)

# Shuffle flashcards
random.shuffle(anki_notes)

anki_deck = genanki.Deck(model_id, anki_deck_title)
anki_package = genanki.Package(anki_deck)

# Add flashcards to the deck
for anki_note in anki_notes:
    anki_deck.add_note(anki_note)

# Save the deck to a file
anki_package.write_to_file(deck_filename)

print("Created deck with {} flashcards".format(len(anki_deck.notes)))
