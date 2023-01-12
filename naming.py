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




def findProcessIdByName(processName):
    
    listOfProcessObjects = []
    
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        
        try:
            
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            
            if processName.lower() in pinfo['name'].lower() :
                
                listOfProcessObjects.append(pinfo)
        
        except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
            
            pass
    
    return listOfProcessObjects;




def checkIfProcessRunning(processName):
    
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        
        try:
            
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                
                return True
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            
            pass
    
    return False;




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
        
        optionYN = input('\nDo you want to continue encoding this file? [y/n/blank to exit]: ')
           
        if optionYN == "y":
                
            print('\nContinuing encode of files fragments before...')
            interrEncode()
            
        elif optionYN == "n":
                
            # break
            exit()
            
        else:
                
            exit()
    
    else:
        
        print("No mkv file detected. Proceeding for default programs...")



def getVideoInformation():

    # GET OLD FRAGMENTED ENCODE DURATION
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-show_streams", "-print_format", "json", filenameDict[0]])
    ffprobe_data = json.loads(out)
    
    global duration
    global videoBitrate
    global codecs
    global videoFPS
    
    duration = float(ffprobe_data["format"]["duration"])
    videoBitrate = int(ffprobe_data["format"]["bit_rate"])
    codecs = str(ffprobe_data['streams'][0]['tags']['ENCODER'])
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
    a = 0
    b = 100
    
    for bb in worker:
        
        f = open( bb , "a")
        f.write("ffmpeg -ss "+ tstInterrStart[a] +" -i " + filePath +" "+ ffmpegCMDs +" -an -movflags use_metadata_tags -to "+ timestampArr[a] +" \""+ filenameDict[b] + "\"")
        f.close()
        a += 1
        b += 1
        
    for c in worker:
        subprocess.Popen('start cmd /c '+ c, shell=True)




def timestamp():

    filePathNoQuote = filePath.replace("\"", "")
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-show_streams", "-print_format", "json", filePathNoQuote])
    ffprobe_data = json.loads(out)
    
    durationFull = float(ffprobe_data["format"]["duration"])
    
    w2sT = str(datetime.timedelta(seconds = (1/2) * durationFull))
    w3ff = str(datetime.timedelta(seconds = (2/2) * durationFull))
    
    w1to = str(datetime.timedelta(seconds = ((0/2) * durationFull) + duration))
    w2to = str(datetime.timedelta(seconds = ((1/2) * durationFull) + duration))
    
    global timestampArr
    global tstInterrStart
    
    timestampArr = [w2sT, w3ff]
    tstInterrStart = [w1to, w2to]




def interrEncode():
    
    speed = input("\nInput speed to encode: ")
    
    getVideoInformation()
    
    global ffmpegCMDs
    ffmpegCMDs = "-c:v "+ codecs +" -preset "+ speed +" -b:v " + str(videoBitrate) + " -r "+ videoFPS +" -pix_fmt yuv420p -movflags use_metadata_tags"
    
    print(ffmpegCMDs)

    filenameplusInterr()
    
    timestamp()
    
    writeWorkerFile()
    
    
    

def divitFFprocess():

    # LIST PROCESS BASED ON PROCESS NAME: FFMPEG
    k = []
    listOfProcessIds = findProcessIdByName('ffmpeg')
    
    if len(listOfProcessIds) > 0:
        
        print('FFmpeg process ID detected:')
    
        for elem in listOfProcessIds:
        
            ffPID = elem['pid']
            print(ffPID)
            k.append(ffPID)

    else :
    
        print('ERROR: FFmpeg process not detected')
    
    # ASSIGN EVERY FFMPEG PID TO ITS OWN VARIABLE    
    PIDArr = [ k[0] , k[1] ]
    print(PIDArr)
    
    # CREATE NEW VARIABLE WITH ITS OWN AFFINITY MASK
    if name == 'nt':
        
        mask1 = 63
        mask2 = 4032
    
    else:
        
        mask1 = {0,1,2,3,4,5}
        mask2 = {6,7,8,9,10,11}

    AffArr = [ mask1 , mask2 ]
    print("\nTherefore uses "+ name +" format affinity masking:")
    print(AffArr)
    
    u = 0

    # SETTING CPU AFFINITY TO EVERY FFMPEG PID
    if name == 'nt':
    
        for s in PIDArr:
        
            
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, s)
            win32process.SetProcessAffinityMask(handle, AffArr[u])
            u += 1

    else:
    
        for s in PIDArr:
        
            os.sched_setaffinity(s, AffArr[u])
            u += 1
            
    # GET CPU AFFINITY FOR EACH FFMPEG WORKER (THIS IS AFTER APPLYING CPU MASKING)




    # LOOP CHECK IF FFMPEG PROCESS IF RUNNING, IF TRUE THEN DON'T PROCEED TO NEXT STAGE
    while checkIfProcessRunning('ffmpeg') == True:
    
        clear()
        print("\nAffinity set!")
        print('INFO: FFmpeg process detected, halting process temporarily until encoding finished.\n')
        
        if name == 'nt':
    
            cc = 0
            for w in PIDArr:
                
                handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, PIDArr[cc])
                y = win32process.GetProcessAffinityMask(handle)
                print("\nFFmpeg PID "+ str(w) +" is running on thread "+ str(y))
                cc += 1

        else:
    
            y = [os.sched_getaffinity(p), os.sched_getaffinity(q)]
    
            for w in PIDArr:
        
                print("\nFFmpeg PID "+ str(w) +" is running on thread "+ str(y))
    




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

time.sleep(3)

# DIVIT FFMPEG PROCESS TO ITS CERTAIN CPU AFFINITY
divitFFprocess()







#####################################################################
#####################################################################





# MESSAGE DONE PROCESSING
print("\nExecution done!")