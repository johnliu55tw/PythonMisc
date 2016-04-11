#!/usr/bin/python3

import signal
import time

def handler(signum, frame):
    pass

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, 0.1, 0.1)
    
    counter = 0
    while True:
        signal.pause()
        print("Time up! {}".format(time.time()))

