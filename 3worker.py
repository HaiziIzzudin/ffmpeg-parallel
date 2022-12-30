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

workerSSArr = [w1ss,w2sT,w3ss]
print("\n3 start point of this media is",workerSSArr,"\nDuration from start point is",w2sT)





# invoke new ffmpeg process with its own ffmpeg commands



## but before that, we need to configure outputName
fpthOut1 = (videoPath[:-4] + "_AV1-1.mp4")
fpthOut2 = (videoPath[:-4] + "_AV1-2.mp4")
fpthOut3 = (videoPath[:-4] + "_AV1-3.mp4")
print("\nProcessed video will be named as following:\n" + fpthOut1 + "\n" + fpthOut2 + "\n" + fpthOut3)
fpthOutArr = [fpthOut1,fpthOut2,fpthOut3]


## Command template
a = "ffmpeg -ss "
b = "-i "
c = "-c:v libsvtav1 -b:v 2.5M -preset 7 -c:a aac -b:a 192k -t "
d = " "



## create temporary worker file

if name == 'nt': # for windows
        wFile = ["w1.bat","w2.bat","w3.bat"]
else:            # for mac and linux
        wFile = ["w1.sh","w2.sh","w3.sh"]

for x in wFile:
    f = open( x , "a")
    f.write(a + w1ss + b + videoPath + c + w2sT + d + fpthOut1)
    f.close()