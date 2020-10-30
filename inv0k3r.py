import time
import os
import datetime
from threading import *
import re
import webbrowser


class Invoker(Thread):

    banner = """\n
    ██ ███   ██ ██    ██  ██████  ██   ██ ███████ ████████
    ██ ████  ██ ██    ██ ██    ██ ██  ██  ██      ██    ██
    ██ ██ ██ ██ ██    ██ ██    ██ █████   ███████ ████████
    ██ ██  ████  ██  ██  ██    ██ ██  ██  ██      ██  ██
    ██ ██   ███   ████    ██████  ██   ██ ███████ ██   ███

  .:.:.Script written by : @iam-v0id(SUHAAS KORAMPALLY).:.:.\n\n"""

    data = []
    currPlatform = None

    def run(self):
        while True:

            while True:
                Link = input('Enter a valid Meeting Link\t  : ')
                pattern = r"^[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$"
                if re.search(pattern, Link) == None:
                    print("INVALID URL")
                else:
                    break

            while True:
                try:
                    Time = list(map(int, input('Start Time(HH MM) <24-hour Format>: ').split()))
                    if Time[0] >= 0 and Time[0] < 24 and Time[1] >= 0 and Time[1] < 60:
                        break
                    else:
                        raise Exception
                except:
                    print("Expecting two space seperated integers [0-23] [0-59]")

            while True:
                try:
                    Duration = int(input('Duration of the meeting (Minutes) : '))
                    break
                except:
                    print("Expecting a single Integer")
            
            print('SUCCESS!!')
            print()

            curr = datetime.datetime.now()
            Meeting_Time = datetime.datetime(curr.year, curr.month, curr.day, Time[0], Time[1]).timestamp()
            self.data.append([Meeting_Time, Link, Duration])
            self.data.sort()

    def getPlatform(self):
        Platform = os.popen("uname -a 2> NUL").read()
        if 'Android' in Platform:
            return('Android')
        elif 'Linux' in Platform:
            return('Linux')
        else:
            return('Windows')

    def getPid(self):
        if self.currPlatform == 'Windows':
            try:
                return re.findall(r"\d+", os.popen("wmic process get Caption,ParentProcessId,ProcessId | find \"Zoom\"").read())[-1]
            except:
                os.system("zoom")
                time.sleep(10)
                return re.findall(r"\d+", os.popen("wmic process get Caption,ParentProcessId,ProcessId | find \"Zoom\"").read())[-1]
        elif self.currPlatform == 'Linux':
            pass
            """
                    TODO : Implement getPid() for Linux  
            """

    def invoke(self):
        self.currPlatform = self.getPlatform()
        while True:
            if len(self.data) > 0 and time.time() > self.data[0][0]:
                if self.currPlatform == 'Windows':
                    os.system("TASKKILL /F  /IM  Zoom.exe > NUL 2>&1")
                elif self.currPlatform == 'Linux':
                    os.system("pkill zoom")
                else:
                    os.system('termux-open-url %s  > /dev/null 2>&1' % data[0][1])
                    if 'zoom' in self.data[0][1]:
                        while (self.data[0][0]+60*self.data[0][2]) > time.time():
                            os.system('termux-open-url %s  > /dev/null 2>&1' % data[0][1])
                    del self.data[0]
                    continue
                webbrowser.open(self.data[0][1])
                if 'zoom' in self.data[0][1]:
                    time.sleep(100)
                    pid = self.getPid()
                    while (self.data[0][0]+60*self.data[0][2]) > time.time():
                        if pid != self.getPid():
                            webbrowser.open(self.data[0][1])
                            time.sleep(100)
                            pid = self.getPid()
                del self.data[0]


if __name__ == "__main__":
    print(Invoker.banner)
    t = Invoker()
    t.start()                  # Starting Thread
    t.invoke()
