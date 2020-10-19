import time
import os
import datetime
from threading import *
import re


class Invoker(Thread):

    banner = """
     ██ ███   ██ ██    ██  ██████  ██   ██ ███████ ████████
     ██ ████  ██ ██    ██ ██    ██ ██  ██  ██      ██    ██
     ██ ██ ██ ██ ██    ██ ██    ██ █████   ███████ ████████
     ██ ██  ████  ██  ██  ██    ██ ██  ██  ██      ██  ██
     ██ ██   ███   ████    ██████  ██   ██ ███████ ██   ███

    .:.:.Script written by: @iam-v0id(SUHAAS KORAMPALLY).:.:.\n\n"""

    Meeting_Times = []

    def run(self):
        while True:
            Link = input('Enter Meeting Link : ')
            Time = list(map(int, input('Time (HH MM) : ').split()))
            Duration = int(input('Duration of the meeting (Minutes) : '))
            curr = datetime.datetime.now()
            Meeting_Time = datetime.datetime(
                curr.year, curr.month, curr.day, Time[0], Time[1]).timestamp()

            self.Meeting_Times.append([Meeting_Time, Link, Duration])
            self.Meeting_Times.sort()

    def getPlatform(self):
        Platform = os.popen("uname -a 2> NUL").read()
        if 'Android' in Platform:
            return('Android')
        elif 'Linux' in Platform:
            return('Linux')
        else:
            return('Windows')

    def getCommand(self, currPlatform):
        if currPlatform == 'Windows':
            return('start')
        elif currPlatform == 'Android':
            return('termux-open-url')
        elif currPlatform == 'Linux':
            return('firefox')

    def getPid(self):
        return re.findall(r"\d+", os.popen("wmic process get Caption,ParentProcessId,ProcessId | find \"Zoom\"").read())[-1]

if __name__ == "__main__":
    print(Invoker.banner)
    t = Invoker()              # Creating Object of Input Class
    t.start()                  # Starting Thread
    currPlatform = t.getPlatform()
    cmd = t.getCommand(currPlatform)

    while True:
        if len(t.Meeting_Times) > 0 and time.time() > t.Meeting_Times[0][0]:
            # Kills the existing meeting if any
            if currPlatform == 'Windows':
                os.system("TASKKILL /F  /IM  Zoom.exe > NUL 2>&1")
            elif currPlatform == 'Linux':
                os.system("pkill zoom")
            # Starts the meeting
            os.system('%s %s  > NUL 2>&1' % (cmd, t.Meeting_Times[0][1]))
            if 'zoom' in Meeting_Times[0][1]:
                time.sleep(100)
                pid = t.getPid()
                while (t.Meeting_Times[0][0]+60*t.Meeting_Times[0][2]) > time.time():
                    if pid != t.getPid():
                        os.system('%s %s  > NUL 2>&1' %(cmd, Meeting_Times[0][1]))
                        time.sleep(100)
                        pid = t.getPid()
            del Meeting_Times[0]
