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

def configureFFmpeg():
    
    clear()
    print("Enter in video codec to use for your encoding.")
    print("Some of the helpful keyword is: libsvtav1, libx265")
    print("TIP: 'libsvtav1' is useful to compress video that is ready for delivery. NOT COMPATIBLE with video editors and some low end devices.")
    print("TIP: 'libx265' is useful to compress video that is used for production. COMPATIBLE with video editors like Adobe Premiere Pro and some hardware.")
    codecs = input("Input string (strict lowercase only): ")
    clear()

    if codecs == 'libsvtav1':

        print("libsvtav1 selected. Input speed to use.")
        print("TIP: Speed 12 = ~36 frames processed / second.")
        print("TIP: Speed 7 = ~20 frames processed / second.")
        print("TIP: Speed 6 = ~16 frames processed / second.")
        print("TIP: Speed 4 = ~7 frames processed / second.")
        print("(This metrics is based on system: AMD Ryzen 5 6600H on max TDP. Your frame processed can vary between system, CPU and footage complexity.)")
        speed = input("\nInput integer only: ")

    elif codecs == 'libx265':

        print("libx265 selected. Input speed to use.")
        print("TIP: Speed 'veryfast' = ~25 frames processed / second.")
        print("TIP: Speed 'medium' = ~5 frames processed / second.")
        print("TIP: Speed 'slow' = ~1.7 frames processed / second.")
        print("(This metrics is based on system: AMD Ryzen 5 6600H on max TDP. Your frame processed can vary between system, CPU and footage complexity.)")
        speed = input("\nInput valid string only (ultrafast, veryfast, fast, medium, slow, veryslow): ")

    else:

        print("custom codec inputted. Make sure the codec you inserted abide with the ffmpeg documentation, else encoding will fail.")
        speed = input("\nInput speed (that is valid for the codec): ")
    
    clear()
    print("Enter in bitrate to use for your encoding.")
    print("Leave blank to set video bit rate automatically (original footage bit rate / 2)")
    print("TIP: This is functional if you are converting from lossless like Apple ProRes Codec")
    videoBitrateOutput = input("Input integer in bytes (you can put unit like: k = kilobit, M = megabit): ")

    if not videoBitrateOutput:
        
        videoBitrateOutput = (videoBitrate/2)
        
    clear()
    print("Enter in frame rate. Leave blank to use default frame rate.")
    print("TIP: some video recording has variable frame rate. This can cause problem on some editors and playback.")
    print("TIP: Best practice is to use whole numbers (not float).")
    videoFPSOutput = input("Input integer: ")
    global ffmpegCMDs

    if not videoFPSOutput:
        
        ffmpegCMDs = "-c:v "+ codecs +" -preset "+ speed +" -b:v " + str(videoBitrateOutput) + " -pix_fmt yuv420p -movflags use_metadata_tags"
        
    else:

        ffmpegCMDs = "-c:v "+ codecs +" -preset "+ speed +" -b:v " + str(videoBitrateOutput) + " -r "+ videoFPSOutput +" -pix_fmt yuv420p -movflags use_metadata_tags"

    print(ffmpegCMDs)



# CLEAR TERMINAL
clear()



# GET FILE INPUT
videoPath = input("FFmpeg-parallel (Version 2 - debug code: 230107-0112)\ngithub.com/HaiziIzzudin\n\nDrag video file into this program:\n")



# EXTRACT AND PRINT VIDEO METADATA
out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", videoPath])
ffprobe_data = json.loads(out)
duration = float(ffprobe_data["format"]["duration"])
filename = str(ffprobe_data["format"]["filename"])
videoBitrate = int(ffprobe_data["format"]["bit_rate"])

clear()
print("This video filename is " + str(filename))
print("Total duration in seconds is " + str(duration))
print("Video bitrate is " + str(videoBitrate))

configureFFmpeg()



# now, find its HH:MM:SS for each worker (by fraction)
w1ss = str(datetime.timedelta(seconds = (0/2) * duration))
w2sT = str(datetime.timedelta(seconds = (1/2) * duration))
SSAr = [w1ss,w2sT]
print("\n\nTwo (2) start point of this media is",SSAr,"\nDuration from start point is",w2sT)



# GET FILENAME+EXTENSION ONLY, NO PATH
videoFileNameAr = os.path.split(videoPath) #array
videoFileNameExt = videoFileNameAr[1] # filename only

Out1 = (videoFileNameExt[:-4] + "_frag1.mkv")
Out2 = (videoFileNameExt[:-4] + "_frag2.mkv")
fileFragExt = [Out1, Out2] # this one baru filename + frag + extension Array

print("\nProcessed fragments will be named as following:")
ee = -1
for e in fileFragExt:
    ee += 1
    print("\t" + e)



## declare worker name for nt and posix
if name == 'nt':
    wFile = ["w1.bat","w2.bat"]
    wRunner = "runner.bat"
else:
    wFile = ["w1.sh","w2.sh"]
    wRunner = "runner.sh"



# CREATE NEW WORKER FILE BASED ON WFILE ARRAY
g = -1
for e in wFile:
    g += 1
    f = open( e , "a")
    f.write("ffmpeg -ss " + SSAr[g] + " -i " + videoPath +" "+ ffmpegCMDs +" -an -movflags use_metadata_tags -t "+ w2sT +" "+ fileFragExt[g])
    f.close()



# CREATE NEW RUNNER FILE
i = -1
j = open(wRunner , "a")
for h in wFile:
    if name == 'nt':
        j.write("start cmd /c " + h + "\n")
    else:
        j.write("konsole -e bash ./" + h + "&\n")
j.close()



# RUN RUNNER --> W1,W2,W3
if name == 'nt':
    subprocess.Popen('start cmd /c runner.bat',shell=True)
else:
    subprocess.Popen('chmod +x ./runner.sh; ./runner.sh',shell=True)

time.sleep(5)




################################################################################
################################################################################




## LIST PROCESS BASED ON PROCESS NAME: FFMPEG
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



## CREATE NEW VARIABLE WITH ITS OWN AFFINITY MASK
if name == 'nt':
    mask1 = 63
    mask2 = 4032
else:
    mask1 = {0,1,2,3,4,5}
    mask2 = {6,7,8,9,10,11}

AffArr = [mask1,mask2]
print("\nTherefore uses "+ name +" format affinity masking:")
print(AffArr)



# SETTING CPU AFFINITY TO EVERY FFMPEG PID
u = -1

if name == 'nt':
    
    for s in PIDArr:
        
        u += 1
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, s)
        win32process.SetProcessAffinityMask(handle, AffArr[u])

else:
    
    for s in PIDArr:
        
        u += 1
        os.sched_setaffinity(s, AffArr[u])



# GET CPU AFFINITY FOR EACH FFMPEG WORKER (THIS IS AFTER APPLYING CPU MASKING)
print("\nAffinity set!")

if name == 'nt':
    
    for w in PIDArr:
        
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, s)
        y = win32process.GetProcessAffinityMask(handle)
        print("FFmpeg PID "+ str(w) +" is running on thread "+ str(y))

else:
    
    y = [os.sched_getaffinity(p), os.sched_getaffinity(q)]
    
    for w in PIDArr:
        
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
        print("\nINFO: While you're on it, please check CPU affinity masking in\nNT: Task Manager / UNIX: taskset -cp [PID]\nif its uses correct masking.\n\n")
    
    else:
        
        ffProc = False
        print('INFO: FFmpeg process not detected anymore. Proceeding to next process...\n\n')



# WRITE FILENAME TO CONCATLIST.TXT
ad = open("concatList.txt" , "a")

for ae in fileFragExt:
    
    ad.write("file '"+ ae + "'\n")

ad.close()



## CREATE NEW AUDIO EXTRACT WORKER FILE
aacPath = videoFileNameExt[:-4] + "_audio.aac"
print("Temporary audio only file will be rendered:\n" + aacPath)

if name == 'nt':
    
    af = open("audioexct.bat" , "a")

else:
    
    af = open("audioexct.sh" , "a")

af.write("ffmpeg -nostats -nostdin -hide_banner -loglevel quiet -i "+ videoPath +" -vn -c:a aac -b:a 256k -filter:a dynaudnorm -movflags use_metadata_tags " + aacPath)
af.close()



## CREATE NEW CONCATENATE + AUDIO WORKER FILE
ag = os.path.split(videoPath) # array
agFname = ag[1] # select filename only
agFnameNoExt = agFname[:-4]

homedir = os.path.expanduser('~')

if name == 'nt':
    
    DesktopDir = "\\Desktop\\"
    af = open("concat.bat" , "a")

else:
    
    DesktopDir = "/Desktop/"
    af = open("concat.sh" , "a")

outConcatPlusAudio = homedir + DesktopDir + agFnameNoExt + "_AV1.mp4"

af.write("ffmpeg -nostats -nostdin -hide_banner -loglevel quiet -f concat -safe 0 -i concatList.txt -i "+ aacPath +" -c copy -movflags use_metadata_tags " + outConcatPlusAudio)
af.close()



## FIRST, RUN AUDIOEXCT.BAT/.SH & CONCAT.BAT/.SH
print('INFO: Encoding aac file...\n')

if name == 'nt':
    
    subprocess.run('audioexct.bat',shell=True)
    print('INFO: Concatenating...\n\n')
    subprocess.run('concat.bat',shell=True)

else:
    
    subprocess.run('chmod +x ./audioexct.sh; ./audioexct.sh',shell=True)
    print('INFO: Concatenating...\n\n')
    subprocess.run('chmod +x ./concat.sh; ./concat.sh',shell=True)  



# DELETE CONCAT.BAT/.SH & CONCATLIST & AUDIOEXCT.BAT/.SH & ALL FRAGMENTED ENCODER
if name == 'nt':
    listRemoval = ["concatList.txt", "audioexct.bat", "concat.bat"]
else:
    listRemoval = ["concatList.txt", "audioexct.sh", "concat.sh"]


time.sleep(2)


clear()
option = input("\nRemove temporary file? [y/n] (case-sensitive): ")

if option == "y":
    
    print("Removing temporary file...")
    
    for ah in fileFragExt:
        
        os.remove(ah)
    
    for ai in listRemoval:
        
        os.remove(ai)
    
    os.remove(aacPath)
    os.remove("3worker_v2.py")

elif option == "n":
    
    print("\nTemporary file kept.")
    print("Access these file at "+ homedir)
    print("(Make sure to DELETE all temporary files before running ffmpeg-parallel again.)")






# MESSAGE DONE PROCESSING
print("\n\nExecution done!\nYour encoded file should be in Desktop.\n\n")