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
w2ss = str(datetime.timedelta(seconds = (1/3) * duration))
w3ss = str(datetime.timedelta(seconds = (2/3) * duration))

wt   = str(datetime.timedelta(seconds = (1/3) * duration))

workerSSArr = [w1ss,w2ss,w3ss]
print(workerSSArr,wt)





# invoke new ffmpeg process with its own ffmpeg commands



## but before that, we need to configure outputName
fpthOut1 = (videoPath[:-4] + "_AV1-1.mp4")
fpthOut2 = (videoPath[:-4] + "_AV1-2.mp4")
fpthOut3 = (videoPath[:-4] + "_AV1-3.mp4")
print("\nProcessed video will be named as following:\n" + fpthOut1 + "\n" + fpthOut2 + "\n" + fpthOut3)
fpthOutArr = [fpthOut1,fpthOut2,fpthOut3]

