import threading
import time


def doThreading(func, args, waitingTime=0):
    if waitingTime:
        time.sleep(waitingTime)
    t = threading.Thread(target=func, args=args)
    t.start()
