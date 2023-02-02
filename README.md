![MAIN_1](https://user-images.githubusercontent.com/79714350/215285318-486b5db3-a3bf-479b-af53-0f8160533f8c.gif)



# Encode with two concurrent ffmpeg process instead of one!
This is a Python script where ffmpeg will split inputted video into 2 parts, and encode it to their own cpu affinity SIMULTANEOUSLY to utilize CPU 100%

## REQUIREMENT / DEPENDENCIES
- ffmpeg 5.2, MUST accessible thru PATH. (Automated installation within this script will be added later on version 3.5, hopefully)
- python, MUST accessible in PATH
- If you going to use Windows, please install PowerShell version 6 or above.

## IMPORTANT NOTE
This script has been tailored for me and my machine. That's why I provide in script mode, not executable mode. Since this script is editable and open source, go ahead and change some of the parameters inside the script to match what's spec on your machine.

Some of the parameters that you can change is:
  - CPU Affinity allocation
  - LINUX ONLY: Terminal name (my script is written for Konsole, which is KDE desktop environment command prompt)
  
Hopefully the next update I can eliminate some of the problem above.

## DOWNLOAD AND RUN SCRIPT
### Windows
You MUST and HAVE to run this command inside powershell version 6 and above. The one shipped with Windows is most probably old. Get the latest PowerShell by invoking `winget install microsoft.powershell`, OR if you don't have winget, [download here](https://learn.microsoft.com/en-gb/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.3#msi).
```
irm https://raw.githubusercontent.com/HaiziIzzudin/ffmpeg-parallel/main/parallel_v3-1.py > parallel_v3-1.py; (Get-Content -path ~\parallel_v3-1.py) | Set-Content -Encoding utf8NoBOM -Path ~\parallel_v3-1.py; python ./parallel_v3-1.py;
```

### Linux / UNIX equivalent (Still on v2, pls wait for me to port for linux. I try to find best affordable linux VPS with DE support. If u hv suggestions, leave it in [issues](https://github.com/HaiziIzzudin/ffmpeg-parallel/issues))
Run command below in BASH
```
curl -fsSL https://raw.githubusercontent.com/HaiziIzzudin/ffmpeg-parallel/main/3worker_v2.py >> 3worker_v2.py; python3 ./3worker_v2.py
```

## CHANGELOGS
### NEW: VERSION 3.1
Version 3.1 is nothing very drastic, but it addresses some of the problem it have:
- Video with multitrack audio will now be encoded wholesale, no encode only one stream.
- (Your source video now must have at least one audio track, or else script will fail.)
- AAC has been changed to m4a, to support multitrack audio support.
- Added libx264 (H.264) as encode option.

Expect version 3.2 will add linux support (idk when tho, I'm busy lately.)

**Consider donating! I set it as low as 1$ (~ 4.40 MYR):
[ko-fi.com/haiziizzudin](https://ko-fi.com/haiziizzudin)**

### Version 3
Version 3 brings improvement under the hood from v2. This includes:
- Path will now doesn't care if its contains spaces or not.
- Codes, cache, and user interaction improvements.
- Uses colorama for header design.
- Encoded file will now drop in same path as the original file resides. No more on desktop.
- No more user has to install additional packages! Script has all included.
- HOTFIX 1: Remove python script file if user select to remove.

### Version 2
- Users can now choose to remove or keep temporary files. Temporary files need to be DELETED to invoke ffmpeg-parallel again at later time.
- Concatenated video will now be dropped on Desktop instead of with the original file.
- Audio will now be processed with aac@320kb/s. Override by edit it in script.
- Processed fragments will now be encoded with .mkv container to avoid data corruption, and universability.
- User can now input custom FFmpeg command instead of the one provided.

### Version 1
- Initial release



