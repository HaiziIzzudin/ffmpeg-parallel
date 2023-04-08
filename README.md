![MAIN_1](https://user-images.githubusercontent.com/79714350/215285318-486b5db3-a3bf-479b-af53-0f8160533f8c.gif)



# Encode with two concurrent ffmpeg process instead of one!
This is a Python script where ffmpeg will split inputted video into 2 parts, and encode it to their own cpu affinity SIMULTANEOUSLY to utilize CPU 100%

## REQUIREMENT / DEPENDENCIES
- ffmpeg 6, MUST accessible thru PATH. (Automated installation within this script will be added later on version 4, hopefully)
- python, MUST accessible in PATH
- pip
- Windows only: Please install PowerShell version 6 or above.

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
irm https://github.com/HaiziIzzudin/ffmpeg-parallel/raw/main/parallel_v3.2.py > ffparal.py; (Get-Content -path ~\ffparal.py) | Set-Content -Encoding utf8NoBOM -Path ~\ffparal.py; python ./ffparal.py;
```

### Linux / UNIX equivalent
Run command below in BASH
```
curl -fsSL https://github.com/HaiziIzzudin/ffmpeg-parallel/raw/main/parallel_v3.2.py >> ffparal.py; python3 ./ffparal.py
```

## CHANGELOGS
### **NEW: VERSION 3.3**
Version 3.3 brings cleanup to underlying code. This includes:
- Lesser line of code count (incl empty line).
- Longer explaination of certain subjects has been shorten.

**Consider donating! I set it as low as 1$ (~ 4.40 MYR):
[ko-fi.com/haiziizzudin](https://ko-fi.com/haiziizzudin)**

### Version 3.2
- Added linux support.
- Fix path quotation marks.

### Version 3.1
- Video with multitrack audio will now be encoded wholesale, no encode only one stream.
- (Your source video now must have at least one audio track, or else script will fail.)
- AAC has been changed to m4a, to support multitrack audio support.
- Added libx264 (H.264) as encode option.
- Removed option to set frame rate (frankly, this will fuck up the video more. So, I let it go.)


### Version 3.0
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



