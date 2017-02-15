import sched
import time
import threading


def doEvent(name, event):
    print("{} doEvent @ {}: {}".format(name, time.time(), str(event)))


def startPeriodic(name, period):
    scheduler = sched.scheduler(time.time, time.sleep)
    nextGoTime = time.time()

    while True:
        nextGoTime += period
        scheduler.enterabs(time=nextGoTime, priority=1,
                           action=doEvent, argument=(name, 'hello!'))
        scheduler.run()


if __name__ == "__main__":

    periods = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    threads = list()

    for period in periods:
        thread = threading.Thread(name="Period_{}".format(period),
                                  target=startPeriodic,
                                  args=("Period_{}".format(period), period))
        threads.append(thread)
        thread.start()

    while True:
        "Main loop entering sleep..."
        time.sleep(10)
