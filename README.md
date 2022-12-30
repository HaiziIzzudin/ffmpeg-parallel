# ffmpeg-3worker
Python script where ffmpeg will broke a video into 3 parts, and encode it to their own cpu affinity to avoid system crash.

## REQUIREMENT / DEPENDENCIES
- ffmpeg, MUST accessible thru PATH. Those who don't know how to install I will provide tutorial later.
- python, MUST accessible in PATH
- pip, because you want to install some of other python module dependency
  - After installing pip, execute command below:
    ```
    asasasasasasas
    ```
- If you going to use Windows, please install PowerShell version 6 or above.

## DOWNLOAD AND RUN SCRIPT
### Windows
You MUST and HAVE to run this command inside powershell version 6 and above. The one shipped with Windows is version 5. Do get the latest PowerShell by invoking `winget install microsoft.powershell`, OR if you don't have winget, [download here](https://learn.microsoft.com/en-gb/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.3#msi).
```
irm https://github.com/HaiziIzzudin/ffmpeg-3worker/raw/main/3worker.py > 3worker.py; (Get-Content -path ~\3worker.py) | Set-Content -Encoding utf8NoBOM -Path ~\3worker.py; python ./3worker.py;
```
### Linux / UNIX equivalent
Run command below in BASH
```
curl -fsSL https://raw.githubusercontent.com/HaiziIzzudin/ffmpeg-3worker/main/3worker.py >> 3worker.py; python3 ./3worker.py
```
