import nltk
import subprocess
import os
from enum import Enum

# textFormats = Enum('plain')

class Text:

    languageCode = None
    meta1 = None
    meta2 = None
    cells = None

    def __str__(self):
        return self.textString[:200]

    def load(self, fileName):
        
        file = open(fileName, 'r', encoding="utf8")
        
        # lines = file.readlines()
        # self.fromRawCells(lines)

        with open(fileName, 'r', encoding="utf8") as file:
            lines = file.read().splitlines()
            self.fromRawCells(lines)

    def loadPlain(self, fileName, id, languageCode):

        self.id = id

        self.languageCode = languageCode

        with open(fileName, 'r', encoding="utf8") as file:
            self.cells = file.read().splitlines()

    def fromRawCells(self, cells):
            self.id = cells[0]
            self.languageCode = cells[1]
            self.meta1 = cells[2]
            self.meta2 = cells[3]
            self.cells = cells[4:]

    def fromData(self, id, languageCode, meta1, meta2, cells):
            self.id = id
            self.languageCode = languageCode
            self.meta1 = meta1
            self.meta2 = meta2
            self.cells = cells

    def save(self, fileName):

        outFile = open(fileName, 'w', encoding="utf8")

        outFile.write(self.id)
        outFile.write('\n')

        outFile.write(self.languageCode)
        outFile.write('\n')

        outFile.write(self.meta1)
        outFile.write('\n')

        outFile.write(self.meta2)
        outFile.write('\n')

        for cell in self.cells:
            outFile.write(cell)
            outFile.write('\n')

        outFile.close()

    def saveNoMeta(self, fileName):

        outFile = open(fileName, 'w', encoding="utf8")

        for cell in self.cells:
            outFile.write(cell)
            outFile.write('\n')

        outFile.close()

##    def segment(self):
##
##        tokenizerName = {'it': 'italian', 'pl': 'polish', 'en': 'english', 'de': 'german', 'fr': 'french'}
##
##        # sent_detector = nltk.data.load('spanish.pickle')
##        sent_detector = nltk.data.load('tokenizers/punkt/' + tokenizerName[self.languageCode] + '.pickle')
##
##        sents = sent_detector.tokenize(self.textString)
##
##        newSents = []
##
##        for sent in sents:
##            newArray = sent.splitlines(True)
##            for item in newArray:
##                if item != "" and item != "\n":
##                    newSents.append(item)
##
##        outString = ""
##
##        for sent in newSents:
##            outString += sent
##            outString += " "
##            outString += "\n"
##
##        returnText = Text()
##        returnText.languageCode = self.languageCode
##        returnText.textString = outString
##
##        return returnText

    def segment(self):

        tokenizerName = {'it': 'italian', 'pl': 'polish', 'en': 'english', 'de': 'german', 'fr': 'french'}

        # sent_detector = nltk.data.load('spanish.pickle')
        sent_detector = nltk.data.load('tokenizers/punkt/' + tokenizerName[self.languageCode] + '.pickle')

        newCells = []

        for cell in self.cells:
            newArray = sent_detector.tokenize(cell)
            for item in newArray:
                if item != "" and item != "\n":
                    newCells.append(item + ' ')

        returnText = Text()
        returnText.fromData('UNSET', self.languageCode, 'UNSET', 'UNSET', newCells)

        return returnText
    

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

    def align(self, newText):

        # Prepare Original Text

        sourceLineCounter = len(self.cells)

        paragraphs = []

        outString = ""

        sourceTempLineCounter = 0

        for i in range(len(self.cells)):
            if self.cells[i] == '<p>':
                paragraphs.append(i)
            else:
                outString += self.cells[i] + '\n'
                sourceTempLineCounter += 1

        writeOutFile = open('originalTextTemp.txt', 'w', encoding="utf8")
        writeOutFile.write(outString)
        writeOutFile.close()

        # Prepare New Text

        segmented = newText.segment()
        segmented.saveNoMeta('newTextTemp.txt')

        # newText.save('newTextTemp.txt')

        # Run HunAlign

        dicName = self.languageCode + '-' + newText.languageCode +'.dic' 

        args = ['hunalign/hunalign.exe', 'hunalign/data/' + dicName, '../originalTextTemp.txt', '../newTextTemp.txt', '-realign']

        returned = subprocess.run(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        decoded = returned.stdout.decode('ascii')

        lines = decoded.splitlines()

        # Delete temporary files

        # os.remove("originalTextTemp.txt")
        # os.remove("newTextTemp.txt")

        # Prepare structure

        data = []

        for line in lines:
            splitLine = line.split('\t')
            data.append({"sourceIndex": int(splitLine[0]), "targetIndex": int(splitLine[1]), "confidence": splitLine[2]})

        # Add missing items

        ##lookFor = 0
        ##
        ##for i in range(len(data)):
        ##    while lookFor != data[i]["targetIndex"]:
        ##        data.insert(i, { "sourceIndex": data[i-1]["sourceIndex"], "targetIndex": i } )
        ##        lookFor = lookFor + 1

        # Transform data

        alreadySeen = []
        newData = {}

        for item in data:
            if item["targetIndex"] not in alreadySeen:
                alreadySeen.append(item["targetIndex"])
                if item["sourceIndex"] not in newData:
                    newData[item["sourceIndex"]] = [item["targetIndex"]]
                else:
                    newData[item["sourceIndex"]].append(item["targetIndex"])


        ##for i in range(len(lines)):
        ##    splitLine = lines[i].split('\t')
        ##    sourceIndex = int(splitLine[0])
        ##    targetIndex = int(splitLine[1])
        ##    if targetIndex not in alreadySeen:
        ##        alreadySeen.append(targetIndex)
        ##        if sourceIndex not in data:
        ##            data[sourceIndex] = [targetIndex]
        ##        else:
        ##            data[sourceIndex].append(targetIndex)

        text2lines = newText.cells

        ##out = ""
        ##
        ##lastOne = 0
        ##
        ##for i in range(1000):
        ###    if i in paragraphs:
        ###         out += "<p>\n"
        ##    if i in newData:
        ##        for j in newData[i]:
        ##            out += text2lines[j]
        ##            lastOne = j
        ##        lastOne = lastOne+1
        ##    if (i+1) in newData:
        ##        while lastOne not in newData[i+1]:
        ##            out += text2lines[lastOne]
        ##            lastOne = lastOne+1
        ##    out += "\n"

        out = []

        nextOne = 0

        def missing(aDic, searchFor):
            for key in aDic.keys():
                if searchFor in aDic[key]:
                    return False

            return True

        for i in range(sourceTempLineCounter):
            lineString = ""
            if i in newData:
                for j in newData[i]:
                    # This is because it's a slice based file format and my code is crummy.
                    if j < len(text2lines):
                        lineString += text2lines[j]
                        nextOne = j
                nextOne = nextOne+1

            while (missing(newData, nextOne) and nextOne < len(text2lines)):
                print('Missing: ' + str(nextOne))
                lineString += text2lines[nextOne]
                nextOne = nextOne+1
            out.append(lineString)

        for i in range(sourceLineCounter):
            if i in paragraphs:
                out.insert(i, "<p>")

        outCells = []

        for line in out:
            outCells.append(line)

        returnText = Text()
        returnText.fromData('UNSET', newText.languageCode, newText.meta1, newText.meta2, outCells)

        return returnText
