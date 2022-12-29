# ffmpeg-3worker
Python script where ffmpeg will broke a video into 3 parts, and encode it to their own cpu affinity to avoid system crash. STILL PRELIMINARY SOFTWARE.

## Install and run script:
```
irm https://github.com/HaiziIzzudin/ffmpeg-3worker/raw/main/3worker.py > 3worker.py; (Get-Content -path %USERPROFILE%\3worker.py) | Set-Content -Encoding utf8 -Path %USERPROFILE%\3worker.py; python ./3worker.py;
```