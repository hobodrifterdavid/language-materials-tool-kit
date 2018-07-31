import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

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

for x in range(300):
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

print(currentLines)
