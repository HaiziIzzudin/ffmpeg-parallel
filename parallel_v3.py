import subprocess
import json
import datetime
import os
import time
from glob import glob
from os import system, name
    
def install(package): # this is a definition to install package NOT included with python library (denoted with install())
    subprocess.run(["pip", "install", package])
    
install("psutil")
import psutil

if name == 'nt':

    install("colorama")
    install("pywin32")
    subprocess.run(["python", "Scripts/pywin32_postinstall.py", "-install"])
    import win32api
    import win32con
    import win32process
    import msvcrt
    from colorama import just_fix_windows_console
    from colorama import Fore, Back, Style



# FUNCTIONS COLLECTION
def header():
    print(Back.YELLOW + '                                                                   ')
    print(Fore.BLACK  + '        FFMPEG PARALLEL VERSION 3 BY MUHAMAD HAIZI IZZUDIN         ')
    print(Fore.BLACK  + '    github.com/haiziizzudin • DONATE AT: ko-fi.com/haiziizzudin    ')
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
    return listOfProcessObjects;

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;



def configureFFmpeg():
    
    clear()
    header()
    print("Enter in option\n[A] libsvtav1, or\n[B] libx265\nto use for your encoding.")
    print("\nInput either A or B: ")
    codecs = msvcrt.getch().decode('ASCII')
    codecs = codecs.upper()
    clear()
    header()

    if codecs == 'A':

        codecs = 'libsvtav1'
        print(codecs + " selected. Input speed to use:")
        print("TIP: 12 = ~36 fps\nTIP: 7 = ~20 fps")
        print("TIP: 6 = ~16 fps\nTIP: 4 = ~7 fps")
        print("\nThis metrics is based on AMD Ryzen 5 6600H\n(results may vary)")
        speed = input("\nInput integer only: ")

    elif codecs == 'B':

        codecs = 'libx265'
        print(codecs + " selected. Input speed to use:")
        print("TIP: Speed 'veryfast' = ~25 fps\nTIP: Speed 'medium' = ~5 fps")
        print("TIP: Speed 'slow' = ~1.7 fps")
        print("\nThis metrics is based on AMD Ryzen 5 6600H\n(results may vary)")
        print("\nInput a character either\n[A] ultrafast\n[B] veryfast\n[C] fast\n[D] medium\n[E] slow, OR \n[F] veryslow: ")
        speed = msvcrt.getch().decode('ASCII')
        speed = codecs.upper()
        
    else:
        
        print("Program error: Input invalid\nProgram will now exit.")
        time.sleep(0.5)
        clear()
        exit()
    
    clear()
    header()
    print("Enter in bitrate to use for your encoding.")
    print("Leave blank to set bit rate halves of the original.")
    videoBitrateOutput = input("\nInput integer in bytes (you can put unit like k OR M): ")

    if not videoBitrateOutput:
        
        videoBitrateOutput = (videoBitrate/2)
        
    clear()
    header()
    print("Enter in frame rate. Leave blank to use default frame rate.")
    print("TIP: some video recording has variable frame rate. This is not recommended for Post-Production footage.")
    print("TIP: Best practice is to use whole numbers (not float).")
    videoFPSOutput = input("\nInput integer: ")
    
    global ffmpegCMDs

    if not videoFPSOutput:
        
        ffmpegCMDs = "-c:v "+ codecs +" -preset "+ speed +" -b:v " + str(videoBitrateOutput) + " -pix_fmt yuv420p -movflags use_metadata_tags"
        
    else:

        ffmpegCMDs = "-c:v "+ codecs +" -preset "+ speed +" -b:v " + str(videoBitrateOutput) + " -r "+ videoFPSOutput +" -pix_fmt yuv420p -movflags use_metadata_tags"

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
videoPathNoQuote = videoPath.replace("\"", "")
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
        subprocess.Popen('chmod +x ./runner.sh; ./runner.sh',shell=True)

time.sleep(3)




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




################################################################################
################################################################################




# LOOP CHECK IF FFMPEG PROCESS IF RUNNING, IF TRUE THEN DON'T PROCEED TO NEXT STAGE
ffProc = True

while ffProc == True:

    if checkIfProcessRunning('ffmpeg'):
        
        ffProc = True
        clear()
        header()
        print('INFO: FFmpeg process detected, halting process temporarily until encoding finished.\n')        
        print("\nINFO: While you're on it, please check CPU affinity masking in\nNT: Task Manager / UNIX: taskset -cp [PID]\nif its uses correct masking.\n\n")
    
    else:
        
        ffProc = False
        print('INFO: FFmpeg process not detected anymore. Proceeding to next process...\n\n')



# WRITE FILENAME TO CONCATLIST.TXT
ad = open("concatList.txt" , "a")

for i in range(100, 102):
    
    ad.write("file '"+ fragFNdict[i] + "'\n")

ad.close()



# RUN AUDIO EXTRACT
aacPath = videoFNb4split[0] + "_audio.aac"
print("Temporary audio only file will be rendered:\n" + aacPath)
subprocess.run('ffmpeg -nostats -nostdin -hide_banner -loglevel quiet -i '+ videoPath +' -vn -c:a aac -b:a 256k -af dynaudnorm=f=10:g=3:m=35 -movflags use_metadata_tags \"' + aacPath + "\"", shell=True)



# RUN CONCATENATION
if name == 'nt':
    dirSlash = "\\"
else:
    dirSlash = "/"

subprocess.run('ffmpeg -hide_banner -f concat -safe 0 -i concatList.txt -i \"'+ aacPath +'\" -c copy -movflags use_metadata_tags ' + videoFNAr[0] + dirSlash + videoFNb4split[0] + '_AV1.mp4\"', shell=True)



# OPTION TO REMOVE TEMPORARY FILE
clear()
header()
print("Remove temporary file? [y/n]: ")
option = msvcrt.getch().decode('ASCII')
option = option.upper()

if option == "Y":
    
    print("Removing temporary file...")
    
    # DELETE WORKER FILE
    for i in range(0,2):
    
        os.remove(worker[i])
        os.remove(fragFNdict[i+100])
    
    os.remove(aacPath)
    os.remove("concatList.txt")
    clear()

elif option == "N":
    
    print("\nTemporary file kept.")
    print("Access these file at your home directory.")
    print("(Make sure to DELETE all temporary files before running ffmpeg-parallel again.)")