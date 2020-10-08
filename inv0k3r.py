# Author : SUHAAS KORAMPALLY
from myimports import *

print(banner.logo)

Meeting_Link = {}        # Dictionary to store Meeting Links, with Timestamp as key
Meeting_Times = []       # List to store keys(Timestamps) in sorted order


class Input(Thread):
    def run(self):
        while True:
            Link = input('Enter Meeting Link : ')
            Time = list(map(int, input('Time (HH MM) : ').split()))
            curr = datetime.datetime.now()
            Meeting_Time = datetime.datetime(
                curr.year, curr.month, curr.day, Time[0], Time[1]).timestamp()

            Meeting_Link[Meeting_Time] = Link         # Storing Meeting Link
            Meeting_Times.append(Meeting_Time)        # Keeping track of Key
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
        if len(Meeting_Times) > 0 and time.time() > Meeting_Times[0]:
            # Kills the existing meeting if any
            if currPlatform == 'Windows':
                os.system("TASKKILL /F  /IM  Zoom.exe > NUL 2>&1")
            elif currPlatform == 'Linux':
                os.system("pkill zoom")
            # Starts the meeting
            os.system('%s %s  > NUL 2>&1' %
                      (cmd, Meeting_Link[Meeting_Times[0]]))
            # Rejoins meeting after 40 mins
            if 'zoom' in Meeting_Link[Meeting_Times[0]]:
                time.sleep(40*60)
                os.system('%s %s  > NUL 2>&1' %
                          (cmd, Meeting_Link[Meeting_Times[0]]))
            del Meeting_Link[Meeting_Times[0]]
            Meeting_Times.pop(0)
