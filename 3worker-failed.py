import subprocess
import json
import datetime
import os
import time
from os import system, name

# FUNCTIONS TO CLEAR TERMINAL
def clear():
    if name == 'nt': # for windows
        _ = system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        _ = system('clear')

clear()

# get file input
fpth = input("Drag video file into this program: ")

# extract and print time in seconds (we use ffprobe here)
out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", fpth])
ffprobe_data = json.loads(out)
dur = float(ffprobe_data["format"]["duration"])
print("Total duration in seconds is "+ str(dur))

# now, find its HH:MM:SS for each worker
w1ss = str(datetime.timedelta(seconds = (0/3)*dur))
w2ss = str(datetime.timedelta(seconds = (1/3)*dur))
w3ss = str(datetime.timedelta(seconds = (2/3)*dur))
wt = str(datetime.timedelta(seconds = (1/3)*dur))
workerSSArr = [w1ss,w2ss,w3ss]
print(workerSSArr,wt)

# invoke new ffmpeg process with its own ffmpeg commands

## but before that, we need to configure outputName
fpthOut1 = (fpth[:-4] + "_AV1-1.mp4")
fpthOut2 = (fpth[:-4] + "_AV1-2.mp4")
fpthOut3 = (fpth[:-4] + "_AV1-3.mp4")
print("\n\nProcessed video will be named as following:\n" + fpthOut1 + "\n" + fpthOut2 + "\n" + fpthOut3)
fpthOutArr = [fpthOut1,fpthOut2,fpthOut3]

## now we can invoke command ffmpeg (in new terminal possibly)

### filename has to change according to operating system
workerFilenameNTKnl = ["worker1.bat","worker2.bat","worker3.bat"]
workerFilenamePosix = ["worker1.sh","worker2.sh","worker3.sh"]
ffmpegCMD = " -c:v libsvtav1 -preset 7 -b:v 2.5M -c:a aac -b:a 192k -t "

# condition to create worker source file
z = -1
if name == 'nt': # for windows
    for x in workerFilenameNTKnl:
        z += 1
        f = open(x, "a")
        f.write("ffmpeg -ss "+workerSSArr[z]+" -i "+ fpth + ffmpegCMD + wt +" "+ fpthOutArr[z])
        
else: # for mac and linux(here, os.name is 'posix')
    for x in workerFilenamePosix:
        z += 1
        f = open(x, "a")
        f.write("ffmpeg -ss "+workerSSArr[z]+" -i "+ fpth + ffmpegCMD + wt +" "+ fpthOutArr[z])
    subprocess.Popen('konsole --noclose -e bash ./worker1.sh', shell=True)
    time.sleep(0.5)
    subprocess.Popen('konsole --noclose -e bash ./worker2.sh', shell=True)
    time.sleep(0.5)
    subprocess.Popen('konsole --noclose -e bash ./worker3.sh', shell=True)

time.sleep(5)

# setting process ID for every ffmpeg workers
processID = subprocess.check_output('pidof ffmpeg', shell=True).split()

print(processID)

p = int(processID[0])
q = int(processID[1])
r = int(processID[2])

print("ffmpeg has been detected to run on these process ID:")
print(p,q,r)

affinityMask1 = {0,5,10,7}
affinityMask2 = {4,9,6,3}
affinityMask3 = {8,1,2,11}

os.sched_setaffinity(p, affinityMask1)
os.sched_setaffinity(q, affinityMask2)
os.sched_setaffinity(r, affinityMask3)

affinityForP = os.sched_getaffinity(p)
affinityForQ = os.sched_getaffinity(q)
affinityForR = os.sched_getaffinity(r)

print("Affinity has been set!\nNow process P is running on thread ", affinityForP)
print("Process Q is running on thread ", affinityForQ)
print("Process R is running on thread ", affinityForR)