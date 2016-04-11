#!/usr/bin/python3

import zmq
from threading import Thread

INPROC_ADDR = "inproc://command"

class Show(Thread):
    def __init__(self):
        super().__init__()
        self.ctx = zmq.Context.instance()
        self.comm_sock = self.ctx.socket(zmq.PAIR)
        self.comm_sock.bind(INPROC_ADDR)

    def run(self):
        ctx = zmq.Context.instance()
        sock = ctx.socket(zmq.PAIR)
        sock.connect(INPROC_ADDR)

        poller = zmq.Poller()
        poller.register(sock, zmq.POLLIN)

        while True:
            socks = dict(poller.poll(timeout=100))
            
            if sock in socks:
                (comm, data) = sock.recv_multipart()

                if comm == b"say":
                    print("You want me to say: {}".format(data))

                elif comm == b"quit":
                    print("Goodbye!")
                    break

    def Say(self, sth):
        self.comm_sock.send_multipart([b"say", sth.encode("utf-8")])

    def Quit(self):
        self.comm_sock.send_multipart([b"quit", b""])
        self.join()
