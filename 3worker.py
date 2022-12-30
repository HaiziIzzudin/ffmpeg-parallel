#!/usr/bin/python

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
videoPath = input("Drag video file into this program: ")





# extract and print time in seconds (we use ffprobe here)
out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", videoPath])
ffprobe_data = json.loads(out)
duration = float(ffprobe_data["format"]["duration"])
print("Total duration in seconds is " + str(duration))





# now, find its HH:MM:SS for each worker (by fraction)
w1ss = str(datetime.timedelta(seconds = (0/3) * duration))
w2sT = str(datetime.timedelta(seconds = (1/3) * duration))
w3ss = str(datetime.timedelta(seconds = (2/3) * duration))

SSAr = [w1ss,w2sT,w3ss]
print("\n\n3 start point of this media is",SSAr,"\nDuration from start point is",w2sT)





# invoke new ffmpeg process with its own ffmpeg commands



## but before that, we need to configure outputName
Out1 = (videoPath[:-4] + "_AV1-1.mp4")
Out2 = (videoPath[:-4] + "_AV1-2.mp4")
Out3 = (videoPath[:-4] + "_AV1-3.mp4")
OutAr = [Out1,Out2,Out3]

print("\nProcessed video will be named as following:\n",OutAr[0],"\n",OutAr[1],"\n",OutAr[2])



## Command template
a = "ffmpeg -ss "
b = " -i "
c = " -c:v libsvtav1 -b:v 2.5M -preset 7 -c:a aac -b:a 192k -t "
d = " "
g = -1
n = "\n"



## create temporary worker file and runner file

if name == 'nt': # for windows
        wFile = ["w1.bat","w2.bat","w3.bat","runner.bat"]
else:            # for mac and linux
        wFile = ["w1.sh","w2.sh","w3.sh","runner.sh"]

for e in wFile:
    g += 1
    f = open( e , "a")
    f.write(a + OutAr[g] + b + videoPath + c + w2sT + d + OutAr[g])
    f.close()

f = open(wFile[3] , "a")
f.write(wFile[0],n,wFile[1],n,wFile[2])
f.close()