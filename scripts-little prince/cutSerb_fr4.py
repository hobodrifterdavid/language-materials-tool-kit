from pydub import AudioSegment
import json
import sys
import os
import subprocess

os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAI5RAGB2FAG7RW7SA'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'

#fileName = sys.argv[1]

fileName = "english"
workDirectory = 'work'

TrackName = "EN_A"

#Open source text at work/fileName, remove <p>s
text= open(workDirectory+"/"+fileName+".txt").read()
text = text.replace("<p>", "")

# Break chapters into seperate files
chapters=text.split("<c>")

# For each chapter
for chapterIndex in range(len(chapters)):
	chapterIndex = chapterIndex+1
	text = chapters[chapterIndex]
	text = text.replace("|", "\n")
	#text = os.linesep.join([s for s in text.splitlines() if s != ''])
	text = "\n".join([s for s in text.splitlines() if s != ''])
	# text = [s for s in text.splitlines() if s != '\n']
	# Save each chapter to a file
	thisFilename = fileName+str(chapterIndex)
	newTextFile = open(workDirectory+"/"+thisFilename, "w")
	newTextFile.write(text)
	newTextFile.close()

	# Figure out file paths
	#mp3Path = workDirectory+"/"+thisFilename+".mp3"

	mp3Path = workDirectory+"/"+"Ch"+str(chapterIndex)+".wav"

	textPath = workDirectory+"/"+thisFilename
	jsonPath = workDirectory+"/"+thisFilename+".json"
	parameterString = '"task_language=en|os_task_file_format=json|is_text_type=plain|task_adjust_boundary_algorithm=beforenext|task_adjust_boundary_beforenext_value=0.200"'

# |tts=aws|tts_cache=True

	# Not used:
	#argumentString = "vagrant ssh -c 'aeneas_execute_task " + "/vagrant/"+mp3Path + " " + "/vagrant/"+textPath + " " + parameterString + " " + "/vagrant/"+jsonPath + "'"
	#os.system(argumentString)

	# Vagrant
	# argumentString = """vagrant ssh -c "cd /vagrant; aeneas_execute_task """ + mp3Path + " " +textPath + " " + parameterString + " " + jsonPath + '"'
	
	# No Vagrant
	argumentString = """python -m aeneas.tools.execute_task """ + mp3Path + " " +textPath + " " + parameterString + " " + jsonPath + '"'

	# Run Aeneas
	print(argumentString)
	os.system(argumentString)

	#subprocess.call(["vagrant", "ssh", "-c", "aeneas_execute_task", "/vagrant/"+mp3Path, "/vagrant/"+textPath, parameterString, "/vagrant/"+jsonPath])

	# Get the JSON output file
	data = json.loads(open(jsonPath).read())

	# Load the original MP3 file
	# rec = AudioSegment.from_mp3(mp3Path)
	rec = AudioSegment.from_wav(mp3Path)

	chapterFolderPath = workDirectory + "/" + str(chapterIndex).zfill(4) + "_KID"

	# Create a new folder for the chapter
	#os.mkdir(chapterFolderPath) 

	try:
		os.mkdir(chapterFolderPath) 
	except:
		print("Output folder already exists, skip creating.\n")

	# Save the chopped-up mp3's to that folder
	for idx, val in enumerate(data["fragments"]):
	    startT = 1000*float(val["begin"])
	    endT = 1000*float(val["end"])
	    clip = rec[startT:endT]
	    if(idx == 0):
	    	clip.export(workDirectory+"/"+str(chapterIndex).zfill(4) + TrackName + ".mp3", format="mp3")
	    else:
	    	clip.export(chapterFolderPath + "/" + str(idx).zfill(4) + TrackName + ".mp3", format="mp3")
