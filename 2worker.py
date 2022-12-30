import subprocess
import json
import datetime
import os
import time
import psutil
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

# CLEAR TERMINAL
clear()

# FORMATTING & STRING TEMPLATE
a = "ffmpeg -ss "
b = " -i "
c = " -c:v libsvtav1 -b:v 2.5M -preset 7 -c:a aac -an -t "
d = " "
n = "\n"
t = "\t"
nt = "\n\t"
nn = "\n\n"

# get file input
videoPath = input("Drag video file into this program: ")
#videoPath = r"C:\Users\Haizi\221221_CrimsonSnow-pzZGkScgBsQ.mp4"

# extract and print time in seconds (we use ffprobe here)
out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", videoPath])
ffprobe_data = json.loads(out)
duration = float(ffprobe_data["format"]["duration"])
print("Total duration in seconds is " + str(duration))

# now, find its HH:MM:SS for each worker (by fraction)
w1ss = str(datetime.timedelta(seconds = (0/2) * duration))
w2sT = str(datetime.timedelta(seconds = (1/2) * duration))
#w3ss = str(datetime.timedelta(seconds = (2/3) * duration))

SSAr = [w1ss,w2sT]
print(nn,"2 start point of this media is",SSAr,n,"Duration from start point is",w2sT)

# Write cache file and runner file
## but before that, we need to configure outputName
Out1 = (videoPath[:-4] + "_AV1-1.mp4")
Out2 = (videoPath[:-4] + "_AV1-2.mp4")
#Out3 = (videoPath[:-4] + "_AV1-3.mp4")
OutAr = [Out1,Out2]
print(n,"Processed video will be named as following:",nt,OutAr[0],nt,OutAr[1])

## declare worker name for nt and posix
if name == 'nt': # for windows
        wFile = ["w1.bat","w2.bat"]
        wRunner = "runner.bat"
else:            # for mac and linux
        wFile = ["w1.sh","w2.sh"]
        wRunner = "runner.sh"

## create new worker file based on wFile array
g = -1
print(g)
for e in wFile:
    g += 1
    f = open( e , "a")
    print(g)
    f.write(a + SSAr[g] + b + videoPath + c + w2sT + d + OutAr[g])
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

# RUN RUNNER --> W1,W2
if name == 'nt': # for windows
    subprocess.Popen('start cmd /c runner.bat',shell=True)
else:            # for mac and linux
    subprocess.Popen('chmod +x ./runner.sh; ./runner.sh',shell=True)

time.sleep(5)



# DO CPU ASSIGNMENTS
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
#r = k[2]
PIDArr = [p,q]
print(PIDArr)

## create var with its own affinity mask
if name == 'nt': # for windows
    mask1 = 63
    mask2 = 4032
    
else:            # for mac and linux
    mask1 = {0,1,2,3,4,5}
    mask2 = {6,7,8,9,10,11}
    

AffArr = [mask1,mask2]
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
if name == 'posix':
    unixAffAr = [os.sched_getaffinity(p), os.sched_getaffinity(q)]
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

# MESSAGE DONE PROCESSING
print("\n\nExecution done!")
if name == 'nt':
    print("Do double check CPU affinity in Task Manager.\n\n")
else:
    print("Do double check CPU affinity by using command 'taskset -cp [PID]'.\n\n")