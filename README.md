# A simple tool that I use to merge the mp3 files

## Prerequisites
natsort & ffmpeg utils installed
```
pip3 install ffmpeg
pip3 install natsort
```

ffmpeg -f concat -safe 0 -i list.txt -c copy Portrait.mp3