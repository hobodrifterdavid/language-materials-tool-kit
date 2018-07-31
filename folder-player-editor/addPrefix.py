import os
import shutil

def addPostfix(postfix):
        # Reorders the files and folders in the CWD
        index = 0
        searchIndex = 0
        while(index <= 9999):
                searchFilenamePath = os.path.join(os.getcwd(), str(index).zfill(4) + '.wav')
                if os.path.isfile(searchFilenamePath):
                        # set searchIndex file to index file
                        src = os.path.join(os.getcwd(), str(index).zfill(4) + '.wav')
                        dest = os.path.join(os.getcwd(), str(index).zfill(4) + postfix + '.wav')
                        shutil.move(src, dest)
                index +=1

addPostfix("FR_A")
