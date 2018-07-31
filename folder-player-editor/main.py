import os
import pygame
import readchar
import shutil
# import tts.sapi

##### Config #####

primaryLang = 'FRA'
secondaryLang = 'ENG'
extension = '.mp3'

startDir = os.path.normpath(os.getcwd())

currentIndex = 0

startIndex = 0
finishIndex = 0

playingFileHandle = False

dummyPath = os.path.join(os.getcwd(),'dummy.wav')

postfix = "FR_A"

##### TTS functions #####

# voice = tts.sapi.Sapi()
# voice.set_rate(5)

# def say(string):
#       player.stop()
#       voice.say(string)

##### Media Playing functions #####

##vlc_instance = vlc.Instance()
##myPlayer = vlc_instance.media_player_new()
##vlc_events = myPlayer.event_manager()

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
pygame.mixer.init()

_playlist = []

def queuePlay(file):
        _playlist.append(file)

def startQueue():
        _playNext('fried')

def _playNext(event):
        global _playlist
        global startDir
        global vlc_instance
        global myPlayer
        print("called")
        print(str(_playlist))

        if len(_playlist) > 0:
                path = os.path.join(startDir, 'tts', _playlist.pop(0) + '.mp3')
                myPlayer.stop()
                newMedia = vlc_instance.media_new_path(path)
                myPlayer.set_media(newMedia)
                myPlayer.play()

##def play(filename):
##    myPlayer.stop()
##    _playlist =  []
##    media = vlc_instance.media_new(filename)
##    myPlayer.set_media(media)
###    print media.get_mrl() # File location to get title 
###    print player.get_length() #Time duration of file -1 means there is no media
###    print player.get_state() #Player's state
##    myPlayer.play()

def play(filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

def stop():
        pygame.mixer.music.stop()
        pygame.mixer.music.load(dummyPath)
        
def playTTS(filename):
        path = os.path.join(startDir, 'tts', filename + '.mp3')
        play(path)

def playNum(inputInt):
        inputInt = int(inputInt)
        string = str(inputInt)
        if len(string) > 4:
                print("Number too big to read!")
                return
        # thousands
        if len(string) > 3:
                queuePlay(string[-4].ljust(4, '0'))
        # hundreds
        if len(string) > 2:
                if string[-3] == '0':
                        pass
                else:
                        queuePlay(string[-3].ljust(3, '0'))
        # tens
        atLeast10 = False
        if len(string) > 1:
                atLeast10 = True
                if string[-2] == '0':
                        pass
                else:
                        queuePlay(string[-2].ljust(2, '0'))
        # ones
        if len(string) > 0:
                if atLeast10 and string[-1] == '0':
                        pass
                else:
                        queuePlay(string[-1])

        startQueue()



##### Directory Operations #####

def getCurrentDirInt():
        try:
                value = os.path.split(os.getcwd())[1][:4]
                dirInt = int(value)
                # cdi = int(os.getcwd().split('\\')[-1][:3])
                return dirInt
        except:
                print("Can't find a Number")



def moveToFirstChildDir():
        items = os.listdir()
        dirName = None
        count = 0
        for item in items:
                try:
                        int(item[:3])
                        count += 1
                except:
                        pass

                if item.startswith('0001'):
                        dirName = item

        if (dirName == None):
                if os.path.normpath(os.getcwd()) == startDir:
                        playTTS("noBooksFound")
                else:
                        playTTS("noChildrenItems")
        else:
                playNum(count)
                playTTS("items")
                newPath = os.path.join(os.getcwd(), dirName)
                enterDir(newPath)
                

def moveToNextDir():
        cdi = getCurrentDirInt()
        parentDirPath = os.path.split(os.getcwd())[0]
        parentDirItems = os.listdir(parentDirPath)

        for item in parentDirItems:
                # Look for a directory to move to
                if item.startswith(str(cdi+1).zfill(4)):
                        print("directory found" + item)
                        newPath = os.path.join(parentDirPath, item)
                        enterDir(newPath)
                        return
        else:
                # case none is found
                playTTS("lastItem")

def moveToPrevDir():
        cdi = getCurrentDirInt()
        parentDirPath = os.path.split(os.getcwd())[0]
        parentDirItems = os.listdir(parentDirPath)

        for item in parentDirItems:
                # Look for a directory to move to
                if item.startswith(str(cdi-1).zfill(4)):
                        newPath = os.path.join(parentDirPath, item)
                        enterDir(newPath)
                        return
        else:
                # case none is found
                playTTS("lastItem")


def playPrimary():
        primaryPath = os.path.join(os.getcwd(), primaryLang+extension)
        if (os.path.isfile(primaryPath)):
                play(primaryPath)
        else:
                playTTS("fileMissing")

def playSecondary():
        SecondaryPath = os.path.join(os.getcwd(), secondaryLang+extension)
        if (os.path.isfile(SecondaryPath)):
                play(SecondaryPath)
        else:
                playTTS("fileMissing")

##### Get a Keystroke. Hard Apparently. #####

def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

getch = _find_getch()

##### Wait on user input #####


##### Wait on user input #####

def createSubfolder():
        global startIndex
        global finishIndex
        global currentIndex
        global postfix
        
        newFolderName = str(startIndex).zfill(4) + "_KIDS"
        print "newfolder name " + newFolderName
        try:
                os.mkdir(newFolderName)
        except:
                print "Folder already exist or some error";
        for loopIndex in range(startIndex+1, finishIndex+1, 1):
                src = os.path.join(os.getcwd(), str(loopIndex).zfill(4) + postfix + '.wav')
                dest = os.path.join(os.getcwd(), newFolderName, str(loopIndex).zfill(4) + postfix + '.wav')
                shutil.move(src, dest)

        os.chdir(os.path.join(os.getcwd(), newFolderName))
        reorder()
        os.chdir('..')
        reorder()

        currentIndex = startIndex + 1

def reorder():
        # Reorders the files and folders in the CWD
        index = 0
        searchIndex = 0
        while(searchIndex <= 9999):
                searchFilenamePath = os.path.join(os.getcwd(), str(searchIndex).zfill(4) + postfix + '.wav')
                if os.path.isfile(searchFilenamePath):
                        # set searchIndex file to index file
                        src = os.path.join(os.getcwd(), str(searchIndex).zfill(4) + postfix + '.wav')
                        dest = os.path.join(os.getcwd(), str(index).zfill(4) + postfix + '.wav')
                        shutil.move(src, dest)
                        
                        searchFolderName = str(searchIndex).zfill(4) + "_KIDS"
                        searchFolderPath = os.path.join(os.getcwd(), searchFolderName)
                        if os.path.isdir(searchFolderPath):
                                src = searchFolderPath
                                dest = os.path.join(os.getcwd(), str(index).zfill(4) + "_KIDS")
                                shutil.move(src, dest)
                        index +=1
                searchIndex +=1



ks = ''

while(True):

        # FIX: windows only :-/
        # os.system('cls')
        
        print os.getcwd()
        print '\n'
        print "Current Index = " + str(currentIndex).zfill(4)
        print "Start Index = " + str(startIndex).zfill(4)
        print "Finish Index = " + str(finishIndex).zfill(4)

        playpath = os.path.join(os.getcwd(), str(currentIndex).zfill(4) + postfix + '.wav')

        print playpath

        print ks

        try:
                play(playpath)
        except:
                print "Nope playback not happening"

        ks = readchar.readchar()

        stop()

        if ks == b'h':
                # Prev
                currentIndex -= 1
        elif ks == b'j':
                pass
                # Repeat
                # Do nothing here
        elif ks == b'k':
                # Next
                currentIndex += 1
        elif ks == b'u':
                # Up
                os.chdir('..')
                currentIndex = 0
        elif ks == b'm':
                # Down
                searchFolderName = str(currentIndex).zfill(4) + '_KIDS'
                searchFolderPath = os.path.join(os.getcwd(), searchFolderName)
                if os.path.isdir(searchFolderPath):
                        os.chdir(searchFolderPath)
                        currentIndex = 0
        elif ks == b's':
                startIndex = currentIndex
        elif ks == b'f':
                finishIndex = currentIndex
        elif ks == b'd':
                createSubfolder()
        elif ks == b'd':
                moveToNextDir()
        elif ks == b'a':
                moveToPrevDir()
        elif ks == b'r':
                reorder()
