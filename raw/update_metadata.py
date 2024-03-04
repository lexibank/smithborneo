"""This module updates the metadata."""
import csv
from collections import defaultdict
from csvw.dsv import UnicodeDictReader


# Load initial concepts
initial_concepts = defaultdict()
with UnicodeDictReader('../etc/archive/concepts.tsv', delimiter='\t') as reader:
    for line in reader:
        initial_concepts[line["ENGLISH"]] = [
            line['ENGLISH'],
            line['CONCEPTICON_GLOSS'],
            line['CONCEPTICON_ID']
            ]

# Load initial languages
initial_languages = defaultdict()
with UnicodeDictReader('../etc/archive/languages.tsv', delimiter='\t') as reader:
    for line in reader:
        initial_languages[line["Name"]] = [
            line['Name'],
            line['Glottocode'],
            line['ID'],
            line['Longitude'],
            line['Latitude']
            ]

# Load data to check missing\
final_concepts = defaultdict()
final_langs = defaultdict()

with UnicodeDictReader('cognates_95_229.csv', delimiter='\t') as reader:
    for row in reader:
        # Concept
        if row['concept'] not in final_concepts:
            # Add missing
            if row['concept'] in initial_concepts:
                final_concepts[row['concept']] = initial_concepts[row['concept']]

            else:
                final_concepts[row['concept']] = [row['concept'], '', '']

        # Languages
        if row['doculect'] not in final_langs:
            if row['doculect'] in initial_languages:
                final_langs[row['doculect']] = initial_languages[row['doculect']]
            else:
                final_langs[row['doculect']] = [row['doculect'], '', '', '', '']


with open('../etc/concepts.tsv', 'w', encoding="utf8", newline='') as f:
    csv_writer = csv.writer(f, delimiter='\t')
    csv_writer.writerow(['ENGLISH', 'CONCEPTICON_GLOSS', 'CONCEPTICON_ID'])
    for row in final_concepts:
        csv_writer.writerow(final_concepts[row])

with open('../etc/languages.tsv', 'w', encoding="utf8", newline='') as f:
    csv_writer = csv.writer(f, delimiter='\t')
    csv_writer.writerow(['NAME', 'GLOTTOCODE', 'ID', 'LONGITUDE', 'LATITUDE'])
    for row in final_langs:
        csv_writer.writerow(final_langs[row])
