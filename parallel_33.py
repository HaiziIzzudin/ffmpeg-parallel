debugFlag = False

import subprocess
import json
import datetime
import os
import time
from glob import glob
from os import system, name
    
def pip_install(package): # this is a definition to install package NOT included with python library (denoted with install())
    subprocess.run(["pip", "install", package])
    
pip_install("psutil")
pip_install("colorama")
time.sleep(1)
import psutil
from colorama import Fore, Back, Style

if name == 'nt':
    pip_install("pywin32")
    subprocess.run(["python", "Scripts/pywin32_postinstall.py", "-install"])
    time.sleep(1)
    import win32api
    import win32con
    import win32process
    from colorama import just_fix_windows_console
    import msvcrt
else:
    pip_install("getch")
    time.sleep(1)
    import getch



# FUNCTIONS COLLECTION
def header():
    print(Back.YELLOW + '                                                                   ')
    print(Fore.BLACK  + '        FFMPEG PARALLEL VERSION 3 BY MUHAMAD HAIZI IZZUDIN         ')
    print(Fore.BLACK  + '    github.com/haiziizzudin • DONATE AT: ko-fi.com/haiziizzudin    ')
    if debugFlag == True:
        print(Back.RED+ '    ATTENTION: debugFlag is set to True. Only enable this if       ')
        print(Back.RED+ '               you are debugging or are a developer.               ')
    print(Back.YELLOW + '                                                                   ')
    print(Style.RESET_ALL)

def clear():
    if name == 'nt': # for windows
        _ = system('cls')
    else: # for mac and linux (here, os.name is 'posix')
        _ = system('clear')
        
def findProcessIdByName(processName):
    listOfProcessObjects = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if processName.lower() in pinfo['name'].lower() :
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
            pass
    return listOfProcessObjects

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False



def configureFFmpeg():
    
    clear()
    header()
    print("Type in EXACTLY:\nlibsvtav1, or\n[B] libx264\nto use for your encoding.")
    
    if debugFlag == False:
        codecs = input("\nInput: ")
    else:
        codecs = "libx264"

    clear()
    header()

    if codecs == 'libsvtav1':
        print(codecs + " selected. Input speed to use:")
        print("\n*** TIP ***\n12 = ~36 fps\n7 = ~20 fps\n6 = ~16 fps\n4 = ~7 fps\n***********")
        if debugFlag == False:
            speed = input("Integer only: ")
        else:
            speed = 6

    elif codecs == 'libx264':
        codecs = 'libx264'
        print(codecs + " selected. Type the speed parameters EXACTLY, FOLLOW CAPS:")
        print("\n*** TIP ***\n'veryfast' = ~25 fps\n'medium' = ~5 fps\n'slow' = ~1.7 fps\n***********")
        if debugFlag == False:
            speed = input("\nInput EXACTLY either\nultrafast\nveryfast\nfast\nmedium\nslow, OR \nveryslow: ")
        else:
            speed = "veryslow"
        
    else:
        
        print("Program error: Input invalid\nProgram will now exit.")
        time.sleep(0.5)
        clear()
        exit()
    
    clear()
    header()
    print("Enter in bitrate to use for your encoding.\nLeave blank to set bit rate halves of the original.")
    videoBitrateOutput = input("\nInput integer in bytes (you can put unit like k OR M): ")

    if not videoBitrateOutput:
        videoBitrateOutput = videoBitrate/2
    
    global ffmpegCMDs
    ffmpegCMDs = "-c:v "+ codecs +" -preset "+ str(speed) +" -b:v " + str(videoBitrateOutput) + " -pix_fmt yuv420p -movflags use_metadata_tags"

    clear()
    header()
    print("FFmpeg command:\n" + ffmpegCMDs)



def findTimestamp():
    
    global timestampDict
    timestampDict = {}
    print("\nThree point of this media is ")
    
    for a in range(0, 3):
        
        timestampDict[a] = str(datetime.timedelta(seconds = (a/2) * durationOri))
        print(timestampDict[a])



def getFilenameplusMkv():
    
    global videoFNAr
    global videoFNb4split
    videoFNAr = os.path.split(videoPath) #array [path, file+ext]
    videoFNb4split = videoFNAr[1].split(".") # split filename with ext on "."
    # to get filename only, enter videoFNb4split[0]
    
    global fragFNdict
    fragFNdict = {}
    print("\nFragments filename will be named as following:")
    
    for a in range(100, 102):
        
        fragFNdict[a] = videoFNb4split[0] + "_frag" + str(a) + ".mkv"
        print(fragFNdict[a])



# GET FILE INPUT
clear()
header()
videoPath = input("Input video: ")



# GET MEDIA INFORMATION, CONFIGURE FFMPEG, FIND TIMESTAMP AND GET FRAGMENTED FILENAME
if name == 'nt':
    videoPathNoQuote = videoPath.replace("\"", "")
else:
    videoPathNoQuote = videoPath.replace("\'", "")

out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-show_streams", "-print_format", "json", videoPathNoQuote])
ffprobe_data = json.loads(out)
durationOri = float(ffprobe_data["format"]["duration"])
videoBitrate = int(ffprobe_data["format"]["bit_rate"])

configureFFmpeg()
findTimestamp()
getFilenameplusMkv()
input("\nPress enter to continue...")



# CREATE NEW WORKER FILE BASED ON WFILE ARRAY
if name == 'nt':
    worker = {0: 'w1.bat', 1: 'w2.bat'}
else:
    worker = {0: 'w1.sh',  1: 'w2.sh'}

for i in range(0,2):
    
    f = open( worker[i] , "a")
    f.write("ffmpeg -ss " + timestampDict[i] + " -i " + videoPath +" "+ ffmpegCMDs +" -an -movflags use_metadata_tags -to "+ timestampDict[i+1] +" \""+ fragFNdict[i+100] +"\"")
    f.close()



# RUN RUNNER --> W1,W2
for i in range(0,2):

    if name == 'nt':
        subprocess.Popen('start cmd /c '+ worker[i] , shell=True)
    else:
        subprocess.Popen('chmod +x ./' + worker[i] + '; konsole -e bash ./'+ worker[i] + ' $' , shell=True)

time.sleep(3)





############################################################
## PART III: SETTING AND CONFIGURING PID AND CPU AFFINITY ##
############################################################

# LIST PROCESS BASED ON PROCESS NAME: FFMPEG
k = []
listOfProcessIds = findProcessIdByName('ffmpeg')
if len(listOfProcessIds) > 0:
    print('FFmpeg process ID detected:')
    for elem in listOfProcessIds:
        ffPID = elem['pid']
        k.append(ffPID)
else :
    print('ERROR: FFmpeg process not detected')
    

# ASSIGN EVERY FFMPEG PID TO ITS OWN VARIABLE
p = k[0]
q = k[1]
PIDArr = [p,q]
print(PIDArr)

# SETTING CPU AFFINITY TO EVERY FFMPEG PID
u = -1

if name == 'nt':
    mask1 = 3591
    mask2 = 504
    AffArr = [mask1,mask2]
    for s in PIDArr:
        u += 1
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, s)
        win32process.SetProcessAffinityMask(handle, AffArr[u])          # Set affinity
        y = win32process.GetProcessAffinityMask(handle)                 # Get affinity (check if affinity is successfully set)
        print("FFmpeg PID "+ str(s) +" is running on thread "+ str(y))  # print PID + affinity

else:
    mask1 = {0,1,2,9,10,11}
    mask2 = {3,4,5,6,7,8}
    AffArr = [mask1,mask2]
    for s in PIDArr:
        u += 1
        os.sched_setaffinity(s, AffArr[u])                              # Set affinity
        y = [os.sched_getaffinity(p), os.sched_getaffinity(q)]          # Get affinity (check if affinity is successfully set)
        print("FFmpeg PID "+ str(s) +" is running on thread "+ str(y))  # print PID + affinity


# GET CPU AFFINITY FOR EACH FFMPEG WORKER (THIS IS AFTER APPLYING CPU MASKING)
print("\nAffinity set!")

################################################################################
################################################################################




# LOOP CHECK IF FFMPEG PROCESS IF RUNNING, IF TRUE THEN DON'T PROCEED TO NEXT STAGE
ffProc = True

while ffProc == True:

    if checkIfProcessRunning('ffmpeg'):
        
        ffProc = True
        clear()
        header()
        print('INFO: FFmpeg process detected, halting process temporarily until encoding finished.')
        print("\nINFO: While you're on it, please check CPU affinity masking in\nNT: Task Manager / UNIX: taskset -cp [PID]\nif its uses correct masking.")
        time.sleep(5)
    
    else:
        
        ffProc = False
        print('INFO: FFmpeg process not detected anymore. Proceeding to next process...\n\n')



# WRITE FILENAME TO CONCATLIST.TXT
ad = open("concatList.txt" , "a")

for i in range(100, 102):
    
    ad.write("file '"+ fragFNdict[i] + "'\n")

ad.close()



# RUN AUDIO EXTRACT
m4aPath = videoFNb4split[0] + "_audio.m4a"
print("Temporary audio only file will be rendered:\n" + m4aPath)
subprocess.run('ffmpeg -nostats -nostdin -hide_banner -loglevel quiet -i '+ videoPath +' -vn -c:a aac -map 0:1 -map 0:2? -map 0:3? -b:a 320k -af dynaudnorm=f=10:g=3:m=20 -movflags use_metadata_tags \"' + m4aPath + "\"", shell=True)



# RUN CONCATENATION
if name == 'nt':
    dirSlash = "\\"
    dirComma = "\""
else:
    dirSlash = "/"
    dirComma = "\'"

if debugFlag == True:
    cmdFull = 'ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i concatList.txt -i '+ dirComma + m4aPath + dirComma + ' -c copy -map 0:0 -map 1:0 -map 1:1? -map 1:2? -movflags use_metadata_tags '+ dirComma + videoFNAr[0] + dirSlash + videoFNb4split[0] + '_AV1.mp4' + dirComma

    print(cmdFull)

    ad = open("concatScript.sh" , "a")
    ad.write(cmdFull)
    ad.close()

    input("Press enter to proceed concatenation:")

subprocess.run('ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i concatList.txt -i '+ dirComma + m4aPath + dirComma + ' -c copy -map 0:0 -map 1:0 -map 1:1? -map 1:2? -movflags use_metadata_tags '+ dirComma + videoFNAr[0] + dirSlash + videoFNb4split[0] + '_AV1.mp4' + dirComma , shell=True)





# OPTION TO REMOVE TEMPORARY FILE
if debugFlag == False:
    clear()
    header()

print("Remove temporary file? [y/n]: ")

if name == 'nt':
    option = msvcrt.getch().decode('ASCII')
else:
    option = getch.getch()

option = option.upper()

if option == "Y":
    
    print("Removing temporary file...")
    
    # DELETE WORKER FILE
    for i in range(0,2):
    
        os.remove(worker[i])
        os.remove(fragFNdict[i+100])
    
    os.remove(m4aPath)
    os.remove("concatList.txt")

    if debugFlag == False:
        os.remove("parallel_v3.py")

    clear()

elif option == "N":
    
    print("\nTemporary file kept.")
    print("Access these file at your home directory.")
    print("(Make sure to DELETE all temporary files before running ffmpeg-parallel again.)")
