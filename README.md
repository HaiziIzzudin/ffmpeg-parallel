# ffmpeg-3worker
Python script where ffmpeg will broke a video into 3 parts, and encode it to their own cpu affinity to avoid system crash.

## Download and run script:
### Windows
```
irm https://github.com/HaiziIzzudin/ffmpeg-3worker/raw/main/3worker.py > 3worker.py; (Get-Content -path ~\3worker.py) | Set-Content -Encoding utf8NoBOM -Path ~\3worker.py; python ./3worker.py;
```
