import subprocess
import json
import datetime
import os
import time
import psutil
from glob import glob
from os import system, name

if name == 'nt': # for windows
    import win32api
    import win32con
    import win32process

# FUNCTIONS COLLECTION
def clear():
    if name == 'nt': # for windows
        _ = system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        _ = system('clear')
        
def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
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
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

# CLEAR TERMINAL
clear()

# FORMATTING & STRING TEMPLATE
a = "ffmpeg -ss "
b = " -i "
c = " -c:v libsvtav1 -b:v 5M -preset 12 -an -t "
d = " "

nt = "\n\t"
nn = "\n\n"

# get file input
videoPath = input("FFmpeg-3worker (Version 2)\ngithub.com/HaiziIzzudin\n\nDrag video file into this program:\n")
#videoPath = r"C:\Users\Haizi\After_Like.mp4"

# extract and print time in seconds (we use ffprobe here)
out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", videoPath])
ffprobe_data = json.loads(out)
duration = float(ffprobe_data["format"]["duration"])
filename = str(ffprobe_data["format"]["filename"])
print("This video filename is " + str(filename))
print("Total duration in seconds is " + str(duration))

# now, find its HH:MM:SS for each worker (by fraction)
w1ss = str(datetime.timedelta(seconds = (0/3) * duration))
w2sT = str(datetime.timedelta(seconds = (1/3) * duration))
w3ss = str(datetime.timedelta(seconds = (2/3) * duration))

SSAr = [w1ss,w2sT,w3ss]
print(nn,"3 start point of this media is",SSAr,"\nDuration from start point is",w2sT)

# Write cache file and runner file
## but before that, we need to configure outputName
# GET FILENAME ONLY
videoFileNameAr = os.path.split(videoPath) #array
videoFileNameExt = videoFileNameAr[1] # filename only

Out1 = (videoFileNameExt[:-4] + "_frag1.mp4")
Out2 = (videoFileNameExt[:-4] + "_frag2.mp4")
Out3 = (videoFileNameExt[:-4] + "_frag3.mp4")
fileFragExt = [Out1, Out2, Out3] # this one baru filename + frag Array

print("\nProcessed fragments will be named as following:")
ee = -1
for e in fileFragExt:
    ee += 1
    print("\t" + e)

## declare worker name for nt and posix
if name == 'nt': # for windows
    wFile = ["w1.bat","w2.bat","w3.bat"]
    wRunner = "runner.bat"
else:            # for mac and linux
    wFile = ["w1.sh","w2.sh","w3.sh"]
    wRunner = "runner.sh"

## create new worker file based on wFile array
g = -1
for e in wFile:
    g += 1
    f = open( e , "a")
    f.write(a + SSAr[g] + b + videoPath + c + w2sT + d + fileFragExt[g])
    f.close()

## create new runner file
i = -1
j = open(wRunner , "a")
for h in wFile:
    if name == 'nt': # for windows
        j.write("start cmd /c " + h + "\n")
    else:            # for mac and linux
        j.write("konsole -e bash ./" + h + "&\n")
j.close()

# RUN RUNNER --> W1,W2,W3
if name == 'nt': # for windows
    subprocess.Popen('start cmd /c runner.bat',shell=True)
else:            # for mac and linux
    subprocess.Popen('chmod +x ./runner.sh; ./runner.sh',shell=True)

time.sleep(5)




################################################################################
################################################################################




## List process ID detected from name: ffmpeg
k = []
listOfProcessIds = findProcessIdByName('ffmpeg')
if len(listOfProcessIds) > 0:
    print('FFmpeg process ID detected:')
    for elem in listOfProcessIds:
        ffPID = elem['pid']
        k.append(ffPID)
else :
    print('ERROR: FFmpeg process not detected')
    
## assigning every ffmpeg worker ID to its own var
### NT & POSIX
p = k[0]
q = k[1]
r = k[2]
PIDArr = [p,q,r]
print(PIDArr)

## create var with its own affinity mask
if name == 'nt': # for windows
    mask1 = 1185
    mask2 = 600
    mask3 = 2310
else:            # for mac and linux
    mask1 = {0,5,10,7}
    mask2 = {4,9,6,3}
    mask3 = {8,1,2,11}

AffArr = [mask1,mask2,mask3]
print("\nTherefore uses "+ name +" format affinity masking:")
print(AffArr)

## now set affinity to the PID ffmpeg
u = -1
if name == 'nt': # for windows
    for s in PIDArr:
        u += 1
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, s)
        win32process.SetProcessAffinityMask(handle, AffArr[u])
else:            # for mac and linux
    for s in PIDArr:
        u += 1
        os.sched_setaffinity(s, AffArr[u])

## get CPU affinity for each ffmpeg worker and print it (POSIX ONLY).
if name == 'posix': # for windows
    unixAffAr = [os.sched_getaffinity(p), os.sched_getaffinity(q), os.sched_getaffinity(r)]
    print("\nAffinity set!")
    x = -1
    for w in PIDArr:
        x += 1
        y = unixAffAr[x]
        print("FFmpeg PID "+ str(w) +" is running on thread "+ str(y))

# DELETE RUNNER AND WORKER FILE
for v in wFile:
    os.remove(v)
os.remove(wRunner)




################################################################################
################################################################################




# LOOP CHECK IF FFMPEG PROCESS IF RUNNING, IF TRUE THEN DON'T PROCEED TO NEXT STAGE
ffProc = True
while ffProc == True:
    if checkIfProcessRunning('ffmpeg'):
        ffProc = True
        clear()
        print('INFO: FFmpeg process detected, halting process temporarily until encoding finished.\n')
        print("INFO: While you're on it, please check CPU affinity masking in\nNT: Task Manager / UNIX: taskset -cp [PID]\nif its uses correct masking.\n\n")
    else:
        ffProc = False
        print('INFO: FFmpeg process not detected anymore. Proceeding to next process...\n\n')


# GET FILENAME ONLY
#aa = os.path.split(OutAr[0]) # array
#ab = os.path.split(OutAr[1]) # array
#ac = os.path.split(OutAr[2]) # array
#fileWithExt = [aa[1], ab[1], ac[1]] # this one baru filename only


# WRITE FILENAME TO CONCATLIST.TXT
ad = open("concatList.txt" , "a")
for ae in fileFragExt:
    ad.write("file '"+ ae + "'\n")
ad.close()


## CREATE NEW AUDIO-EXTRACT WORKER FILE
aacPath = videoFileNameExt[:-4] + "_audio.aac"
print("All the file listed below has no use and will be removed:\n" + aacPath)

if name == 'nt': # for windows
    af = open("audioexct.bat" , "a")
else:            # for mac and linux
    af = open("audioexct.sh" , "a")

af.write("ffmpeg -i "+ videoPath +" -vn -c:a copy " + aacPath)
af.close()



## CREATE NEW CONCAT+AUDIO WORKER FILE
ag = os.path.split(videoPath) # array
agFname = ag[1] # select filename only
agFnameNoExt = agFname[:-4]

homedir = os.path.expanduser('~')

if name == 'nt': # for windows
    DesktopDir = "\\Desktop\\"
    af = open("concat.bat" , "a")
else:            # for mac and linux
    DesktopDir = "/Desktop/"
    af = open("concat.sh" , "a")

outConcatPlusAudio = homedir + DesktopDir + agFnameNoExt + "_AV1.mp4"
# print(outConcatPlusAudio)

af.write("ffmpeg -f concat -safe 0 -y -i concatList.txt -i "+ aacPath +" -c copy " + outConcatPlusAudio)
af.close()



## FIRST, RUN AUDIOEXCT.BAT/.SH & CONCAT.BAT/.SH
if name == 'nt': # for windows
    subprocess.run('start cmd /c audioexct.bat',shell=True)
    subprocess.run('start cmd /c concat.bat',shell=True)
else:            # for mac and linux
    subprocess.run('chmod +x ./audioexct.sh; konsole -e bash audioexct.sh',shell=True)
    subprocess.run('chmod +x ./concat.sh; konsole -e bash concat.sh',shell=True)  



## DELETE CONCAT.BAT/.SH & CONCATLIST & AUDIOEXCT.BAT/.SH & ALL FRAGMENTED ENCODER
if name == 'nt': # for windows
    listRemoval = ["concatList.txt", "audioexct.bat", "concat.bat"]
else: # for mac and linux
    listRemoval = ["concatList.txt", "audioexct.sh", "concat.sh"]

for aj in fileFragExt:
    print(aj)
for ak in listRemoval:
    print(ak)

print("\n\nComment out os.remove() in script to keep these file.")

time.sleep(2)

for ah in fileFragExt:
    os.remove(ah)
for ai in listRemoval:
    os.remove(ai)
os.remove(aacPath)
os.remove("3worker.py")




# MESSAGE DONE PROCESSING
print("\n\nExecution done!\nYour encoded file should be in Desktop.\n\n")
