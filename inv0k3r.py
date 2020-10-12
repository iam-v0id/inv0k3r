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
            for minutes in range(Meeting_Times[0][2]):            
                os.system('%s %s  > NUL 2>&1' %(cmd, Meeting_Times[0][1]))
                if 'zoom' not in Meeting_Times[0][1]:
                    break
                time.sleep(60)
            del Meeting_Times[0]
