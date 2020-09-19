# Author : SUHAAS KORAMPALLY

import time
import datetime
import os
from threading import *


inv0k3r_logo ="""
 ██ ███   ██ ██    ██  ██████  ██   ██ ███████ ████████
 ██ ████  ██ ██    ██ ██    ██ ██  ██  ██      ██    ██
 ██ ██ ██ ██ ██    ██ ██    ██ █████   ███████ ████████
 ██ ██  ████  ██  ██  ██    ██ ██  ██  ██      ██  ██
 ██ ██   ███   ████    ██████  ██   ██ ███████ ██   ███

.:.:.Script written by: @iam-v0id(SUHAAS KORAMPALLY).:.:.\n\n"""
print(inv0k3r_logo)


Meeting_Link={}        # Dictionary to store Meeting Links, with Timestamp as key
Meeting_Times=[]       # List to store keys(Timestamps) in sorted order

""" Thread to continuously take input """
class Input(Thread):
    def run(self):
        while True:
            Link=input('Enter Meeting Link : ')
            Time=list(map(int,input('Time (HH MM) : ').split()))

            curr=datetime.datetime.now()
            Meeting_Time=datetime.datetime(curr.year,curr.month,curr.day,Time[0],Time[1]).timestamp()
            
            Meeting_Link[Meeting_Time]=Link         # Storing Meeting Link
            Meeting_Times.append(Meeting_Time)      # Keeping track of Key
            Meeting_Times.sort()                    

t=Input()          # Creating Object of Input Class
t.start()          # Starting Thread


""" Continuously compares current time with the first meeting's time """
while True:

    if  len(Meeting_Times)>0 and time.time() > Meeting_Times[0]:
        os.system("TASKKILL /F  /IM  Zoom.exe > NUL 2>&1")   # Kills the existing meeting if any
        os.system('start %s  > NUL 2>&1'%Meeting_Link[Meeting_Times[0]])  # Starts the meeting
        if 'zoom' in Meeting_Link[Meeting_Times[0]] :  
            time.sleep(41*60)
            os.system('start %s  > NUL 2>&1'%Meeting_Link[Meeting_Times[0]]) # Rejoins meeting after 41 mins
        del Meeting_Link[Meeting_Times[0]]   
        Meeting_Times.pop(0)
