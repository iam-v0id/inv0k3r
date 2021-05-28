import time
import os
import datetime
from threading import Thread
import re
import webbrowser


class Data:
    def __init__(self, start_time, duration, link):
        self.start_time = start_time
        self.duration = duration
        self.link = link


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

            link = input('Enter a valid Meeting Link\t  : ').strip()

            while True:
                try:
                    meeting_time = list(
                        map(int, input('Start Time(HH MM) <24-hour Format>: ').split()))
                    if meeting_time[0] >= 0 and meeting_time[0] < 24 and meeting_time[1] >= 0 and meeting_time[1] < 60:
                        break
                    else:
                        raise Exception
                except:
                    print(
                        "Expecting two space seperated integers [0-23] [0-59]")

            while True:
                try:
                    duration = int(
                        input('Duration of the meeting (Minutes) : '))
                    break
                except:
                    print("Expecting a single Integer")

            curr = datetime.datetime.now()
            start_time = datetime.datetime(
                curr.year, curr.month, curr.day, meeting_time[0], meeting_time[1]).timestamp()
            self.data.append(Data(start_time, duration, link))
            self.data.sort(key=lambda x: x.start_time)
            print("\n----------SUCCESS! Added this to the queue----------\n\n")

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
                    TODO: Implement getPid() for Linux    
            """

    def invoke(self):
        self.currPlatform = self.getPlatform()
        while True:
            if len(self.data) > 0 and time.time() > self.data[0].start_time:
                if self.currPlatform == 'Windows':
                    os.system("TASKKILL /F  /IM  Zoom.exe > NUL 2>&1")
                    pass
                elif self.currPlatform == 'Linux':
                    os.system("pkill zoom")
                else:
                    os.system('termux-open-url %s  > /dev/null 2>&1' %
                              self.data[0].link)
                    if 'zoom' in self.data[0][1]:
                        while (self.data[0][0]+60*self.data[0][2]) > time.time():
                            os.system(
                                'termux-open-url %s  > /dev/null 2>&1' % self.data[0].link)
                    del self.data[0]
                    continue
                webbrowser.open(self.data[0].link)
                if 'zoom' in self.data[0].link:
                    time.sleep(100)
                    pid = self.getPid()
                    time.sleep(30*60)
                    while (self.data[0].start_time+60*self.data[0].duration) > time.time():
                        if pid != self.getPid():
                            webbrowser.open(self.data[0].link)
                            time.sleep(100)
                            pid = self.getPid()
                            time.sleep(
                                min(30*60, (self.data[0].start_time+60*self.data[0].duration)-time.time()))
                        time.sleep(50)
                del self.data[0]


if __name__ == "__main__":
    print(Invoker.banner)
    t = Invoker()
    t.start()                  # Starting Thread
    t.invoke()
