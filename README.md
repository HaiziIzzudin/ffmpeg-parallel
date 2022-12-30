# ffmpeg-3worker
Python script where ffmpeg will broke a video into 3 parts, and encode it to their own cpu affinity to avoid system crash.

## Download and run script:
### Windows
You MUST and HAVE to run this command inside powershell version 6 and above. The one shipped with Windows is version 5. Do get the latest PowerShell by invoking `winget install microsoft.powershell`, OR if you don't have winget, [download here](https://learn.microsoft.com/en-gb/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.3#msi).
```
irm https://github.com/HaiziIzzudin/ffmpeg-3worker/raw/main/3worker.py > 3worker.py; (Get-Content -path ~\3worker.py) | Set-Content -Encoding utf8NoBOM -Path ~\3worker.py; python ./3worker.py;
```
