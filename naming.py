import subprocess
import json
import datetime
import os
import time
import psutil
import os.path
from glob import glob
from os import system, name

if name == 'nt': # for windows
    import win32api
    import win32con
    import win32process



def clear():
    if name == 'nt': # for windows
        _ = system('cls')
    else: # for mac and linux (here, os.name is 'posix')
        _ = system('clear')



def filenameExtract():
    
    # SPLIT FILEPATH INTO PATH AND FILE
    splitPath = os.path.split(filePath)
    global splitFilename
    splitFilename = splitPath[1].split(".")
    print("\n" + splitFilename[0]) # print filename only, no extension
    
    

def fragmentfnWizard():
    
    # WHILE LOOP
    a = 0
    global filenameDict
    filenameDict = {}
    
    while a <= 1:
        
        filenameDict[a] = (splitFilename[0] + "_frag" + str(a) + ".mkv")
        a += 1
        
    # print("\n" + str(filenameDict))



def interruptWizard():
    
    boolFileExist = (os.path.exists(filenameDict[0]) and os.path.exists(filenameDict[1]))
    # print(boolFileExist)
    
    if boolFileExist == True:
        
        print("\nThere is unfinished encoded file exists in cache.")
        print("This maybe due to encoder interrupted before.")
        
        while True:
            
            optionYN = input('\nDo you want to continue encoding this file? [y/n]: ')
            
            if optionYN == "y":
                
                print('\nContinuing encode of files fragments before...')
                interrEncode()
                exit()
            
            elif optionYN == "n":
                
                # break
                exit()
            
            else:
                
                clear()
                print ("Try again.") 
    
    else:
        
        print("No mkv file detected. Proceeding for default programs...")



def getVideoInformation():

    # GET OLD FRAGMENTED ENCODE DURATION
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-show_streams", "-print_format", "json", filenameDict[0]])
    ffprobe_data = json.loads(out)
    
    global duration
    duration = float(ffprobe_data["format"]["duration"])
    
    global videoBitrate
    videoBitrate = int(ffprobe_data["format"]["bit_rate"])
    
    global codecs
    codecs = str(ffprobe_data['streams'][0]['tags']['ENCODER'])
    
    global videoFPS
    videoFPS = str(ffprobe_data['streams'][0]['avg_frame_rate'])
    
    codecsArr = codecs.split(' ')
    codecs = codecsArr[1]
    
    videoFPSArr = videoFPS.split('/')
    videoFPS = videoFPSArr[0]




def filenameplusInterr():
    
    # WHILE LOOP
    a = 100
    
    while a <= 101:
        
        filenameDict[a] = (splitFilename[0] + "_frag" + str(a) + ".mkv")
        a += 1
        
    # print("\n" + str(filenameDict))




def writeWorkerFile():

    worker = ["worker1.bat", "worker2.bat"]
    a = 1
    
    for bb in worker:
        
        f = open( bb , "a")
        f.write("ffmpeg -ss "+ str(datetime.timedelta(seconds = (2/2) * duration)) +" -i " + filePath +" "+ ffmpegCMDs +" -an -movflags use_metadata_tags -to "+ str(timestampArr[a]) +" \""+ filenameDict[100] + "\"")
        f.close()
        a += 1




def timestamp():

    filePathNoQuote = filePath.replace("\"", "")
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-show_streams", "-print_format", "json", filePathNoQuote])
    ffprobe_data = json.loads(out)
    
    global durationFull
    durationFull = float(ffprobe_data["format"]["duration"])

    global w1ss
    global w2sT
    global w3ff
    
    w1ss = str(datetime.timedelta(seconds = (0/2) * durationFull))
    w2sT = str(datetime.timedelta(seconds = (1/2) * durationFull))
    w3ff = str(datetime.timedelta(seconds = (2/2) * durationFull))
    
    global timestampArr
    timestampArr = [w1ss, w2sT, w3ff]




def interrEncode():
    
    speed = input("\nInput speed to encode: ")
    
    getVideoInformation()
    
    global ffmpegCMDs
    ffmpegCMDs = "-c:v "+ codecs +" -preset "+ speed +" -b:v " + str(videoBitrate) + " -r "+ videoFPS +" -pix_fmt yuv420p -movflags use_metadata_tags"
    
    print(ffmpegCMDs)

    filenameplusInterr()
    
    timestamp()
    
    writeWorkerFile()
    
    




#####################################################################
#####################################################################





# CLEAR TERMINAL
clear()

# GET FILE INPUT
filePath = input("Drag video file into this program:\n")

# CALL FUNCTION FILENAME-EXTRACT
filenameExtract()

# CREATE NEW INTERMEDIARY FILE
fragmentfnWizard()

# CHECK IF THERE IS INTERMEDIARY FILE IN HOME DIRECTORY
interruptWizard()







#####################################################################
#####################################################################





# MESSAGE DONE PROCESSING
print("\nExecution done!")