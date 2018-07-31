import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from googletrans import Translator

# obtain path to "english.wav" in the same folder as this script



from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "0005FR_A.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

translator = Translator()
# use the audio file as the audio source
r = sr.Recognizer()


for index in range(1,51):
    mp3 = AudioSegment.from_mp3(str(index).zfill(4) + "FR_A.mp3")
    mp3.export(str(index).zfill(4) + "FR_A.wav", format="wav")

    with sr.AudioFile(str(index).zfill(4) + "FR_A.wav") as source:

        audio = r.record(source)  # read the entire audio file
        # try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        recognisedText = r.recognize_google(audio, language="fr")
        print("Google Speech Recognition thinks you said " + recognisedText)
        #except sr.UnknownValueError:
        #    print("Google Speech Recognition could not understand audio")
        #except sr.RequestError as e:
       #     print("Could not request results from Google Speech Recognition service; {0}".format(e))

        tts = gTTS(text=recognisedText, lang='fr')
        tts.save(str(index).zfill(4) + "FR_B.mp3")

        
        tts = gTTS(text=translator.translate(recognisedText, dest='en').text, lang='en')
        tts.save(str(index).zfill(4) + "EN_A.mp3")

