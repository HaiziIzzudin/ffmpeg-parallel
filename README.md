![image_2022-12-30_23-33-14](https://user-images.githubusercontent.com/79714350/210088270-1e48cc3e-e0f6-438e-9452-c44bb99dab54.png)


# Encode with 3 concurrent ffmpeg process instead of one!
This is a Python script where ffmpeg will split inputted video into 3 parts, and encode it to their own cpu affinity SIMULTANEOUSLY to avoid system crash, and utilize CPU 100%

## REQUIREMENT / DEPENDENCIES
- ffmpeg, MUST accessible thru PATH. Those who don't know how to install I will provide tutorial later.
- python, MUST accessible in PATH
- pip, because you want to install some of other python module dependency
  - After installing pip, execute command below:
    ```
    pip install psutil
    ```
- If you going to use Windows, please install PowerShell version 6 or above.

## IMPORTANT NOTE
This script has been tailored to my machine. That's why I provide in script mode, not executable mode. Since this script is editable and open source, go ahead and change some of the parameters inside the script to match what's spec on your machine.

Some of the parameters that you can change is:
  - CPU Affinity allocation
  - Filename addition and extensions
  - the FFmpeg command itself
  - LINUX ONLY: Terminal name (my script is written for Konsole, which is KDE desktop environment command prompt)
  
Hopefully the next update I can eliminate some of the problem above.

## DOWNLOAD AND RUN SCRIPT
### Windows
You MUST and HAVE to run this command inside powershell version 6 and above. The one shipped with Windows is most probably old. Get the latest PowerShell by invoking `winget install microsoft.powershell`, OR if you don't have winget, [download here](https://learn.microsoft.com/en-gb/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.3#msi).
- 3 Workers
  ```
  irm https://raw.githubusercontent.com/HaiziIzzudin/ffmpeg-3worker/main/3worker_v2.py > 3worker.py; (Get-Content -path ~\3worker.py) | Set-Content -Encoding utf8NoBOM -Path ~\3worker.py; python ./3worker.py;
  ```
- 2 Workers
  ```
  irm https://github.com/HaiziIzzudin/ffmpeg-3worker/raw/main/2worker.py > 2worker.py; (Get-Content -path ~\2worker.py) | Set-Content -Encoding utf8NoBOM -Path ~\2worker.py; python ./2worker.py;
  ```
### Linux / UNIX equivalent
Run command below in BASH
- 3 Workers
  ```
  curl -fsSL https://raw.githubusercontent.com/HaiziIzzudin/ffmpeg-3worker/main/3worker_v2.py >> 3worker.py; python3 ./3worker.py
  ```
- 2 Workers
  ```
  curl -fsSL https://raw.githubusercontent.com/HaiziIzzudin/ffmpeg-3worker/main/2worker.py >> 2worker.py; python3 ./2worker.py
  ```

## CHANGELOGS
### Plan on Version 4
- Program can now detect threads count, and allocate automatically; OR maybe...
- User can now input their own CPU affinity.

### Plan on Version 3
- Continue encoding when process is interrupted or when sudden power loss occured.
- When there's only one ffmpeg encoding PID detected, all CPU affinity will then be updated to be allocated to that PID only.

### Version 2
- Users can now choose to remove or keep temporary files. Temporary files need to be DELETED to invoke ffmpeg-parallel again at later time.
- Concatenated video will now be dropped on Desktop instead of with the original file.
- Audio will now be processed with aac@320kb/s. Override by edit it in script.
- Processed fragments will now be encoded with .mkv container to avoid data corruption, and universability.
- User can now input custom FFmpeg command instead of the one provided.

### Version 1
- Initial release
