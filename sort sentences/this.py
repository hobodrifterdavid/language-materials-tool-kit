import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

def run():

    file=open('english.txt', encoding='utf8')
    lines=file.readlines()

    frequency = {}

    wordLines = []

    for line in lines:
        words = word_tokenize(line)
        wordLines.append(words)
        lemWords = [wordnet_lemmatizer.lemmatize(word) for word in words]
        for word in lemWords:
            if(word in frequency):
                frequency[word] += 1
            else:
                frequency[word] = 1

    wordFreq = sorted(frequency.items(), key=lambda x:x[1], reverse=True)

    wordBag = []

    for x in range(100):
        wordBag.append(wordFreq.pop(0)[0])

    def allIn(line, wordBag):
        for word in line:
            if word not in wordBag:
                return False
        return True

    currentLines = []

    for wordArray in wordLines:
        result=allIn(wordArray, wordBag)
        if(result):
            currentLines.append(wordArray)
     
    newWords={}

    for word in wordFreq:
        word= word[0]
        testWordBag=list(wordBag)
        testWordBag.append(word)
        index = 0
        for wordArray in wordLines:
            if wordArray in currentLines:
                continue
            result=allIn(wordArray, testWordBag)
            if(result):
                if(word in newWords):
                    newWords[word]['times']+=1
                    newWords[word]['sents'].append(wordArray)
                else:
                    newData = { 'times':1, 'sents': [wordArray] }
                    newWords[word] = newData

    newWordFreq = sorted(newWords.items(), key=lambda x:x[1]['times'], reverse=True)

    for item in newWordFreq:
        print(item[1]['times'])
        print(item[0])
        for sent in item[1]['sents']:
            print(sent)

import cProfile
cProfile.run(run())
