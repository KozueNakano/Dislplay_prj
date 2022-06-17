#!/usr/bin/python3
import sys
import subprocess

cmd = "omxplayer /home/pi/Display_prj/gura.mp4"
print(cmd)
proc = subprocess.Popen(cmd, shell=True, 
                                stdin=subprocess.PIPE, 
                                universal_newlines=True)
proc.wait()