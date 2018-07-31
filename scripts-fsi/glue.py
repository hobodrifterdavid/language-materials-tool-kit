from gtts import gTTS
from tempfile import TemporaryFile
import os

outputDirectory = "output"
TrackName = "EN_A"

try:
	os.mkdir(outputDirectory) 
except:
	print("Output folder already exists, skip creating.\n")

file = open("eng.txt")
lines = file.readlines()
for idx, val in enumerate(lines):
    tts = gTTS(text=val, lang='en')
    tts.save(outputDirectory + "/"  + str(idx+1).zfill(4) + TrackName + ".mp3")
    #f = TemporaryFile()
    #tts.write_to_fp(f)
    #f.close()
