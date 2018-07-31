from gtts import gTTS
from tempfile import TemporaryFile
import os
import codecs

TrackName = "FR_B"

try:
	os.mkdir(outputDirectory) 
except:
	print("Output folder already exists, skip creating.\n")

file = codecs.open("work/french4", encoding='utf8')
# file = open("work/french4")
lines = file.readlines()
for idx, val in enumerate(lines):
    tts = gTTS(text=val, lang='fr')
    tts.save("work/0004_KID/"  + str(idx+1).zfill(4) + TrackName + ".mp3")
    #f = TemporaryFile()
    #tts.write_to_fp(f)
    #f.close()
