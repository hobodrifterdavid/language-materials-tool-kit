import nltk

file = open('pol3.txt', 'r', encoding="utf8")

# sent_detector = nltk.data.load('spanish.pickle')
sent_detector = nltk.data.load('tokenizers/punkt/polish.pickle')

sents = sent_detector.tokenize(file.read())

file.close()

newSents = []

# newSents = sents

for sent in sents:
    newArray = sent.splitlines()
    for item in newArray:
        if item != "" and item != "\n":
            newSents.append(item)

outString = ""

for sent in newSents:
    outString += sent
    outString += " "
    outString += "\n"

##process output string with this:
##
##        this.prepareText = function(inputText) {
##
##        // Standardise newlines
##        inputText = inputText.replace(/(\r\n|\n|\r)/gm, "\n");
##
##        // Paragraph breaks go to |*p|
##        inputText = inputText.replace(/(\n){2,}/gi, "|*p|");
##
##        // newlines go to |
##        inputText = inputText.replace(/\n/gi, "|");
##
##        // I forget what this does. Whitespace?
##        inputText = inputText.replace(/\s+/g, " ");

## new_string = re.sub(r'"(\d+),(\d+)"', r'\1.\2', outString)    

fileOut = open('pol3-seg.txt', 'w', encoding="utf8")

fileOut.write(outString)

fileOut.close()
