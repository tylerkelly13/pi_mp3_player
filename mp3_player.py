# -*- coding: utf-8 -*-
"""
Basic MP3 player for raspberry pi

WARNING Infinite loop!

By Tyler Kelly
"""

import subprocess
import random
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def next_track(channel):
    proc.kill()

DIR = '/home/pi/music'   # music top directory
POS = '/home/pi/pos'   # last tracked play file

if os.path.isfile(POS):
    fin = open((POS), 'r')
    last = fin.read(10)
    if (len(last) < 1):
        last = 5
    if (int(last) >= 0):
        last = int(last)
    else:
        last = 5
    fin.close()
else:
    last = 1
counter = 1
os.chdir(DIR) # change directory to music
playlist = {}
for root, dirs, files in os.walk(DIR):
    for name in files:
        if name.endswith('.mp3'):
            path= os.path.join(root,name)
            playlist[counter]=path
            counter = counter + 1
            
leng = int(len(playlist))

if last < 10:
    track = last + random.randint(1,10) 
else:
    track = last - random.randint(1,9)
    
song = playlist[track]
play = ['mpg123','-C',song]
proc = subprocess.Popen(play)
GPIO.add_event_detect(17, GPIO.FALLING, callback=next_track, bouncetime=300)
proc.wait()

while True:
    track = random.randint(1,leng) 
    song = playlist[track]
    proc = subprocess.Popen(['mpg123','-C',song])   
    proc.wait()
    if os.path.isfile(POS):
        os.remove(POS)
    fout = open((POS), 'wt')
    print(track,file=fout)
    fout.close()
