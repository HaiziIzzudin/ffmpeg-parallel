# ffmpeg-3worker
Python script where ffmpeg will broke a video into 3 parts, and encode it to their own cpu affinity to avoid system crash.

## Download and run script:
### Windows
You MUST and HAVE to run this command inside powershell version 6 and above. The one shipped with Windows is version 5. Do get the latest PowerShell by invoking `winget install microsoft.powershell`. OR if you don't have winget, [download here](https://objects.githubusercontent.com/github-production-release-asset-2e65be/49609581/41eea90a-04c6-4840-993a-996d67ca41b6?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20221230%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20221230T105116Z&X-Amz-Expires=300&X-Amz-Signature=8edf6f348a5d1fb7f8fa3befd70bee2b8d87e5ec5e04f70fe11fb67fd33232ee&X-Amz-SignedHeaders=host&actor_id=79714350&key_id=0&repo_id=49609581&response-content-disposition=attachment%3B%20filename%3DPowerShell-7.3.0-win-x64.msi&response-content-type=application%2Foctet-stream).
```
irm https://github.com/HaiziIzzudin/ffmpeg-3worker/raw/main/3worker.py > 3worker.py; (Get-Content -path ~\3worker.py) | Set-Content -Encoding utf8NoBOM -Path ~\3worker.py; python ./3worker.py;
```
