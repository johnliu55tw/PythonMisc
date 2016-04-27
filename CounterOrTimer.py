#!/usr/bin/python3

from threading import Thread
from multiprocessing import Process
import time
import zmq


class CounterOrTimer(Process):
    def __init__(self):
        super().__init__()
        self.alarmAddr = "inproc://alarm"
        self.eventAddr = "ipc:///tmp/event.ipc"


    def _alarm(self):
        time = 5000
        ctx = zmq.Context.instance()
        print(ctx)
        sock = ctx.socket(zmq.PAIR)
        print(self.alarmAddr)
        sock.connect(self.alarmAddr)

        while True:
            evt = sock.poll(timeout=time, flags=zmq.POLLIN)
            if evt & zmq.POLLIN:
                data = sock.recv()
                if data == b"stop":
                    break

                try:
                    time = int(data)
                except ValueError:
                    print("Unable to parse time")

                continue

            elif evt == 0:
                sock.send(b"alarm")

    def run(self):
        self.backendCtx = zmq.Context.instance()
        print(self.backendCtx)

        self.eventSock = self.backendCtx.socket(zmq.SUB)
        self.eventSock.setsockopt(zmq.SUBSCRIBE, b"")
        self.eventSock.bind(self.eventAddr)

        self.alarmSock = self.backendCtx.socket(zmq.PAIR)
        self.alarmSock.bind(self.alarmAddr)

        self.poller = zmq.Poller()
        self.poller.register(self.alarmSock, zmq.POLLIN)
        self.poller.register(self.eventSock, zmq.POLLIN)

        alarmThread = Thread(target=self._alarm, daemon=True)
        alarmThread.start()

        self.counter = 0

        while True:
            readySocks = dict(self.poller.poll())

            if self.eventSock in readySocks:
                data = self.eventSock.recv()
                print(data)
                self.counter += 1
                if self.counter == 10:
                    print("Counter = {}".format(self.counter))
                    self.counter = 0
                    print("Change timer interval to 3000")
                    self.alarmSock.send(b"3000")

            elif self.alarmSock in readySocks:
                _ = self.alarmSock.recv()
                print("Alarm Clock: {}".format(time.time()))
                print("Counter = {}".format(self.counter))
                self.counter = 0


if __name__ == "__main__":
    p = CounterOrTimer()
    p.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
