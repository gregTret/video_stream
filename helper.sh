#!/bin/sh
ls
cd /home/nbgt/files/gits/video_stream
systemctl --user restart docker-desktop
python3 server.py

