#!/usr/bin/python3

import signal
from multiprocessing import Process
from os import urandom
import zmq

IPC_ADDR = "ipc:///tmp/{}.ipc".format(urandom(8).hex())

class IntervalRunner(Process):
    def __init__(self, interval):
        super().__init__()
        self.interval = interval
        self.ctx = zmq.Context()
        self.comm = self.ctx.socket(zmq.PAIR)
        self.comm.bind(IPC_ADDR)

    def _dummyHandler(self, signum, frame):
        pass

    def run(self):
        ctx = zmq.Context()
        sock = ctx.socket(zmq.PAIR)
        sock.connect(IPC_ADDR)

        # Set up interval timer with a dummy handler
        signal.signal(signal.SIGALRM, self._dummyHandler)
        signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

        while True:
            # Wait for the timer
            signal.pause()
            try:
                # Non-blocking recv
                (comm, data) = sock.recv_multipart(flags=zmq.NOBLOCK)
            except zmq.Again:
                # No data ready, go back to wait for the timer
                continue

            # Handling command
            if comm == b"say":
                print("You want me to say: {}".format(data))
            elif comm == b"quit":
                print("Goodbye!")
                break

    def Say(self, sth):
        self.comm.send_multipart([b"say", sth.encode("utf-8")])

    def Quit(self):
        self.comm.send_multipart([b"quit", b""])
        self.join()
