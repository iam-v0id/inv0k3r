# Author : SUHAAS KORAMPALLY
from myimports import *

print(banner.logo)

Meeting_Times = []       # List to store keys(Timestamps) in sorted order


class Input(Thread):
    def run(self):
        while True:
            Link = input('Enter Meeting Link : ')
            Time = list(map(int, input('Time (HH MM) : ').split()))
            Duration = int(input('Duration of the meeting (Minutes) : '))
            curr = datetime.datetime.now()
            Meeting_Time = datetime.datetime(
                curr.year, curr.month, curr.day, Time[0], Time[1]).timestamp()

            Meeting_Times.append([Meeting_Time,Link,Duration])     
            Meeting_Times.sort()


if __name__ == "__main__":
    t = Input()              # Creating Object of Input Class
    t.start()                # Starting Thread

    currPlatform = Platform.getPlatform()
    if currPlatform == 'Windows':
        cmd = 'start'
    elif currPlatform == 'Android':
        cmd = 'termux-open-url'
    elif currPlatform == 'Linux':
        cmd = 'firefox'

    while True:
        if len(Meeting_Times) > 0 and time.time() > Meeting_Times[0][0]:
            # Kills the existing meeting if any
            if currPlatform == 'Windows':
                os.system("TASKKILL /F  /IM  Zoom.exe > NUL 2>&1")
            elif currPlatform == 'Linux':
                os.system("pkill zoom")
            # Starts the meeting         
            os.system('%s %s  > NUL 2>&1' %(cmd, Meeting_Times[0][1]))
            if 'zoom' in Meeting_Times[0][1]:
                time.sleep(100)
                pid= re.findall(r"\d+",os.popen("wmic process get Caption,ParentProcessId,ProcessId | find \"Zoom\"").read())[-1]
                while (Meeting_Times[0][0]+60*Meeting_Times[0][2])>time.time() :
                    curr_pid=re.findall(r"\d+",os.popen("wmic process get Caption,ParentProcessId,ProcessId | find \"Zoom\"").read())[-1]
                    if pid != curr_pid:
                        os.system('%s %s  > NUL 2>&1' %(cmd, Meeting_Times[0][1]))
                        time.sleep(100)
                        pid=re.findall(r"\d+",os.popen("wmic process get Caption,ParentProcessId,ProcessId | find \"Zoom\"").read())[-1]
            del Meeting_Times[0]
