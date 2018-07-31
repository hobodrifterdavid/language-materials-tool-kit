# -*- coding: utf-8 -*-
import vocabs

raw = """Gardening is the practice of growing plants. Ornamental plants are normally grown for their flowers, foliage, overall appearance, or for their dyes. Useful plants are grown for consumption (vegetables, fruits, herbs, and leaf vegetables) or for medicinal use. A gardener is someone who practices gardening.
Gardening ranges in scale from fruit orchards, to long boulevard plantings with one or more different types of shrubs, trees and herbaceous plants, to residential yards including lawns and foundation plantings, to large or small containers grown inside or outside. Gardening may be very specialized, with only one type of plant grown, or involve a large number of different plants in mixed plantings. It involves an active participation in the growing of plants, and tends to be labor intensive, which differentiates it from farming or forestry."""

import nltk

tokens = nltk.word_tokenize(raw)

text = nltk.Text(tokens)

from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
lmtzr.lemmatize('cars')

now_known=set([])

#               lemmed      word        translation
word_database={"ejemplo": {"ejemplos": {"examples":1}}}

def get_translation(word, lemmed, context):
    # Do we have the lemmed versioned?
    if lemmed in word_database:
        # Do we have the specific word?
        if word in word_database[lemmed]:
            print context
            # Print choices:
            for i in range(len(word_database[lemmed][word])):
                print "Choice "+str(i)+".: "+word_database[lemmed][word].items()[i][0]+str(word_database[lemmed][word].items()[i][1])
            selection = raw_input("? ")
            if selection == "t":
                translation = raw_input("Enter translation: ")
                translation =word_database[lemmed][word][translation]=1
                return translation
            if selection.isdigit():
                translation =word_database[lemmed][word].items()[int(selection)][0]
                word_database[lemmed][word][translation] += 1
                return translation
        # We don't have the specific word
        print context
        translation = raw_input("Enter translation: ")
        word_database[lemmed] = {word: {translation:1}}
        return translation
        
    print context
    translation = raw_input("Enter translation: ")
    word_database[lemmed] = {word: {translation:1}}
    return translation

    

for i in range(len(text)):
    lemmed = lmtzr.lemmatize(text[i]).lower()
    if lemmed not in vocabs.oxford3000:
        if lemmed not in now_known:
            string = ""
            for item in text[i-8:i]:
                string += " " + item
            string+= " **" + text[i] + "**"
            for item in text[i+1:i+8]:
                string += " " + item
            text.tokens[i]=text.tokens[i] + " (*" + get_translation(text[i], lemmed, string) + "*)"
