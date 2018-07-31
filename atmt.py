
text1Filename = 'fr-master.txt'
text2Filename = 'pol3-seg.txt'
dicName = 'fr-pl.dic'
outFileName = 'pol3-out.txt'

# Prepare Source Text

sourceTextFile = open(text1Filename, 'r', encoding="utf8")

lines = sourceTextFile.readlines()

sourceLineCounter = len(lines)

paragraphs = []

outString = ""

sourceTempLineCounter = 0

for i in range(len(lines)):
    if lines[i] == '<p>\n':
        paragraphs.append(i)
    else:
        outString += lines[i]
        sourceTempLineCounter += 1

writeOutFile = open('sourceTemp.txt', 'w', encoding="utf8")
writeOutFile.write(outString)
writeOutFile.close()

# Run HunAlign

args = ['hunalign/hunalign.exe', 'hunalign/data/' + dicName, '../sourceTemp.txt', text2Filename, '-realign']

import subprocess

returned = subprocess.run(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

decoded = returned.stdout.decode('ascii')

lines = decoded.splitlines()

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

            


text2 = open(text2Filename, 'r', encoding="utf8")
text2lines = text2.read().splitlines()

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

outString = ""

for line in out:
    outString += line
    outString += "\n"

outFile = open(outFileName, 'w', encoding="utf8")

outFile.write(outString)
outFile.close()

